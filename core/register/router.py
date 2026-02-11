from __future__ import annotations

import os
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from .ocr_service import extract_text
from .parser import parse_registry_text, split_registry_sections
from .pdf_utils import is_pdf, pdf_to_images
from .risk_analysis import build_check_items, build_risk_flags, explain_risk
from .storage import get_document, save_document, update_document

# 페이지별 OCR 병렬 처리 워커 수 (환경변수 DEED_OCR_MAX_WORKERS로 조절 가능)
_MAX_OCR_WORKERS = int(os.environ.get("DEED_OCR_MAX_WORKERS", "2"))

router = APIRouter()


class SectionUpdate(BaseModel):
    pyojebu: Optional[str] = None
    gapgu: Optional[str] = None
    eulgu: Optional[str] = None


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    preprocess: str = Form("none"),  # reserved (호환용)
    use_llm_correction: str = Form("false"),  # reserved (호환용)
):
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="파일이 비어 있습니다.")

    timing_ms: Dict[str, float] = {}

    if is_pdf(raw):
        t0 = time.perf_counter()
        images = pdf_to_images(raw)
        timing_ms["pdf_to_images"] = round((time.perf_counter() - t0) * 1000)

        t1 = time.perf_counter()
        if len(images) == 1:
            all_texts = [extract_text(images[0])]
        else:
            workers = min(_MAX_OCR_WORKERS, len(images))
            with ThreadPoolExecutor(max_workers=workers) as executor:
                all_texts = list(executor.map(extract_text, images))
        extracted_text = "\n\n--- 페이지 구분 ---\n\n".join(all_texts)
        timing_ms["ocr"] = round((time.perf_counter() - t1) * 1000)
    else:
        t1 = time.perf_counter()
        extracted_text = extract_text(raw)
        timing_ms["ocr"] = round((time.perf_counter() - t1) * 1000)

    t2 = time.perf_counter()
    structured = parse_registry_text(extracted_text)
    sections = split_registry_sections(extracted_text)
    timing_ms["parse"] = round((time.perf_counter() - t2) * 1000)

    t3 = time.perf_counter()
    doc_id = save_document(extracted_text=extracted_text, parsed_data=structured, sections=sections)
    timing_ms["save"] = round((time.perf_counter() - t3) * 1000)

    timing_ms["total_upload"] = round(sum(timing_ms.values()), 0)
    print("[등기부 upload] timing_ms:", timing_ms)

    return {
        "document_id": doc_id,
        "extracted_text": extracted_text,
        "parsed_data": structured,
        "sections": sections,
        "timing_ms": timing_ms,
    }


@router.get("/documents/{document_id}")
async def get_doc(document_id: int):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
    return doc


@router.post("/documents/{document_id}/sections")
async def update_sections(document_id: int, body: SectionUpdate):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
    sec = doc.get("sections") or {}
    parts = [
        body.pyojebu if body.pyojebu is not None else sec.get("pyojebu", ""),
        body.gapgu if body.gapgu is not None else sec.get("gapgu", ""),
        body.eulgu if body.eulgu is not None else sec.get("eulgu", ""),
    ]
    new_text = "\n\n".join(parts)
    structured = parse_registry_text(new_text)
    sections = {"pyojebu": parts[0], "gapgu": parts[1], "eulgu": parts[2]}
    update_document(document_id, extracted_text=new_text, parsed_data=structured, sections=sections)
    doc = get_document(document_id) or {}
    return {
        "document_id": document_id,
        "extracted_text": doc.get("extracted_text"),
        "parsed_data": doc.get("parsed_data"),
        "sections": doc.get("sections"),
    }


@router.post("/documents/{document_id}/risk-analysis")
async def risk_analysis(document_id: int):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
    text = doc.get("extracted_text") or ""

    timing_ms: Dict[str, float] = {}

    t0 = time.perf_counter()
    structured = parse_registry_text(text)
    update_document(document_id, parsed_data=structured)
    timing_ms["parse"] = round((time.perf_counter() - t0) * 1000)

    t1 = time.perf_counter()
    risk_flags = build_risk_flags(structured)
    timing_ms["risk_flags"] = round((time.perf_counter() - t1) * 1000)

    t2 = time.perf_counter()
    explanation = explain_risk(structured, risk_flags)
    timing_ms["explain_risk"] = round((time.perf_counter() - t2) * 1000)

    t3 = time.perf_counter()
    check_items = build_check_items(structured)
    timing_ms["check_items"] = round((time.perf_counter() - t3) * 1000)

    timing_ms["total_risk_analysis"] = round(sum(timing_ms.values()), 0)
    print("[등기부 risk-analysis] timing_ms:", timing_ms)

    return {
        "success": True,
        "document_id": document_id,
        "structured": structured,
        "risk_flags": risk_flags,
        "explanation": explanation,
        "check_items": check_items,
        "timing_ms": timing_ms,
    }

