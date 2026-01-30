# database.py - In-memory document store for deed analysis
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, Optional

_store: Dict[int, Dict[str, Any]] = {}
_next_id = 1

# JSON 파일 저장 디렉터리 (deed-service/data/)
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def _persist_to_file(doc: Dict[str, Any]) -> None:
    """문서 한 건을 JSON 파일로 저장."""
    doc_id = doc.get("id")
    if not doc_id:
        return
    path = DATA_DIR / f"document_{doc_id}.json"
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
    except Exception:
        # 파일 저장 실패 시에도 서비스 전체가 죽지 않도록 조용히 무시
        pass


def save_document(
    extracted_text: str,
    parsed_data: Optional[Dict] = None,
    sections: Optional[Dict[str, str]] = None,
    **extra: Any,
) -> int:
    """새 문서 저장 + JSON 파일로도 남김."""
    global _next_id
    doc_id = _next_id
    _next_id += 1
    _store[doc_id] = {
        "id": doc_id,
        "extracted_text": extracted_text,
        "parsed_data": parsed_data or {},
        "sections": sections or {},
        **extra,
    }
    _persist_to_file(_store[doc_id])
    return doc_id


def get_document(doc_id: int) -> Optional[Dict[str, Any]]:
    return _store.get(doc_id)


def update_document(doc_id: int, **kwargs: Any) -> bool:
    """문서 수정 + 수정된 내용 JSON 파일로 다시 저장."""
    if doc_id not in _store:
        return False
    for k, v in kwargs.items():
        _store[doc_id][k] = v
    _persist_to_file(_store[doc_id])
    return True
