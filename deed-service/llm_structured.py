# llm_structured.py - LLM으로 등기부 텍스트 → JSON 구조화
from __future__ import annotations
import json
import os
import re
from typing import Any, Dict, Optional

STRUCT_SYSTEM = """당신은 대한민국 부동산 등기부등본의 구조를 이해하는 정보 추출 전문 AI입니다.
당신의 임무는 법률 판단이나 해석이 아니라, 등기부 텍스트에서 객관적인 사실 정보만 정확하게 추출하여 지정된 JSON 형식으로 변환하는 것입니다.
절대 하지 말아야 할 것: 위험하다/안전하다 같은 판단, 법적 해석, 추측 또는 보완.
오직 등기부에 적힌 내용만 구조화하십시오. 값이 없으면 null로 표시하십시오."""

STRUCT_USER_TEMPLATE = """다음은 부동산 등기부등본 OCR 텍스트입니다.

[등기부 텍스트 시작]
{ocr_text}
[등기부 텍스트 끝]

아래 JSON 스키마에 맞춰 정보를 추출하세요. 반드시 JSON만 반환하세요.

{{
  "property_info": {{
    "address": "",
    "building_name": "",
    "dong": "",
    "ho": "",
    "area_m2": ""
  }},
  "owners": [
    {{ "name": "", "ownership_type": "단독/공동", "share": "" }}
  ],
  "ownership_changes": [
    {{ "date": "", "reason": "", "details": "" }}
  ],
  "rights": [
    {{ "section": "갑구/을구", "right_type": "", "holder": "", "receipt_date": "", "registration_date": "", "amount": "", "details": "" }}
  ]
}}"""


def extract_structured(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return _fallback_structured(text)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        user_content = STRUCT_USER_TEMPLATE.format(ocr_text=text)
        resp = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": STRUCT_SYSTEM},
                {"role": "user", "content": user_content},
            ],
            max_tokens=4096,
        )
        raw = (resp.choices[0].message.content or "").strip()
        return _parse_json_from_response(raw) or _fallback_structured(text)
    except Exception:
        return _fallback_structured(text)


def _parse_json_from_response(raw: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return None


def _fallback_structured(text: str) -> Dict[str, Any]:
    from parser import parse_registry_text
    return parse_registry_text(text)
