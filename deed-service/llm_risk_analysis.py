# llm_risk_analysis.py - 위험 신호 생성 + LLM 설명
from __future__ import annotations
import os
from typing import Any, Dict, List, Optional

RISK_SYSTEM = """당신은 부동산 등기부 정보를 사용자에게 쉽게 설명하는 안내 AI입니다.
중요 원칙: 법적 판단을 하지 마십시오. "안전하다", "문제 없다" 같은 표현 금지.
"가능성", "주의 필요", "확인 필요" 수준의 안내만 제공.
어려운 법률 용어를 사용하지 말고, 중학생도 이해할 수 있는 쉬운 말로 설명하세요.
각 항목은: 1) 한 줄 요약 2) 무슨 뜻인지 쉬운 설명 3) 왜 주의해야 하는지 4) 추가로 확인하면 좋은 것."""

RISK_USER_TEMPLATE = """다음은 등기부 분석 시스템이 탐지한 위험 신호 목록입니다.

부동산 정보:
- 주소: {address}
- 건물명: {building_name}
- 동/호수: {dong}동 {ho}호

탐지된 위험 신호:
{risk_flags}

각 항목에 대해 쉬운 말로 설명해주세요. 법적 결론은 하지 마세요."""


def build_risk_flags(structured: Dict[str, Any]) -> List[str]:
    """구조화 데이터에서 위험 신호 리스트 생성 (6가지 확인 항목 반영)."""
    flags: List[str] = []
    prop = structured.get("property_info") or {}
    owners = structured.get("owners") or []
    rights = structured.get("rights") or []
    changes = structured.get("ownership_changes") or []

    # 소유자 2명 이상 = 무조건 공동소유가 아님 (소유권 이전으로 과거/현재 소유자가 함께 잡힐 수 있음)
    owner_names = [o.get("name") for o in owners if o.get("name")]
    owner_names_unique: List[str] = []
    seen = set()
    for n in owner_names:
        if n not in seen:
            seen.add(n)
            owner_names_unique.append(n)

    has_explicit_joint = any((o.get("ownership_type") or "").strip() == "공동" for o in owners)
    has_share = any(o.get("share") for o in owners)

    if (has_explicit_joint or has_share) and len(owner_names_unique) >= 2:
        flags.append("여러 명이 함께 소유하는 것으로 보입니다(공동 소유 가능성).")
    elif len(owner_names_unique) >= 2 and changes:
        flags.append("소유자가 변경된 기록이 있습니다(이전/현재 소유자가 함께 추출될 수 있음).")
    if len(rights) > 0:
        flags.append(f"등기부에 {len(rights)}건의 권리(근저당·전세권 등)가 등재되어 있습니다.")
    if changes:
        flags.append("소유권 이전 이력이 있습니다. 시점 확인이 필요할 수 있습니다.")
    if not (prop.get("address") or prop.get("dong") or prop.get("ho")):
        flags.append("주소·동호 정보가 추출되지 않았습니다. 목적물 특정 확인이 필요합니다.")
    if not flags:
        flags.append("추출된 정보 기준으로 특별한 위험 신호는 없습니다. 전문가 확인을 권장합니다.")
    return flags


def explain_risk(
    structured: Dict[str, Any],
    risk_flags: List[str],
    api_key: Optional[str] = None,
) -> str:
    """위험 신호를 LLM으로 쉬운 설명 문장으로 변환."""
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    prop = structured.get("property_info") or {}
    address = prop.get("address") or "(미추출)"
    building_name = prop.get("building_name") or "(미추출)"
    dong = prop.get("dong") or "(미추출)"
    ho = prop.get("ho") or "(미추출)"
    risk_text = "\n".join(f"{i+1}. {f}" for i, f in enumerate(risk_flags))
    user_content = RISK_USER_TEMPLATE.format(
        address=address,
        building_name=building_name,
        dong=dong,
        ho=ho,
        risk_flags=risk_text,
    )
    if not api_key:
        return _fallback_explanation(risk_flags)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": RISK_SYSTEM},
                {"role": "user", "content": user_content},
            ],
            max_tokens=2048,
        )
        return (resp.choices[0].message.content or "").strip() or _fallback_explanation(risk_flags)
    except Exception:
        return _fallback_explanation(risk_flags)


def _fallback_explanation(risk_flags: List[str]) -> str:
    return "\n\n".join(f"{i+1}. {f}\n   (추가 확인을 권장합니다.)" for i, f in enumerate(risk_flags))


def build_check_items(structured: Dict[str, Any]) -> List[Dict[str, Any]]:
    """6가지 확인 항목별로 답변 생성."""
    prop = structured.get("property_info") or {}
    owners = structured.get("owners") or []
    rights = structured.get("rights") or []
    changes = structured.get("ownership_changes") or []
    
    items = []
    
    # 1. 이 사람이 진짜 주인인가? (소유자 일치 여부)
    owner_names = [o.get("name", "").strip() for o in owners if o.get("name")]
    # 중복 제거(순서 유지)
    owner_names_unique: List[str] = []
    seen = set()
    for n in owner_names:
        if n and n not in seen:
            seen.add(n)
            owner_names_unique.append(n)

    if owner_names_unique:
        current_owner = owner_names_unique[-1]
        previous_owners = owner_names_unique[:-1]
        if previous_owners:
            items.append({
                "status": "caution",
                "summary": f"현재 소유자로 보이는 이름: {current_owner}. 이전 소유자 이름도 함께 추출되었습니다: {', '.join(previous_owners)}. 계약 상대방 이름이 현재 소유자와 같은지 확인하세요. (신원 진위는 등기부만으로는 확인 불가)"
            })
        else:
            items.append({
                "status": "ok",
                "summary": f"등기부상 소유자: {current_owner}. 계약 상대방 이름과 일치 여부를 직접 확인하세요. (신원 진위는 등기부만으로는 확인 불가)"
            })
    else:
        items.append({
            "status": "pending",
            "summary": "소유자 정보가 추출되지 않았습니다. 등기부등본을 다시 확인하거나 전문가 상담을 권장합니다."
        })
    
    # 2. 보증금보다 먼저 가져갈 권리가 있는가? (근저당·가압류 등)
    if len(rights) > 0:
        right_types = [r.get("right_type", "").strip()[:30] for r in rights if r.get("right_type")]
        items.append({
            "status": "caution",
            "summary": f"등기부에 {len(rights)}건의 권리(근저당·전세권 등)가 등재되어 있습니다. 보증금보다 우선 변제받을 수 있는 권리가 있을 수 있으니, 권리 설정 시점과 금액을 확인하세요."
        })
    else:
        items.append({
            "status": "ok",
            "summary": "등기부에 선순위 담보권(근저당·가압류 등)이 등재되어 있지 않습니다. 다만 실제 계약일과 권리 설정일의 순서를 확인하는 것이 중요합니다."
        })
    
    # 3. 이 집, 왜 이렇게 최근에 손바뀜 됐지? (소유권 이전 시점)
    if changes:
        recent = [c for c in changes if c.get("date")]
        if recent:
            latest_date = recent[0].get("date", "")
            items.append({
                "status": "caution",
                "summary": f"소유권 이전 이력이 있습니다. 최근 이전일: {latest_date}. 최근 손바뀜이 있었다면 그 이유(증여·매매·경매 등)를 확인하는 것이 좋습니다."
            })
        else:
            items.append({
                "status": "ok",
                "summary": "소유권 이전 이력이 있지만 구체적인 날짜가 추출되지 않았습니다. 등기부등본에서 직접 확인하세요."
            })
    else:
        items.append({
            "status": "ok",
            "summary": "최근 소유권 이전 이력이 추출되지 않았습니다. 등기부등본에서 직접 확인하거나 전문가 상담을 권장합니다."
        })
    
    # 4. 나 말고 계약 권한 있는 사람이 또 있나? (공동 소유 여부)
    has_explicit_joint = any((o.get("ownership_type") or "").strip() == "공동" for o in owners)
    has_share = any(o.get("share") for o in owners)

    if has_explicit_joint or has_share:
        items.append({
            "status": "caution",
            "summary": "여러 명이 함께 소유(공동 소유)하는 것으로 보입니다. 계약 전에 모든 소유자가 동의/서명하는지 확인하는 것이 좋습니다."
        })
    elif len(owner_names_unique) >= 2 and changes:
        items.append({
            "status": "ok",
            "summary": "소유자 이름이 2명 이상 추출되었지만, 이는 소유권 이전(과거/현재 소유자) 때문일 수 있습니다. 공동 소유로 단정할 수 없으니 등기부에서 '지분/공유' 표기를 확인하세요."
        })
    else:
        items.append({
            "status": "ok",
            "summary": "단독 소유로 보입니다. 공동 소유자 동의 없이 계약한 위험은 낮아 보입니다. 다만 등기부등본에서 직접 확인하세요."
        })
    
    # 5. 내 보증금은 몇 번째 순서인가? (선순위 권리 구조)
    if len(rights) > 0:
        items.append({
            "status": "caution",
            "summary": f"등기부에 {len(rights)}건의 권리가 등재되어 있습니다. 보증금보다 먼저 변제받을 권리(근저당·전세권 등)가 있을 수 있으니, 권리 설정 순서와 금액을 확인하세요. 실제 배당 순위는 법원 경매 시 확정됩니다."
        })
    else:
        items.append({
            "status": "ok",
            "summary": "등기부에 선순위 권리가 등재되어 있지 않습니다. 다만 확정일자·대항력 등도 보증금 회수에 영향을 줄 수 있으니 전문가 상담을 권장합니다."
        })
    
    # 6. 이 계약, 법적으로 특정이 되는가? (호실·목적물 특정)
    address = prop.get("address") or ""
    dong = prop.get("dong") or ""
    ho = prop.get("ho") or ""
    if address or (dong and ho):
        addr_str = address or f"{dong}동 {ho}호"
        items.append({
            "status": "ok",
            "summary": f"등기부상 주소·동호: {addr_str}. 계약서상 주소·동호와 일치하는지 확인하세요. 일치하면 목적물 특정이 가능합니다."
        })
    else:
        items.append({
            "status": "pending",
            "summary": "주소·동호 정보가 추출되지 않았습니다. 등기부등본에서 직접 확인하거나 전문가 상담을 권장합니다."
        })
    
    return items
