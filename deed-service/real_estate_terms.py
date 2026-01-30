# real_estate_terms.py - 부동산/등기 용어 OCR 오인식 보정
import re
from typing import Dict

TYPO_TO_CANONICAL: Dict[str, str] = {
    "표게부": "표제부", "표계부": "표제부", "표재부": "표제부", "표개부": "표제부",
    "소 재 지": "소재지", "면젹": "면적", "등기 일자": "등기일자",
    "갑구": "갑구", "을구": "을구", "근저당": "근저당", "저당권": "저당권",
    "임차인": "임차인", "임대인": "임대인", "전세권": "전세권",
}

REGEX_REPLACEMENTS = [
    (re.compile(r"소\s*재\s*지", re.IGNORECASE), "소재지"),
    (re.compile(r"면\s*적", re.IGNORECASE), "면적"),
    (re.compile(r"m2|m²", re.IGNORECASE), "㎡"),
]


def correct_with_vocab(text: str) -> str:
    if not text or not text.strip():
        return text
    out = text
    for pattern, repl in REGEX_REPLACEMENTS:
        out = pattern.sub(repl, out)
    tokens = out.split()
    corrected = [TYPO_TO_CANONICAL.get(t, t) for t in tokens]
    return " ".join(corrected)
