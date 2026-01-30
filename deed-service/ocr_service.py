# ocr_service.py - OCR 텍스트 추출 (EasyOCR 우선, 없으면 샘플)
from __future__ import annotations
import io
from typing import Optional, Tuple

from real_estate_terms import correct_with_vocab


def extract_text(image_bytes: bytes, preprocess: str = "none", use_llm_correction: bool = False) -> str:
    """이미지 바이트에서 텍스트 추출. preprocess: none|doc|light|full."""
    raw = _run_ocr(image_bytes, preprocess)
    return correct_with_vocab(raw) if raw else ""


def _run_ocr(image_bytes: bytes, preprocess: str) -> str:
    """EasyOCR 기반 OCR. 오류는 콘솔에 상세 로그를 남기고 빈 문자열을 반환."""
    try:
        from PIL import Image
        # Pillow 10+ 에서 ANTIALIAS 제거 → EasyOCR 내부에서 참조함
        if not hasattr(Image, "ANTIALIAS"):
            try:
                # Pillow 10 이상에서의 대체 상수
                Image.ANTIALIAS = Image.Resampling.LANCZOS  # type: ignore[attr-defined]
                print("[OCR] Pillow ANTIALIAS → Resampling.LANCZOS로 패치")
            except Exception:
                print("[OCR] Pillow ANTIALIAS 패치 실패")
        import easyocr
        import numpy as np
        print("[OCR] easyocr / Pillow / numpy import OK")
    except ImportError as e:
        print("[OCR] ImportError - easyocr/Pillow/numpy 중 하나가 없습니다:", repr(e))
        return ""

    try:
        # TODO: preprocess 값에 따라 전처리 추가 가능
        reader = easyocr.Reader(["ko", "en"], gpu=False)
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        arr = np.array(img)
        results = reader.readtext(arr)
        print(f"[OCR] readtext 결과 개수: {len(results)}")
        lines = [item[1] for item in results]
        if not lines:
            print("[OCR] 경고: 인식된 텍스트가 없습니다.")
        return "\n".join(lines) if lines else ""
    except Exception as e:
        print("[OCR] 실행 중 예외 발생:", repr(e))
        return ""


def get_detection_regions(
    image_bytes: bytes, preprocess: str = "none"
) -> Tuple[list, Optional[bytes]]:
    """OCR 영역(bbox, text, confidence)과 사용한 이미지 바이트 반환."""
    try:
        from PIL import Image
        if not hasattr(Image, "ANTIALIAS"):
            try:
                Image.ANTIALIAS = Image.Resampling.LANCZOS  # type: ignore[attr-defined]
                print("[OCR] (regions) Pillow ANTIALIAS → Resampling.LANCZOS로 패치")
            except Exception:
                print("[OCR] (regions) Pillow ANTIALIAS 패치 실패")
        import easyocr
        import numpy as np
    except ImportError as e:
        print("[OCR] ImportError(get_detection_regions) - easyocr/Pillow/numpy 없음:", repr(e))
        return [], None

    try:
        reader = easyocr.Reader(["ko", "en"], gpu=False)
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        arr = np.array(img)
        results = reader.readtext(arr)
        regions = []
        for (bbox, text, conf) in results:
            # bbox 안에 numpy.int32 등이 섞여 있어 FastAPI JSON 직렬화 시 에러가 날 수 있으므로
            # 모두 파이썬 float로 변환
            converted_bbox = [
                [float(coord) for coord in point] for point in bbox  # type: ignore[assignment]
            ]
            regions.append(
                {
                    "bbox": converted_bbox,
                    "text": correct_with_vocab(text),
                    "confidence": round(float(conf), 4),
                }
            )
        print(f"[OCR] 영역 검출 개수: {len(regions)}")
        return regions, image_bytes
    except Exception as e:
        print("[OCR] get_detection_regions 예외:", repr(e))
        return [], image_bytes
