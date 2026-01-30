# 등기부등본 분석 API (Deed Service)

등기부등본 이미지/PDF 업로드 → OCR → 영역 분리(표제부/갑구/을구) → 위험 신호 분석을 제공하는 FastAPI 서비스입니다.

## 실행 방법

1. 가상환경 생성 및 패키지 설치 (선택: OCR 사용 시)

```bash
cd deed-service
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

2. 서버 실행 (기본 포트 8001)

```bash
python main.py
# 또는
uvicorn main:app --host 0.0.0.0 --port 8001
```

3. 프론트엔드에서 사용

- 기본: `http://localhost:8001` (DeedAnalysisPage에서 `VITE_DEED_API_URL` 미설정 시)
- 다른 주소 사용 시: `.env`에 `VITE_DEED_API_URL=http://...` 설정 후 빌드

## API 요약

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/upload` | 이미지/PDF 업로드 → OCR, sections, parsed_data 반환 |
| GET | `/documents/{id}` | 문서 조회 |
| POST | `/documents/{id}/sections` | 표제부/갑구/을구 텍스트 수정 후 저장 |
| POST | `/documents/{id}/llm-structure` | LLM으로 JSON 구조화 추출 |
| POST | `/documents/{id}/risk-analysis` | 위험 신호 생성 + LLM 설명 |
| GET | `/health` | 헬스체크 |

## OCR / LLM

- **OCR**: EasyOCR 미설치 시 샘플 텍스트 반환. 실제 OCR 사용 시 `pip install easyocr` 필요.
- **위험 분석 설명**: `OPENAI_API_KEY` 설정 시 GPT로 쉬운 설명 생성. 미설정 시 위험 신호 목록만 반환.

## CORS

프론트엔드(localhost:5173 등)에서 호출할 수 있도록 CORS는 `allow_origins=["*"]`로 열어 두었습니다.
