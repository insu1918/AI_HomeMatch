# parser.py - 등기부 텍스트 파싱 (소재지, 소유자 등)
from __future__ import annotations
import re
from typing import Any, Dict, List


_KOREAN_NAME_RE = re.compile(r"^[가-힣·]{2,10}$")


def _parse_date(text: str) -> str | None:
    """
    날짜 파싱:
    - 2022.03.15 / 2022-03-15 / 2022/03/15
    - 2014년4월28일 (OCR 오타로 '원'이 섞이는 경우도 일부 허용)
    """
    m = re.search(r"(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})", text)
    if m:
        y, mo, d = m.group(1), int(m.group(2)), int(m.group(3))
        return f"{y}-{mo:02d}-{d:02d}"

    m = re.search(r"(\d{4})\s*년\s*(\d{1,2})\s*(?:월|원)\s*(\d{1,2})\s*일", text)
    if m:
        y, mo, d = m.group(1), int(m.group(2)), int(m.group(3))
        return f"{y}-{mo:02d}-{d:02d}"

    return None


def _extract_owner_names(line: str) -> List[str]:
    """
    한 줄에 '소유자'가 여러 번 나오는 경우를 처리.
    예: "... 소유자 신중희 ... 소유자 이의자 ..."
    """
    names: List[str] = []
    for m in re.finditer(r"소유자\s*[:：]?\s*([^\s\d]{2,20})", line):
        candidate = (m.group(1) or "").strip()
        # '외', '및', 괄호 등 잡음 제거 (첫 토큰 우선)
        candidate = re.split(r"[()\[\],]|외|및", candidate)[0].strip()
        if candidate and _KOREAN_NAME_RE.match(candidate):
            names.append(candidate)
    # 중복 제거(순서 유지)
    out: List[str] = []
    seen = set()
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def parse_registry_text(text: str) -> Dict[str, Any]:
    """OCR 텍스트에서 기본 정보 추출."""
    if not text or not text.strip():
        return _empty_parsed()

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    out: Dict[str, Any] = {
        "property_info": {
            "address": None,
            "building_name": None,
            "dong": None,
            "ho": None,
            "area_m2": None,
        },
        "owners": [],
        "ownership_changes": [],
        "rights": [],
    }

    for line in lines:
        # 1) 소재지 / 주소 (가능한 한 주소 부분만 잘라내기)
        if out["property_info"]["address"] is None:
            # (1) 도로명주소가 있으면 우선 사용
            if "도로명주소" in line or "[도로명주소]" in line:
                # 예: "[도로명주소] ... 장다리로 306번길 35 ..."
                m = re.search(r"(?:도로명주소\]?\s*)(.+)", line)
                if m:
                    addr_part = m.group(1).strip()
                    # 층/면적/대지권 등 뒤는 잘라냄
                    addr_part = re.split(r"(면적|대지권|표시번호|\d+\s*층)", addr_part)[0].strip()
                    if addr_part:
                        out["property_info"]["address"] = addr_part

            # (2) 일반 '소재지' / '주소' (단, '소재지번' 같은 헤더는 제외)
            if out["property_info"]["address"] is None and ("소재지" in line or "주소" in line):
                m = re.search(r"(소재지(?!번)|주소)\s*[:：]?\s*(.+)", line)
                if m:
                    addr_part = m.group(2)
                    addr_part = re.split(r"(건물명|면적|갑구|을구)", addr_part)[0].strip()
                    out["property_info"]["address"] = addr_part or None

        # 2) 건물명
        if "건물명" in line and out["property_info"]["building_name"] is None:
            m = re.search(r"건물명\s*[:：]?\s*(.+)", line)
            if m:
                name_part = m.group(1)
                # 뒤에 동/호 정보가 같이 붙어 있는 경우 잘라내기
                name_part = re.split(r"\d+\s*동|\d+\s*호|면적|㎡", name_part)[0].strip()
                out["property_info"]["building_name"] = name_part or None

        # 3) 면적
        if "면적" in line and out["property_info"]["area_m2"] is None:
            m = re.search(r"(\d+\.?\d*)\s*㎡", line)
            if m:
                out["property_info"]["area_m2"] = m.group(1) + " ㎡"

        # 4) 동/호 (건물명 라인 등에서 함께 추출)
        # 소유자/권리자/채무자 주소에서 동호를 잘못 잡는 경우가 많아서 제외
        if (
            ("동" in line and "호" in line)
            and out["property_info"]["dong"] is None
            and ("소유자" not in line and "채무자" not in line and "권리자" not in line)
        ):
            dong_ho = re.search(r"(\d+)\s*동\s*(\d+)\s*호", line)
            if dong_ho:
                out["property_info"]["dong"] = dong_ho.group(1)
                out["property_info"]["ho"] = dong_ho.group(2)

        # 집합건물의 "제303호" 같은 패턴(동 없이 호만 있는 케이스)
        if out["property_info"]["ho"] is None:
            m = re.search(r"제\s*(\d+)\s*호", line)
            if m and ("[집합건물]" in line or "전유" in line or "표제부" in line or "건물" in line):
                out["property_info"]["ho"] = m.group(1)

        # 5) 소유자 정보
        if "소유자" in line:
            # 한 줄에 여러 번 등장할 수 있으므로 모두 추출
            for name in _extract_owner_names(line):
                out["owners"].append(
                    {
                        "name": name,
                        "ownership_type": "단독",
                        "share": None,
                    }
                )

        # 6) 소유권 이전 이력
        if "소유권" in line and "이전" in line:
            # '소유권이전'이 여러 번 나올 수 있어, 키워드 이후에서 날짜를 찾음
            for m in re.finditer(r"소유권\s*이전", line):
                tail = line[m.end() : m.end() + 80]  # 키워드 이후 일부만 스캔
                parsed_date = _parse_date(tail)
                out["ownership_changes"].append(
                    {
                        "date": parsed_date,
                        "reason": "소유권이전",
                        "details": line,
                    }
                )

        # 7) 권리(을구) 정보
        if "근저당" in line or "저당권" in line or "전세권" in line:
            out["rights"].append(
                {
                    "section": "을구",
                    "right_type": line[:80],
                    "details": line,
                }
            )

    return out


def _empty_parsed() -> Dict[str, Any]:
    return {
        "property_info": {"address": None, "building_name": None, "dong": None, "ho": None, "area_m2": None},
        "owners": [],
        "ownership_changes": [],
        "rights": [],
    }


def split_registry_sections(text: str) -> Dict[str, str]:
    """키워드 기반 표제부/갑구/을구 분리."""
    if not text or not text.strip():
        return {"pyojebu": "", "gapgu": "", "eulgu": ""}
    lines = text.splitlines()
    pyojebu: List[str] = []
    gapgu: List[str] = []
    eulgu: List[str] = []
    current = "pyojebu"
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if "표제부" in stripped:
            current = "pyojebu"
            pyojebu.append(stripped)
        elif "갑구" in stripped:
            current = "gapgu"
            gapgu.append(stripped)
        elif "을구" in stripped:
            current = "eulgu"
            eulgu.append(stripped)
        else:
            if current == "pyojebu":
                pyojebu.append(stripped)
            elif current == "gapgu":
                gapgu.append(stripped)
            else:
                eulgu.append(stripped)
    return {
        "pyojebu": "\n".join(pyojebu) if pyojebu else text[:2000],
        "gapgu": "\n".join(gapgu) if gapgu else "",
        "eulgu": "\n".join(eulgu) if eulgu else "",
    }
