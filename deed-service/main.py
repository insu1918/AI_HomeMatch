# main.py - 등기부등본 분석 API (FastAPI)
from __future__ import annotations
import base64
import io
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import database as db
from ocr_service import extract_text, get_detection_regions
from parser import parse_registry_text, split_registry_sections
from llm_structured import extract_structured
from llm_risk_analysis import build_risk_flags, explain_risk, build_check_items

app = FastAPI(title="등기부등본 분석 API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- PDF 지원 ----------
def pdf_to_images(file_bytes: bytes) -> List[bytes]:
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        images = []
        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap(dpi=150)
            images.append(pix.tobytes("png"))
        doc.close()
        return images
    except Exception:
        return []


def is_pdf(bytes_head: bytes) -> bool:
    return bytes_head[:4] == b"%PDF"


# ---------- Upload ----------
@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    preprocess: str = Form("none"),
    use_llm_correction: str = Form("false"),
):
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="파일이 비어 있습니다.")
    use_llm = use_llm_correction.lower() == "true"
    preprocess = preprocess if preprocess in ("none", "doc", "light", "full") else "none"

    if is_pdf(raw):
        images = pdf_to_images(raw)
        if not images:
            raise HTTPException(status_code=400, detail="PDF에서 이미지를 추출할 수 없습니다.")
        all_texts = []
        for img_bytes in images:
            txt = extract_text(img_bytes, preprocess=preprocess, use_llm_correction=use_llm)
            all_texts.append(txt)
        extracted_text = "\n\n--- 페이지 구분 ---\n\n".join(all_texts)
        regions = []
        image_data_url = None
        if images:
            regions, _ = get_detection_regions(images[0], preprocess)
            image_data_url = "data:image/png;base64," + base64.b64encode(images[0]).decode("utf-8")
    else:
        extracted_text = extract_text(raw, preprocess=preprocess, use_llm_correction=use_llm)
        regions, _ = get_detection_regions(raw, preprocess)
        image_data_url = "data:image/png;base64," + base64.b64encode(raw).decode("utf-8") if raw else None

    parsed_data = parse_registry_text(extracted_text)
    sections = split_registry_sections(extracted_text)
    doc_id = db.save_document(
        extracted_text=extracted_text,
        parsed_data=parsed_data,
        sections=sections,
    )
    return {
        "document_id": doc_id,
        "extracted_text": extracted_text,
        "parsed_data": parsed_data,
        "sections": sections,
        "regions": regions,
        "image_data_url": image_data_url,
    }


# ---------- Document ----------
@app.get("/documents/{document_id}")
async def get_document(document_id: int):
    doc = db.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
    return doc


class SectionUpdate(BaseModel):
    pyojebu: Optional[str] = None
    gapgu: Optional[str] = None
    eulgu: Optional[str] = None


@app.post("/documents/{document_id}/sections")
async def update_sections(document_id: int, body: SectionUpdate):
    doc = db.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
    sec = doc.get("sections") or {}
    parts = [
        body.pyojebu if body.pyojebu is not None else sec.get("pyojebu", ""),
        body.gapgu if body.gapgu is not None else sec.get("gapgu", ""),
        body.eulgu if body.eulgu is not None else sec.get("eulgu", ""),
    ]
    new_text = "\n\n".join(parts)
    parsed_data = parse_registry_text(new_text)
    sections = {"pyojebu": parts[0], "gapgu": parts[1], "eulgu": parts[2]}
    db.update_document(document_id, extracted_text=new_text, parsed_data=parsed_data, sections=sections)
    doc = db.get_document(document_id)
    return {
        "document_id": document_id,
        "extracted_text": doc["extracted_text"],
        "parsed_data": doc["parsed_data"],
        "sections": doc["sections"],
    }


@app.post("/documents/{document_id}/llm-structure")
async def llm_structure(document_id: int):
    doc = db.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
    text = doc.get("extracted_text") or ""
    structured = extract_structured(text)
    db.update_document(document_id, parsed_data=structured)
    return {"success": True, "document_id": document_id, "structured": structured}


@app.post("/documents/{document_id}/risk-analysis")
async def risk_analysis(document_id: int):
    doc = db.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")
    # 파서 개선 사항이 즉시 반영되도록, 저장된 parsed_data가 있더라도 항상 재파싱
    text = doc.get("extracted_text") or ""
    structured = parse_registry_text(text)
    db.update_document(document_id, parsed_data=structured)
    risk_flags = build_risk_flags(structured)
    explanation = explain_risk(structured, risk_flags)
    check_items = build_check_items(structured)
    return {
        "success": True,
        "document_id": document_id,
        "structured": structured,
        "risk_flags": risk_flags,
        "explanation": explanation,
        "check_items": check_items,  # 6가지 질문별 답변
    }


@app.get("/health")
def health():
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
