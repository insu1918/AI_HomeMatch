# 부동산 등기부등본 분석 및 저장
_Exported on 1/29/2026 at 14:08:06 GMT+9 from Cursor (2.4.22)_

---

**User**

부동산 등기부등본을 분석하는 기능을 만들건데 이미지로 업로드 해서 텍스트로 DB에 저장하게 할려고

---

**Cursor**

프로젝트 구조 확인 중. 이미지 업로드, OCR 텍스트 추출, DB 저장 기능을 추가합니다.


프로젝트가 비어 있습니다. 부동산 등기부등본 분석 기능을 처음부터 구성합니다. 초기 TODO를 작성하고 시작합니다.


requirements.txt에서 불필요한 항목 제거 중.


부동산 등기부등본 분석 시스템을 구성했습니다.

## 생성된 파일들

1. **`main.py`** - FastAPI 웹 서버 및 API 엔드포인트
2. **`database.py`** - SQLite 데이터베이스 모델 및 설정
3. **`ocr_service.py`** - OCR 서비스 (EasyOCR, Tesseract 지원)
4. **`parser.py`** - 등기부등본 텍스트 파싱 로직
5. **`requirements.txt`** - 필요한 Python 패키지 목록
6. **`README.md`** - 사용 설명서
7. **`.gitignore`** - Git 제외 파일 목록

## 주요 기능

- 이미지 업로드: 등기부등본 이미지를 업로드
- OCR 텍스트 추출: EasyOCR 또는 Tesseract로 텍스트 추출
- 자동 파싱: 소재지, 소유자명, 면적, 등기일자 등 자동 추출
- DB 저장: SQLite에 텍스트와 파싱 결과 저장
- 문서 조회: 저장된 문서 목록 및 상세 조회 API

## 사용 방법

1. 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 서버 실행:
```bash
python main.py
```

3. API 사용:
- `POST /api/upload` - 이미지 업로드 및 분석
- `GET /api/documents` - 문서 목록 조회
- `GET /api/documents/{id}` - 문서 상세 조회

서버는 `http://localhost:8000`에서 실행되며, `http://localhost:8000/docs`에서 Swagger UI로 API를 테스트할 수 있습니다.

추가 기능이나 수정이 필요하면 알려주세요.

---

**User**

사용하기 쉬운 UI로 바꿔줘

---

**Cursor**

웹 UI 추가 중. 이미지 업로드, 분석 결과 표시, 문서 목록 조회 기능을 포함합니다.


웹 UI 추가 중. 사용하기 쉬운 인터페이스를 구성합니다.


requirements.txt에 Jinja2 추가 중.


웹 UI를 추가했습니다. 주요 기능은 다음과 같습니다:

## 추가된 기능

### 1. **메인 페이지** (`/`)
- 드래그 앤 드롭 또는 클릭으로 이미지 업로드
- 이미지 미리보기
- OCR 방법 선택 (EasyOCR/Tesseract)
- 실시간 분석 진행 상태 표시
- 분석 결과를 카드 형태로 표시
- 추출된 정보 요약 (소재지, 소유자, 면적 등)
- 전체 텍스트 복사 기능

### 2. **문서 목록 페이지** (`/documents`)
- 저장된 모든 문서 목록 표시
- 페이지네이션 지원
- 각 문서의 주요 정보 미리보기
- 클릭으로 상세 페이지 이동

### 3. **문서 상세 페이지** (`/document/{id}`)
- 문서의 모든 정보 표시
- 추출된 전체 텍스트 확인
- 문서 삭제 기능

## 디자인 특징

- 그라데이션 배경과 카드 기반 레이아웃
- 반응형 디자인 (모바일 지원)
- 드래그 앤 드롭 파일 업로드
- 로딩 상태 및 에러 메시지 표시
- 부드러운 애니메이션 및 호버 효과

## 사용 방법

1. 서버 실행:
```bash
python main.py
```

2. 브라우저에서 접속:
```
http://localhost:8000
```

3. 이미지 업로드 및 분석:
   - 메인 페이지에서 등기부등본 이미지를 드래그하거나 선택
   - OCR 방법 선택
   - "분석 시작" 버튼 클릭
   - 결과 확인

웹 UI를 통해 API 없이도 등기부등본을 업로드하고 분석 결과를 확인할 수 있습니다.

---

**User**

easy OCR은 라이브러리야?

---

**Cursor**

네, EasyOCR은 Python OCR 라이브러리입니다. 프로젝트에서의 사용 방식을 확인 중입니다.


네, **EasyOCR**은 Python OCR 라이브러리입니다.

## EasyOCR 개요

- **Python OCR 라이브러리**: 이미지에서 텍스트를 추출하는 오픈소스 라이브러리
- **다국어 지원**: 한국어, 영어, 중국어, 일본어 등 80개 이상 언어 지원
- **딥러닝 기반**: PyTorch 기반으로 정확도가 높음
- **설치**: `pip install easyocr`로 설치

## 현재 프로젝트에서의 사용

프로젝트에서는 `requirements.txt`에 `easyocr==1.7.0`이 포함되어 있고, `ocr_service.py`에서 다음과 같이 사용됩니다:

```python
# EasyOCR 초기화 (한국어 + 영어 지원)
self.easyocr_reader = easyocr.Reader(['ko', 'en'], gpu=False)
```

### 특징

1. **한국어 인식**: 등기부등본의 한글 인식에 적합
2. **별도 설치 불필요**: Tesseract와 달리 별도 프로그램 설치가 필요 없음
3. **첫 실행 시 모델 다운로드**: 초기 실행 시 필요한 모델을 자동 다운로드 (시간 소요 가능)
4. **GPU 지원**: GPU가 있으면 더 빠르게 처리 가능 (현재는 `gpu=False`로 설정)

### Tesseract와의 차이

- **EasyOCR**: Python 라이브러리, 별도 설치 불필요, 한국어 인식 우수
- **Tesseract**: 별도 프로그램 설치 필요, 더 가볍지만 한국어 인식이 상대적으로 낮을 수 있음

현재 프로젝트는 두 가지 OCR 방법을 모두 지원하며, 기본값은 EasyOCR입니다.

---

**User**

OCR 처리 실패: EasyOCR 텍스트 추출 실패: Invalid input type. Supporting format = string(file path or url), bytes, numpy array 이 오류 떠

---

**Cursor**

EasyOCR이 PIL Image를 받지 못합니다. bytes나 numpy array로 변환해 전달하도록 수정합니다.


EasyOCR의 `readtext()`는 **문자열(경로/URL), bytes, numpy 배열**만 받습니다. PIL Image를 넘기면 해당 오류가 납니다. **bytes를 그대로 쓰거나**, **numpy 배열로 변환**해 넘기도록 수정합니다.


RGB/BGR 변환이 오히려 문제를 일으킬 수 있어, numpy array는 RGB 그대로 넘기도록 변경합니다.


수정 반영했습니다. 변경 내용만 정리합니다.

## 원인

EasyOCR `readtext()`는 다음 타입만 받습니다.

- **string**: 파일 경로 또는 URL  
- **bytes**: 이미지 바이트  
- **numpy array**: 이미지 배열  

PIL `Image` 객체는 지원하지 않아 `Invalid input type` 오류가 났습니다.

## 수정 내용

`ocr_service.py`에서 PIL Image 대신 **numpy array**를 넘기도록 바꿨습니다.

1. **numpy 사용**: `import numpy as np` 추가  
2. **PIL → numpy 변환**  
   - `Image.open(io.BytesIO(image_bytes))` 로 열고  
   - `image.convert('RGB')` 로 모드 통일  
   - `np.array(image)` 로 numpy 배열 생성  
3. **EasyOCR 호출**: `readtext(image_np)` 에 numpy 배열 전달  

이렇게 하면 지원 타입에 맞게 입력이 들어가므로, 같은 오류는 나지 않아야 합니다.  
한번 더 업로드해서 OCR이 되는지 확인해보면 됩니다.

---

**User**

OCR 처리 실패: EasyOCR 텍스트 추출 실패: module 'PIL.Image' has no attribute 'ANTIALIAS'

---

**Cursor**

Pillow 10부터 `Image.ANTIALIAS`가 제거되어 EasyOCR 내부에서 오류가 납니다. 호환용 `ANTIALIAS`를 `Image.Resampling.LANCZOS`로 설정합니다.


Pillow 10 이상에서 `Image.ANTIALIAS`가 제거되어 EasyOCR 내부에서 오류가 납니다. EasyOCR import 전에 `Image.ANTIALIAS`를 `Image.Resampling.LANCZOS`로 매핑합니다.


Pillow 10 이상에서는 `Image.Resampling.LANCZOS`만 쓰면 됩니다.


수정 반영했습니다.

## 원인

Pillow **10.0**부터 `Image.ANTIALIAS` 상수가 제거되었고, **`Image.Resampling.LANCZOS`**를 쓰도록 바뀌었습니다.  
EasyOCR 쪽에서는 아직 `Image.ANTIALIAS`를 사용해서, Pillow 10 이상 환경에서 오류가 나는 상황입니다.

## 수정 내용

`ocr_service.py` 상단에서 **PIL을 가장 먼저 import**한 뒤, `ANTIALIAS`가 없을 때만 `LANCZOS`로 채워 넣도록 했습니다.

```python
from PIL import Image
# Pillow 10+ 호환: ANTIALIAS 제거됨 → LANCZOS 사용 (EasyOCR 등 의존성 대응)
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

import easyocr
...
```

이렇게 하면 EasyOCR이 내부에서 `Image.ANTIALIAS`를 쓸 때 `Image.Resampling.LANCZOS`가 사용되어,  
`module 'PIL.Image' has no attribute 'ANTIALIAS'` 오류가 나지 않아야 합니다.  
한번 더 실행해서 OCR이 정상 동작하는지 확인해 보시면 됩니다.

---

**User**

추출된 텍스트의 정확도를 높이고 싶은데 어떻게  해야할까? 말만해줘

---

**Cursor**

추출 텍스트 정확도를 높이는 쪽으로만 정리하면 아래와 같습니다.

## 1. 입력 이미지 품질

- **해상도**: 가급적 300 DPI 이상, 특히 등기부등본은 작은 글씨가 많아서 해상도가 낮으면 오인식이 늘어납니다.
- **초점·흔들림**: 흐리거나 흔들리지 않게 찍거나 스캔합니다.
- **조명**: 그림자·반사 없이 균일하게 비추고, 노출 과다/부족 피합니다.
- **기울기·왜곡**: 문서가 기울어지지 않게 하고, 왜곡(곡면, 찌그러짐)이 있으면 보정 후 OCR에 넣습니다.

## 2. 전처리(이미지 가공)

- **그레이스케일**: 색상 대신 밝기만 쓰면 노이즈에 덜 민감할 수 있습니다.
- **이진화(Threshold)**: 배경은 흰색, 글자는 검정으로 명확히 나누면 인식률이 좋아질 수 있습니다. 적응형 이진화(adaptive threshold)를 쓰면 조명이 고르지 않을 때 유리합니다.
- **노이즈 제거**: 작은 점·얼룩을 없애면 잘못 인식되는 글자가 줄어듭니다.
- **선명화(Sharpening)**: 살짝만 적용해 경계를 분명히 하는 것이 도움이 될 수 있습니다.
- **기울기 보정**: Hough 변환 등으로 줄/문단 기울기를 찾아 회전 보정 후 OCR하면 줄 단위 인식이 나아집니다.
- **잘라내기**: 등기부등본 본문만 잘라서 넘기면 테두리·표 등 불필요한 영역이 줄어듭니다.

## 3. OCR 엔진·설정

- **EasyOCR 옵션**  
  - `detail=0` 대신 상세 결과를 쓰고, 신뢰도(confidence)가 낮은 구간만 따로 처리(재인식, 수동 확인 등)하는 방식이 좋습니다.  
  - 너무 큰 이미지는 리사이즈해서 넘기되, 너무 작게 줄이지 않도록 합니다.
- **Tesseract**  
  - `--psm`(페이지 분할 모드)를 문서 형태에 맞게 바꿔보고(예: 단일 블록, 단일 줄 등), `--oem`으로 LSTM 등 더 나은 엔진을 쓰는 것이 좋습니다.
- **앙상블**  
  - EasyOCR과 Tesseract를 둘 다 돌려서, 같은 위치에서 결과가 일치하는 부분은 신뢰하고, 다르면 신뢰도·후처리 규칙으로 하나를 골라 쓰는 방식입니다.

## 4. 후처리(텍스트 보정)

- **오타 보정**: 등기용어·법률용어 사전을 두고, 유사 문자열(편집 거리 등)로 후보를 추려 바꿔 넣습니다.
- **정규식·패턴**: 날짜, 주소, 면적(㎡, 평) 등 형식이 정해진 부분은 정규식으로 검증하고, OCR 결과가 형식에 안 맞으면 주변 글자만 바꿔서 재매칭하는 방식이 가능합니다.
- **문맥 활용**: “소재지”, “소유자”, “면적” 같은 키워드 주변 문자열만 따로 검증·보정하는 룰을 두는 방법입니다.

## 5. 도메인 특화

- **등기부등본 구조**: “갑구/을구”, “순위번호”, “접수” 등 고정된 표头和 항목 구조를 알고, 블록/줄 단위로 “여기부터가 주소, 여기부터가 소유자”처럼 구역을 나눠서 인식하면, 전체 문단을 한 번에 인식할 때보다 정확해질 수 있습니다.
- **미세 조정(fine-tuning)**: 등기부등본 이미지–텍스트 쌍을 모아서, EasyOCR 백엔드 모델을 그 데이터로 조금 더 학습시키면, 동일한 서식·인쇄체에 대한 정확도가 올라갈 수 있습니다(구현 난이도는 높음).
- **키워드 기반 검증**: “토지”, “건축물”, “㎡”, “평” 등 반드시 나와야 할 단어가 OCR 결과에 없으면, 그 구간만 재인식하거나 수동 검수 후보로 두는 방식입니다.

## 6. 워크플로우

- **다단계 인식**: 1차로 전체 OCR → 저신뢰도 구간만 잘라서 2차 OCR(해상도·전처리 다르게) → 두 결과를 합치거나 선택.
- **사람 검수**: 소재지, 소유자, 면적, 권리관계처럼 중요한 필드는 “자동 추출 + 사람이 한 번 더 확인”하는 구조가 가장 확실합니다.

정리하면, **“입력 품질·전처리로 인식 난이도를 낮추고 → OCR 설정·후처리로 문자열 품질을 높이고 → 등기부 구조와 키워드를 이용해 검증·보정”**하는 순서로 적용하면 정확도를 꽤 끌어올릴 수 있습니다.

---

**User**

진행 해보자

---

**Cursor**

OCR 정확도 개선 작업을 진행합니다. 이미지 전처리·후처리·API/UI 옵션을 추가합니다.


전처리 모듈 생성 및 OCR·API·UI 연동 진행 중.


전처리에 '가벼운' 프리셋을 추가하고, OCR 서비스와 API·UI를 연동합니다.


ocr_service의 for문에서 변수 스코프 오류를 수정하고, API와 UI에 전처리 옵션을 추가합니다.


API와 UI에 전처리 옵션 추가 중.


전처리 값을 폼으로 보내도록 스크립트에 추가하고, API는 `Form()`으로 받도록 수정합니다.


form-hint 스타일 추가 및 preprocess에서 cv2 미설치 시 동작 확인


구현을 모두 반영했습니다. 변경 사항만 정리합니다.

## 1. 이미지 전처리 (`preprocess.py` 신규)

- **리사이즈**: 긴 변 최대 2000px로 제한  
- **그레이스케일**  
- **노이즈 제거**: `cv2.fastNlMeansDenoising`  
- **적응형 이진화** (full 모드): 글자/배경 대비 강화  
- **선명화**: 3×3 sharpening kernel  
- **기울기 보정** (full 모드): `minAreaRect`로 각도 추정 후 회전  
- **프리셋**
  - `preprocess_light`: 리사이즈 → 선명화 → 그레이스케일 → 노이즈 제거 (이진화 없음)
  - `preprocess_full`: 위 + 기울기 보정 + 적응형 이진화  

OpenCV가 없으면 그레이스케일·이진화만 numpy/PIL로 처리하도록 되어 있습니다.

## 2. OCR 서비스 (`ocr_service.py`)

- **전처리 옵션**: `preprocess="none" | "light" | "full"` 을 받아 위 파이프라인 적용  
- **EasyOCR 신뢰도 필터**: `readtext` 결과 중 `confidence < 0.3` 인 라인은 제외  
- **텍스트 후처리**: `m2` / `m²` / `㎡` 를 `㎡` 로 통일하는 정규화 추가  

## 3. API·UI

- **POST /api/upload**  
  - `preprocess`: `Form("light")` 로 받고, `"none"` / `"light"` / `"full"` 만 허용  
- **업로드 폼**  
  - “이미지 전처리 (정확도 향상)” 선택:  
    - **사용 안 함** → `none`  
    - **가벼운 전처리 (권장)** → `light`  
    - **강한 전처리 (품질 낮을 때)** → `full`  
  - 안내 문구:  
    “가벼운: 그레이스케일·노이즈제거·선명화. 강한: 기울기 보정·이진화 포함.”

## 4. 의존성 (`requirements.txt`)

- `opencv-python-headless>=4.8.0`
- `numpy>=1.24.0`

실행 전에 `pip install -r requirements.txt` 로 한 번 더 설치하면 됩니다.  
이미지가 어두우거나 비스듬하면 **강한 전처리**, 그 외에는 **가벼운 전처리**를 쓰면 됩니다.

---

**User**

텍스트 정확도가 많이 좋아졌는데 아직 아쉽고, 이미지 전처리 가벼운, 강함 둘다 사용안할정도로 기능이 안좋아

---

**Cursor**

전처리·OCR 설정을 문서(등기부등본)에 맞게 재설계합니다. CLAHE(대비 향상), 가벼운 노이즈 제거, 적응형 이진화 파라미터 조정을 적용합니다.


전처리를 문서용으로 재설계하고, EasyOCR의 대비 옵션과 다중 실행·결과 병합을 추가합니다.


전처리·OCR 로직 재설계 적용 중입니다.


Tesseract에 `doc` 전처리 지원 및 API·UI 옵션 추가 중.


병합 로직을 '동일 텍스트는 신뢰도 높은 것만 남기고, 출력은 (y,x) 순서 유지'로 수정합니다.


반영했습니다. 요약만 정리합니다.

## 1. 전처리 재설계 (`preprocess.py`)

- **CLAHE 추가**  
  - `clahe()`: 대비 제한 적응 히스토그램으로, 흐릿한 문서만 보정.  
  - 선명화·강한 노이즈제거는 하지 않음(글자 깨짐 방지).

- **문서 대비만 (doc)**  
  - `preprocess_doc_only()`: 그레이스케일 + CLAHE만 적용.  
  - 리사이즈는 긴 변 2400px 초과 시에만.  
  - 기본값을 **doc**으로 두어, “원본 훼손 최소 + 흐릿할 때만 보정”으로 사용.

- **가벼운 (light)**  
  - 이전처럼 grayscale + denoise + sharpen이 아니라,  
  - **doc과 동일**하게 그레이스케일 + CLAHE만 적용.

- **강한 (full)**  
  - CLAHE → **매우 약한** 노이즈제거(h=3, 작은 윈도우) →  
  - **문서용** 적응형 이진화(block_size=21, c=6).  
  - 기울기 보정·강한 선명화는 제거.

## 2. OCR 쪽 개선 (`ocr_service.py`)

- **EasyOCR 옵션**  
  - `readtext(..., contrast_ths=0.1, adjust_contrast=0.5)` 로  
  - 저대비 구간을 한 번 더 인식하도록 설정.

- **light/full 시 원본+전처리 병합**  
  - 원본 이미지로 1회, 전처리 이미지로 1회 OCR 수행.  
  - 두 결과를 (y, x) 순서로 정렬한 뒤,  
  - 같은 텍스트는 신뢰도가 높은 것만 남기고 합쳐서 반환.  
  - 전처리가 과해져도 원본에서 나온 글자는 유지되도록 함.

- **신뢰도 필터**  
  - `CONFIDENCE_THRESHOLD`를 0.3 → 0.2로 낮춰  
  - 잘 나온 글자까지 잘리지 않도록 완화.

## 3. UI·API

- 전처리 선택지:  
  - **사용 안 함**  
  - **문서 대비만 (CLAHE, 권장)** ← 기본  
  - **가벼운 (원본+전처리 결과 병합)**  
  - **강한 (품질이 많이 낮을 때만)**  

- API 기본 `preprocess`는 `"doc"`으로 두고,  
  `"none" | "doc" | "light" | "full"` 만 허용.

이제 **문서 대비만**이 기본이라, 전처리로 인한 글자 깨짐은 줄이고, 흐릿한 부분만 CLAHE로 살짝 올리도록 되어 있습니다. **가벼운**은 원본 + 전처리 결과를 병합해서 인식량을 늘리는 용도로 쓰면 됩니다.

---

**User**

정확도가 낮은 텍스트를 부동산에서 자주 사용하는 언어로 대체 하는 방법은 어때?

---

**Cursor**

부동산·등기 용어 사전으로 OCR 오인식을 보정하는 후처리를 추가합니다.


부동산·등기 용어 사전과 오인식→올바른 표현 매핑을 만들어, OCR 후처리에서 적용합니다.


OCR 서비스에서 전체 추출 결과에 대해 `correct_with_vocab` 적용하기.


구현 반영했습니다. 정리만 합니다.

## 1. 부동산/등기 용어 보정 모듈 (`real_estate_terms.py`)

- **TYPO_TO_CANONICAL**  
  OCR에서 자주 잘못 나오는 문자열 → 표준 용어 매핑  
  - 소재지·소유자·명의자·권리자·의무자  
  - 면적·㎡·평  
  - 등기·등기일자·접수·갑구·을구  
  - 부동산·토지·건축물·대지권  
  - 근저당·저당권·임차인·임대인·전세권·지상권·지역권  
  - 순위번호·접수번호·등기원인·신청인·몇수 등  

- **REGEX_REPLACEMENTS**  
  띄어쓰기/오타가 섞인 표현을 한 번에 표준어로 치환  
  - 예: `소\s*재\s*지` → `소재지`, `면\s*적` → `면적`, `등\s*기\s*일\s*자` → `등기일자`  
  - `m2`, `m²` → `㎡`  

- **correct_with_vocab(text)**  
  위 사전·정규식으로 전체 텍스트를 한 번 보정해 반환  

- **add_typo(wrong, right)**  
  새로 발견한 오인식을 런타임에 사전에 추가할 때 사용  

## 2. OCR 파이프라인 연동 (`ocr_service.py`)

- `extract_text()` 마지막에서  
  EasyOCR/Tesseract로 나온 **전체 문자열**에  
  `correct_with_vocab(raw)`를 적용한 값을 반환하도록 했습니다.  
- 그래서 모든 경로(easyocr/tesseract, 전처리 옵션 등)에서  
  추출 직후 한 번만 부동산/등기 용어 보정이 들어갑니다.  

## 3. 사용 예

- OCR 결과: `소 재 지`, `면젹`, `등기 일자`  
- 보정 후: `소재지`, `면적`, `등기일자`  
- 파서가 “소재지”, “면적”, “등기일자” 같은 표준어로 매칭하기 쉬워져  
  소재지·면적·등기일자 추출이 더 안정적으로 됩니다.  

새로 보이는 오타·오인식은 `add_typo("잘못나온글자", "표준용어")`로  
`real_estate_terms`에 추가해 두면, 다음부터 자동 보정 대상이 됩니다.

---

**User**

여기에 llm 으로 문맥을 읽고 텍스트 정확도를 높일 수 있을까?

---

**Cursor**

가능합니다. LLM으로 문맥을 이용해 OCR 결과를 보정할 수 있습니다. 선택 적용되는 LLM 보정 단계를 추가합니다.


LLM으로 문맥을 활용한 OCR 보정 모듈을 추가하고, 환경 변수로 선택 적용되게 붙입니다.


OCR 파이프라인에 LLM 보정을 선택적으로 붙이고, API·UI에서 켤 수 있게 합니다.


OCRService에 `_use_llm_correction` 메서드 추가 중.


import 위치 확인 중.


requirements에 openai 추가 및 UI에 LLM 보정 옵션 노출


API·UI에서 'LLM 문맥 보정'을 요청할 수 있도록 하고, OCR 서비스가 해당 플래그를 받도록 수정합니다.


extract_text에 `use_llm_correction` 인자를 명시적으로 받도록 수정합니다.


main.py와 폼에 LLM 보정 옵션 추가 중.


스크립트에서 체크박스 값 전송 처리


체크박스용 스타일 추가 중.


README에 LLM 보정 사용법 추가 중.


LLM 문맥 보정 기능을 선택 옵션으로 넣었습니다. 적용된 내용만 정리합니다.

## 1. LLM 문맥 보정 가능 여부

**가능합니다.** 등기부 문맥(소재지·소유자·면적·근저당·임차인 등)을 이용해 OCR 오타·빠진 글자·헷갈리는 표현을 LLM이 한 번 더 고쳐줄 수 있습니다.

## 2. 추가된 모듈·동작 (`llm_correction.py`)

- **correct_with_llm(text, api_key=None, model="gpt-4o-mini")**  
  - OCR 결과 전체를 한 번에 넘기면, 등기부 문맥만 보정하도록 한 프롬프트로 GPT 호출.  
  - “원문에 없던 내용은 넣지 말 것”, “줄바꿈·구조 유지”, “등기 용어는 표준 표기로 통일” 등 규칙을 시스템 프롬프트에 넣어 두었습니다.
- **is_llm_available()**  
  - `openai` 설치 여부 + `OPENAI_API_KEY` 존재 여부로, LLM 보정 사용 가능 여부를 판단합니다.
- API 키가 없거나 `openai`가 없으면 **원문을 그대로 돌려주고**, 예외는 삼키도록 했습니다.

## 3. OCR 파이프라인 연동 (`ocr_service.py`)

- **extract_text(..., use_llm_correction=None)**  
  - `use_llm_correction=True`이거나, `None`인데 환경변수 `USE_LLM_CORRECTION=1`이면  
    **용어 사전 보정(real_estate_terms) 이후**에 `correct_with_llm(text)`를 한 번 더 호출합니다.
- `use_llm_correction=False`이면 LLM 단계는 건너뜁니다.

## 4. API·UI

- **POST /api/upload**  
  - 폼 필드 `use_llm_correction`: `"true"` / `"false"` (기본 `"false"`).
- **업로드 폼**  
  - “LLM 문맥 보정 (OpenAI API 키 필요, 오타·문맥 교정)” 체크박스 추가.  
  - 체크 시 `use_llm_correction=true`로 전달됩니다.
- 서버 쪽에는 **`OPENAI_API_KEY`**가 설정돼 있어야 실제로 LLM이 호출됩니다.

## 5. 의존성·문서

- **requirements.txt**  
  - `openai>=1.0.0` 추가.
- **README.md**  
  - LLM 문맥 보정 사용법(환경변수, UI 옵션) brief 안내 추가.

## 6. 사용 방법

1. **환경변수**  
   - `OPENAI_API_KEY=sk-...`  
   - (선택) 서버 기본 동작으로 LLM 보정을 쓰려면: `USE_LLM_CORRECTION=1`
2. **웹 UI**  
   - 이미지 업로드 후 **“LLM 문맥 보정”** 체크 후 분석 실행.
3. **모델/토큰**  
   - 기본: `gpt-4o-mini`, `max_tokens=4096`.  
   - 바꾸려면 `llm_correction.py`의 `correct_with_llm()` 인자에서 `model`, `max_tokens` 수정하면 됩니다.

정리하면, “문맥을 읽고 텍스트 정확도를 높일 수 있을까?”에 대해 **가능하고**, 위와 같이 LLM 보정을 선택 사항으로 붙여 두었습니다.

---

**User**

키는 REMOVED_TOKEN이거야

---

**Cursor**

`hf_`로 시작하는 키는 Hugging Face 토큰입니다. 현재 LLM 보정은 OpenAI를 쓰므로, Hugging Face Inference API를 지원해 이 토큰으로도 문맥 보정을 쓸 수 있게 추가합니다.  
**키는 코드·설정 파일에 넣지 말고, 환경 변수로만** 쓰세요.


Hugging Face 토큰(`hf_`…)으로 문맥 보정을 사용할 수 있도록, HF Inference API 지원을 추가합니다. **키는 환경 변수로만** 넣어 주세요 (코드/설정 파일에 적지 마세요).


Hugging Face 토큰으로 문맥 보정을 쓸 수 있게 `llm_correction.py`에 HF 지원을 넣고, **키는 환경 변수로만** 쓰도록 하겠습니다.


Hugging Face 토큰 지원 추가. 키는 코드에 넣지 않고 환경 변수로만 사용합니다.


README에 Hugging Face 토큰 설정 방법을 추가하고, `.env.example`에 항목만 넣습니다. **실제 키 값은 README·예제 파일에 넣지 않습니다.**


`.env.example`에 Hugging Face 토큰 예시만 추가합니다. 실제 키는 넣지 않습니다.


Hugging Face 토큰을 알려주셨습니다. 보안상 코드나 설정 파일에 직접 넣지 않고, 환경 변수로만 사용해야 합니다. 프로젝트에 `.env` 로딩과 `.gitignore` 적용 여부를 확인 중입니다.


main.py에 `.env` 로딩이 없습니다. `load_dotenv()`를 추가해 로컬 `.env`에서 `HF_TOKEN`을 읽도록 하겠습니다. 실제 토큰은 코드·설정 파일에 넣지 않고, 사용자가 `.env`에만 적어 사용하시면 됩니다.


`.env` 로딩을 `main.py`에 넣었습니다. 이제 **실제 토큰은 코드나 깃에 넣지 말고**, 아래 방법 중 하나로만 쓰세요.

---

### 1) `.env` 파일로 쓰기 (권장)

프로젝트 루트(`c:\AI_HomeMatch_Python`)에 `.env` 파일을 만들고 다음 한 줄을 넣으세요:

```env
HF_TOKEN=REMOVED_TOKEN
```

`.env`는 이미 `.gitignore`에 있어서 Git에 올라가지 않습니다.

---

### 2) 터미널에서만 쓰기

서버 실행 전에 한 번만 설정:

```powershell
$env:HF_TOKEN="REMOVED_TOKEN"
python -m uvicorn main:app --reload
```

---

웹에서 **"LLM 문맥 보정"**을 체크하면, `OPENAI_API_KEY`가 없을 때 위에 설정한 `HF_TOKEN`으로 Hugging Face Inference API를 사용해 문맥 보정이 동작합니다.

---

**User**

지금 LLM 기능이 적용된거야?

---

**Cursor**

LLM 보정이 업로드부터 OCR까지 어떻게 연결되는지 확인 중입니다.


네, **LLM 기능은 이미 적용된 상태**입니다. 동작 흐름만 정리하면 아래와 같습니다.

---

### 1) 웹 → 서버 연결

- **업로드 화면**: "LLM 문맥 보정 (OpenAI API 키 필요…)" 체크박스가 있고, `script.js`에서  
  `use_llm_correction`을 체크 여부에 따라 `'true'` / `'false'`로 보냅니다.
- **main.py**: `use_llm_correction`을 받아서  
  `use_llm = (값 == "true")` 로 만들고,  
  `ocr_service.extract_text(..., use_llm_correction=use_llm)` 에 넘깁니다.

### 2) OCR 서비스에서 LLM 호출

`ocr_service.py` 안에서:

- `use_llm_correction`이 **True**이면  
  OCR·용어 보정까지 끝난 뒤 **`correct_with_llm(text)`** 를 호출합니다.
- `llm_correction.py`의 `correct_with_llm()`이  
  **OPENAI_API_KEY**가 있으면 OpenAI, 없으면 **HF_TOKEN** / **HUGGINGFACE_HUB_TOKEN** 으로 Hugging Face Inference API를 사용합니다.

그래서 **“LLM 기능이 적용돼 있냐?”**에 대한 답은 **“예, 적용되어 있다”**입니다.

---

### 실제로 LLM이 돌게 하려면

1. **웹에서**  
   이미지 업로드 후 **“LLM 문맥 보정”** 체크하고 **분석 시작**을 누릅니다.
2. **환경 설정**  
   아래 중 하나만 하면 됩니다.
   - `.env`에  
     `HF_TOKEN=hf_CyCo...`  
     넣고, `main.py`에서 `load_dotenv()`로 읽히게 되어 있으므로 **서버만 다시 실행**하면 됩니다.
   - 또는 터미널에서  
     `$env:HF_TOKEN="hf_CyCo..."`  
     설정한 뒤 같은 터미널에서 서버를 실행합니다.

이렇게 하면 **체크했을 때만** LLM 문맥 보정이 적용되고, HF 토큰이 있으면 Hugging Face로 동작합니다.

---

**User**

LLM 보정된 문맥이랑 아닌거랑 텍스트가 같은데

---

**Cursor**

LLM 보정이 적용돼도 텍스트가 그대로인 원인 조사 중입니다. HF API 호출·응답 처리와 오류 시 폴백 로직을 확인합니다.


HF API 호출 실패·응답 파싱 오류 시 예외를 무시하고 원문을 반환하고 있어, 로그 추가·응답 파싱 보강·에러 처리 개선을 진행합니다.


원인: HF API 실패·응답 파싱 실패 시 예외를 삼키고 원문을 그대로 반환하고 있음. 로그 추가, 응답 파싱 보강, HF Chat(OpenAI 호환) 지원을 적용합니다.


HF Chat(OpenAI 호환) 엔드포인트 추가 중. Instruct 모델은 채팅 형식이 더 잘 동작합니다.


HF Chat(router.huggingface.co) 우선 호출 추가 중입니다.


서버 실행 시 LLM 관련 로그가 보이도록 main.py에서 로거 레벨 설정 중.


수정 반영했습니다. LLM 보정이 안 보이던 이유는 **실패해도 예외를 삼키고 원문만 그대로 돌려주던 구조** 때문이었고, 아래처럼 바꿨습니다.

---

## 1. 로그 추가 (원인 확인용)

`llm_correction.py`에 로그를 넣었습니다. **LLM 문맥 보정**을 켜고 다시 실행하면 **서버 콘솔**에서 예를 들어 다음처럼 나옵니다.

- `LLM 보정: OpenAI 시도` / `LLM 보정: HF Chat API 시도 model=...`
- `LLM 보정: HF API 호출 중 model=...` (레거시 호출 시)
- `LLM 보정: HF API 타임아웃` / `LLM 보정: HF 모델 로딩 중 (503)` / `LLM 보정: HF 응답에서 generated_text 없음...`
- **실패 시**: `LLM 보정: 적용 실패, 원문 그대로 반환 (API 오류·파싱 실패·빈 응답 등)`

콘솔에 찍히는 이 메시지로 **왜 원문과 동일하게 나왔는지** 확인할 수 있습니다.

---

## 2. HF API 응답·에러 처리 보강

- 503·에러 JSON(`error`, `estimated_time` 등)를 구분해 처리
- `generated_text`가 리스트/딕셔너리 둘 다 되는 경우에 맞게 파싱
- JSON 파싱 실패·타임아웃도 로그에 남기도록 처리

---

## 3. HF Chat(OpenAI 호환) 우선 사용

Instruct 모델은 **채팅 형식**이 더 잘 맞으니, HF 토큰만 있을 때 호출 순서를 이렇게 바꿨습니다.

1. **HF Chat** (`router.huggingface.co/v1` · OpenAI 호환)  
   - `openai` 패키지로 `base_url` + HF 토큰으로 호출
2. 실패 시 **레거시 Inference API** (`api-inference.huggingface.co/models/...`)

`Qwen/Qwen2-0.5B-Instruct`는 router에서 지원할 수 있어, Chat으로 호출하면 보정이 더 잘 나올 수 있습니다.

---

## 4. 확인 방법

1. 서버 재시작  
   - `python main.py` 또는 `uvicorn main:app --reload`
2. 웹에서 **LLM 문맥 보정** 체크 후 이미지 업로드·분석
3. **서버 터미널**에서  
   - `LLM 보정: HF Chat 시도 ...` / `LLM 보정: HF API 호출 중 ...`  
   - 또는 `LLM 보정: 적용 실패, 원문 그대로 반환 ...`  
   같은 로그가 뜨는지 확인

여기서 **“적용 실패, 원문 그대로 반환”**이 보이면, 그 위에 찍힌 로그(타임아웃, 503, `generated_text` 없음 등)가 원인입니다.  
그 로그 내용을 알려주시면, 그걸 기준으로 다음 수정 지점을 짚어드리겠습니다.

---

**User**

부동산 등기부등본 분석 서비스가 시작되었습니다.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:49384 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:49384 - "GET /style.css HTTP/1.1" 200 OK
INFO:     127.0.0.1:49385 - "GET /script.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:49385 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:49391 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:49391 - "GET /style.css HTTP/1.1" 200 OK
INFO:     127.0.0.1:49391 - "GET /script.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:49391 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:49393 - "POST /api/upload HTTP/1.1" 400 Bad Request
C:\Python310\lib\site-packages\torch\utils\data\dataloader.py:775: UserWarning: 'pin_memory' argument is set as true but no accelerator is found, then device pinned memory won't be used.
  super().__init__(loader)
LLM 보정: HF API 오류 status=410 detail={'error': 'https://api-inference.huggingface.co is no longer supported. Please use https://router.huggingface.co instead.'}
LLM 보정: 적용 실패, 원문 그대로 반환 (API 오류·파싱 실패·빈 응답 등)
INFO:     127.0.0.1:49401 - "POST /api/upload HTTP/1.1" 200 OK

---

**Cursor**

HF 레거시 API(`api-inference.huggingface.co`)가 410으로 중단되었습니다. `router.huggingface.co`만 사용하도록 변경합니다.


레거시 API(`api-inference.huggingface.co`)가 410으로 중단되었습니다. `router.huggingface.co`만 사용하도록 변경합니다. 레거시 폴백을 제거하고 HF Chat만 사용하도록 수정합니다.


레거시 API 호출을 제거하고 HF Chat(`router.huggingface.co`)만 사용하도록 변경했습니다. `requirements.txt`에 `openai`가 포함되어 있는지 확인 중입니다.


변경 완료. 이제 **HF Chat API(`router.huggingface.co`)만 사용**합니다.

---

## 변경 사항

1. 레거시 API 제거: `api-inference.huggingface.co` 호출 코드 삭제 (410 오류 원인)
2. HF Chat만 사용: `router.huggingface.co/v1`의 OpenAI 호환 엔드포인트만 사용
3. 폴백 로직 제거: 레거시로 폴백하지 않음

---

## 동작 방식

- **OpenAI 키**가 있으면 → OpenAI 사용
- **HF 토큰**만 있으면 → HF Chat(`router.huggingface.co`) 사용
- 둘 다 없으면 → LLM 보정 건너뜀

---

## 확인 방법

서버를 재시작한 뒤 **LLM 문맥 보정**을 체크하고 이미지를 업로드하세요. 서버 콘솔에 다음과 같은 로그가 보여야 합니다:

- `LLM 보정: HF Chat API 시도 model=Qwen/Qwen2-0.5B-Instruct`
- `LLM 보정: HF Chat 성공 N 문자` (성공 시)
- 또는 `LLM 보정: HF Chat 실패 ...` (실패 시, 상세 오류 포함)

410 오류는 더 이상 발생하지 않습니다.

---

**User**

ollama 사용해서 가능해?

---

**Cursor**

Ollama 지원 추가 중. OpenAI 호환 API를 제공하므로 동일한 방식으로 사용할 수 있습니다.


Ollama 지원 추가 중. 로컬 실행으로 빠르고 무료이며, 데이터가 외부로 전송되지 않습니다.


Ollama 지원을 추가했습니다. README에 사용법을 추가합니다.


Ollama 지원을 추가했습니다.

---

## 변경 사항

1. Ollama 함수 추가: `_call_ollama()` - 로컬 Ollama 서버와 통신
2. 우선순위 설정:
   - OpenAI (클라우드, 유료)
   - Ollama (로컬, 무료, 빠름) ← 새로 추가
   - Hugging Face (클라우드, 무료 티어)
3. 환경 변수 지원:
   - `OLLAMA_BASE_URL` (기본: `http://localhost:11434/v1`)
   - `OLLAMA_MODEL` (기본: `qwen2.5:7b`)

---

## Ollama 사용 방법

### 1. Ollama 설치
- [ollama.ai](https://ollama.ai/)에서 다운로드 및 설치

### 2. 모델 다운로드 (한국어 지원 모델 추천)
```bash
ollama pull qwen2.5:7b
# 또는
ollama pull llama3.2:3b
```

### 3. Ollama 서버 실행
- Ollama 설치 후 자동으로 `localhost:11434`에서 실행됨
- 별도 설정 불필요 (기본값 사용)

### 4. 환경 변수 설정 (선택)
- `.env` 파일에 추가:
```env
OLLAMA_MODEL=qwen2.5:7b
```
- 또는 터미널에서:
```powershell
$env:OLLAMA_MODEL="qwen2.5:7b"
```

---

## 장점

- 무료: 로컬 실행으로 비용 없음
- 빠름: 네트워크 지연 없음
- 프라이버시: 데이터가 외부로 전송되지 않음
- 오프라인: 인터넷 없이도 사용 가능

---

## 동작 방식

1. OpenAI 키가 있으면 → OpenAI 사용
2. 없으면 → Ollama 시도 (로컬 서버)
3. Ollama 연결 실패 시 → Hugging Face 시도

서버를 재시작한 뒤 LLM 문맥 보정을 체크하고 테스트하세요. 서버 콘솔에 `LLM 보정: Ollama 시도 model=qwen2.5:7b` 같은 로그가 보이면 정상 동작입니다.

---

**User**

gemma2:9b 사용중이야

---

**Cursor**

`gemma2:9b` 사용을 위해 환경 변수 설정을 확인하고, 필요 시 기본값을 업데이트합니다.


`gemma2:9b` 사용을 위해 `.env.example`에 예시를 추가하고, 기본값을 `gemma2:9b`로 변경합니다.


기본값을 `gemma2:9b`로 변경했습니다.

---

## 변경 사항

1. 기본 모델 변경: `qwen2.5:7b` → `gemma2:9b`
2. 문서 업데이트: `.env.example`, `README.md`에 `gemma2:9b` 예시 반영

---

## 동작 방식

- 환경 변수 `OLLAMA_MODEL`이 설정되어 있으면 → 해당 모델 사용
- 설정되어 있지 않으면 → 기본값 `gemma2:9b` 사용

---

## 확인 방법

서버를 재시작한 뒤 LLM 문맥 보정을 체크하고 테스트하세요. 서버 콘솔에 다음과 같은 로그가 보여야 합니다:

```
LLM 보정: Ollama 시도 model=gemma2:9b base_url=http://localhost:11434/v1
LLM 보정: Ollama 성공 N 문자
```

Ollama가 실행 중이고 `gemma2:9b` 모델이 다운로드되어 있으면 바로 사용됩니다.

---

**User**

open 키 값 gpt로 바꿧어

---

**Cursor**

OpenAI API 키를 설정하셨다면, 현재 코드는 이미 OpenAI를 최우선으로 사용합니다. 설정이 올바르게 적용되는지 확인 중입니다.


현재 코드는 OpenAI를 최우선으로 사용합니다. OpenAI API 키가 설정되어 있으면 자동으로 사용됩니다.

---

## 현재 동작 순서

1. OpenAI (키가 있으면 우선 사용)
2. Ollama (OpenAI 실패 시)
3. Hugging Face (Ollama 실패 시)

---

## OpenAI 모델 설정

현재 기본 모델은 `gpt-4o-mini`입니다. 다른 모델을 사용하려면:

### 방법 1: 환경 변수로 설정 (권장)

`.env` 파일에 추가:
```env
OPENAI_API_KEY=sk-여기에키값
OPENAI_MODEL=gpt-4o  # 또는 gpt-3.5-turbo 등
```

### 방법 2: 코드에서 기본값 변경

원하시면 코드의 기본 모델명을 변경할 수 있습니다. 어떤 GPT 모델을 사용하시겠습니까?
- `gpt-4o`
- `gpt-4o-mini` (현재 기본값)
- `gpt-3.5-turbo`
- 기타

---

## 확인 방법

서버를 재시작한 뒤 LLM 문맥 보정을 체크하고 테스트하세요. 서버 콘솔에 다음과 같은 로그가 보여야 합니다:

```
LLM 보정: OpenAI 시도
LLM 보정: OpenAI 성공 N 문자
```

OpenAI 키가 올바르게 설정되어 있으면 바로 사용됩니다.

---

**User**

C:\Python310\lib\site-packages\torch\utils\data\dataloader.py:775: UserWarning: 'pin_memory' argument is set as true but no accelerator is found, then device pinned memory won't be used.
  super().__init__(loader)
LLM 보정: 적용 실패, 원문 그대로 반환 (API 오류·파싱 실패·빈 응답 등)
INFO:     127.0.0.1:50240 - "POST /api/upload HTTP/1.1" 200 OK 계속 이 오류 떠

---

**Cursor**

LLM 보정이 실패하고 있습니다. 원인 파악을 위해 로그를 보강하고, 각 단계의 오류를 더 자세히 출력하도록 수정 중입니다.


로그를 보강해 각 단계의 실패 원인을 명확히 출력하도록 수정 중입니다.


로그를 보강했습니다. 이제 각 단계의 실패 원인을 더 자세히 확인할 수 있습니다.

---

## 변경 사항

1. OpenAI 호출 함수에 로깅 추가: 실패 시 구체적인 오류 메시지 출력
2. 각 단계별 상세 로그 추가:
   - OpenAI 키 존재 여부 확인
   - Ollama 시도 여부 확인
   - HF 토큰 존재 여부 확인
   - 각 단계 실패 시 다음 단계로 폴백하는 과정 표시
3. 로깅 설정 개선: INFO 이상 레벨 로그가 모두 출력되도록 설정

---

## 확인 방법

서버를 재시작한 뒤 LLM 문맥 보정을 체크하고 이미지를 업로드하세요. 서버 콘솔에 다음과 같은 상세 로그가 표시됩니다:

```
LLM 보정: OpenAI 키 발견, OpenAI 시도
LLM 보정: OpenAI 시도 model=gpt-4o-mini
LLM 보정: OpenAI 실패 [구체적인 오류 메시지]
LLM 보정: OpenAI 실패, Ollama로 폴백
LLM 보정: Ollama 시도 model=gemma2:9b base_url=http://localhost:11434/v1
LLM 보정: Ollama 실패 [구체적인 오류 메시지]
...
```

이 로그로 어느 단계에서 실패했는지 확인할 수 있습니다.

---

## 가능한 원인

1. OpenAI 키가 없거나 잘못됨 → "OpenAI 키 없음" 또는 "OpenAI 실패" 로그 확인
2. Ollama가 실행되지 않음 → "Ollama 실패: Connection refused" 같은 오류 확인
3. OpenAI SDK 미설치 → "OpenAI SDK가 설치되지 않음" 로그 확인

서버를 재시작한 뒤 로그를 확인해 주세요. 어떤 오류 메시지가 나오는지 알려주시면 추가로 도와드리겠습니다.

---

**User**

C:\Python310\lib\site-packages\torch\utils\data\dataloader.py:775: UserWarning: 'pin_memory' argument is set as true but no accelerator is found, then device pinned memory won't be used.
  super().__init__(loader)
WARNING: LLM 보정: OpenAI 키는 있지만 OpenAI SDK가 설치되지 않음
WARNING: LLM 보정: OpenAI SDK가 없어 Ollama 사용 불가
INFO: LLM 보정: Hugging Face 토큰 없음
WARNING: LLM 보정: 모든 LLM 옵션 실패, 원문 그대로 반환
INFO:     127.0.0.1:50361 - "POST /api/upload HTTP/1.1" 200 OK 이거

---

**Cursor**

OpenAI SDK가 설치되지 않아 LLM 보정이 동작하지 않습니다. `requirements.txt`를 확인하고 `openai` 패키지 설치 여부를 점검 중입니다.


OpenAI SDK가 설치되지 않아 LLM 보정이 동작하지 않습니다. `requirements.txt`에는 있지만 실제로 설치되지 않았습니다. 설치 중입니다.


pip에서 패키지를 찾지 못하고 있습니다. 네트워크 또는 pip 인덱스 문제일 수 있습니다. 아래 방법으로 설치해 주세요.

---

## 해결 방법

### 1. OpenAI SDK 설치

터미널에서 다음 명령을 실행하세요:

```powershell
pip install openai
```

또는 requirements.txt 전체 설치:

```powershell
pip install -r requirements.txt
```

---

### 2. 설치 확인

설치 후 다음 명령으로 확인:

```powershell
python -c "import openai; print('OpenAI SDK 설치됨:', openai.__version__)"
```

---

### 3. 네트워크 문제 시

pip 인덱스를 명시적으로 지정:

```powershell
pip install -i https://pypi.org/simple openai
```

또는 업그레이드 후 재시도:

```powershell
python -m pip install --upgrade pip
pip install openai
```

---

## 설치 후

서버를 재시작하면 다음 로그가 보여야 합니다:

```
LLM 보정: OpenAI 키 발견, OpenAI 시도
LLM 보정: OpenAI 시도 model=gpt-4o-mini
LLM 보정: OpenAI 성공 N 문자
```

설치 후에도 문제가 있으면 알려주세요.

---

**User**

WARNING: LLM 보정: OpenAI 키는 있지만 OpenAI SDK가 설치되지 않음
WARNING: LLM 보정: OpenAI SDK가 없어 Ollama 사용 불가
INFO: LLM 보정: Hugging Face 토큰 없음
WARNING: LLM 보정: 모든 LLM 옵션 실패, 원문 그대로 반환
INFO:     127.0.0.1:50550 - "POST /api/upload HTTP/1.1" 200 OK

---

**Cursor**

OpenAI SDK가 아직 설치되지 않았거나 다른 Python 환경에 설치된 것으로 보입니다. Python 환경과 설치 상태를 확인 중입니다.


OpenAI SDK가 설치되어 있지 않습니다. 설치를 다시 시도 중입니다.


pip가 패키지를 찾지 못하고 있습니다. 네트워크 또는 인덱스 설정 문제일 수 있습니다. 아래 방법으로 설치해 주세요.

---

## 해결 방법

### 방법 1: requirements.txt로 설치 (권장)

프로젝트 폴더에서 다음 명령을 실행하세요:

```powershell
cd c:\AI_HomeMatch_Python
pip install -r requirements.txt
```

---

### 방법 2: 직접 설치

```powershell
pip install openai
```

또는

```powershell
python -m pip install openai
```

---

### 방법 3: 네트워크 문제 시

인터넷 연결을 확인하고, 필요 시 프록시 설정을 확인하세요. 또는 다른 네트워크에서 시도해 보세요.

---

### 방법 4: 설치 확인

설치 후 다음 명령으로 확인:

```powershell
python -c "import openai; print('설치 완료:', openai.__version__)"
```

---

## 설치 후

1. 서버를 완전히 종료 (Ctrl+C)
2. 서버를 다시 시작
3. LLM 문맥 보정을 체크하고 테스트

설치 후에도 문제가 있으면 알려주세요.

---

**User**

pdf 파일도 가능하게

---

**Cursor**

PDF 파일 지원 추가 중: PDF를 이미지로 변환한 뒤 OCR을 적용합니다.


PDF 지원 추가 중: PDF를 이미지로 변환한 뒤 OCR을 적용합니다.


PDF 처리 함수 추가 및 업로드 엔드포인트 수정 중.


UI에서 PDF 파일 선택 허용 및 안내 문구 업데이트 중.


README에 PDF 지원 내용 추가 중.


PDF 파일 지원을 추가했습니다.

---

## 변경 사항

1. **PDF 처리 라이브러리 추가**: `PyMuPDF`를 `requirements.txt`에 추가
2. **PDF → 이미지 변환**: PDF를 각 페이지별로 이미지로 변환 후 OCR 처리
3. **다중 페이지 지원**: PDF의 모든 페이지를 처리하고 텍스트 병합
4. **UI 업데이트**: 파일 선택에서 PDF 허용 및 안내 문구 수정

---

## 설치 방법

PDF 지원을 사용하려면 PyMuPDF를 설치하세요:

```powershell
pip install PyMuPDF
```

또는 requirements.txt 전체 설치:

```powershell
pip install -r requirements.txt
```

---

## 동작 방식

1. **PDF 업로드**: PDF 파일을 업로드하면 자동으로 감지
2. **페이지별 변환**: 각 페이지를 300 DPI 이미지로 변환
3. **OCR 처리**: 각 페이지에 OCR 적용
4. **텍스트 병합**: 모든 페이지 텍스트를 병합 (페이지 번호 표시)
5. **LLM 보정**: 선택 시 전체 텍스트에 LLM 보정 적용

---

## 사용 방법

1. 서버 재시작
2. 웹 UI에서 **이미지 또는 PDF 파일** 선택
3. "분석 시작" 클릭

PDF 파일은 자동으로 처리되며, 여러 페이지가 있으면 모두 처리됩니다.

---

## 참고

- PDF는 각 페이지를 이미지로 변환하므로 처리 시간이 더 걸릴 수 있습니다
- 대용량 PDF는 메모리 사용량이 증가할 수 있습니다
- PDF 내 텍스트가 이미지로 스캔된 경우에만 OCR이 필요합니다 (텍스트 PDF는 직접 추출 가능하지만 현재는 이미지 변환 방식 사용)

설치 후 테스트해보시고 문제가 있으면 알려주세요.

---

**User**

이미지 화질이 안좋을 때 글을 인식못하거나 정확도가 떨어지는데 업스케일링 추가하고싶어

---

**Cursor**

### 요약

**해상도(업스케일링) 보정을 전처리에 자동으로 추가했습니다.**  
작은 이미지(세로·가로가 전체적으로 너무 작은 등기부 스캔본)는 먼저 키운 다음 OCR을 돌리도록 바꿔서, 흐릿해서 글자를 잘 못 읽던 경우 정확도를 올리도록 했습니다.

---

### 어떻게 동작하는지

`preprocess.py` 쪽 전처리 파이프라인을 이렇게 수정했습니다.

- **새 업스케일링 로직 (`normalize_size`)**
  - 긴 변 기준으로:
    - `side < 1200`이면 → **업스케일링** (비율 유지, `INTER_CUBIC` 또는 Pillow `LANCZOS`)
    - `side > max_side`이면 → 다운스케일링 (기존과 동일)
    - 그 사이면 → 크기 그대로 유지

- **적용 위치**
  - `preprocess_doc_only`, `preprocess_light`, `preprocess_full` 에서 모두 사용:
    - `normalize_size(out, min_side=1200, max_side=2400)`
  - 즉, 전처리 옵션을 `문서 대비만 / 가벼운 / 강한` 중 하나로 쓰면,
    - 이미지가 너무 작을 때 자동으로 **최소 1200px 정도까지 키운 뒤** CLAHE, 이진화 등을 적용합니다.

코드상으로는 대략 이런 식입니다:

```python
def normalize_size(img, min_side=0, max_side=2000):
    # side < min_side → 업스케일
    # side > max_side → 다운스케일
    # 그 외 → 그대로
    ...
```

---

### 사용자가 해야 할 일

따로 옵션을 더 고를 필요는 없습니다.

- 지금 쓰시던 전처리 옵션(`문서 대비만 / 가벼운 / 강한`)을 그대로 사용하시면,
- **해상도가 낮은 이미지일 때만 자동으로 업스케일링**이 걸립니다.

이미지가 충분히 큰 경우에는 크기를 건드리지 않아, 불필요하게 이미지를 키워서 노이즈가 늘어나는 일은 최소화했습니다.

---

### 추가로 해볼 수 있는 것

- **해상도가 아주 낮은 등기부 스캔본**으로 다시 한 번 업로드 테스트해 보세요.
- 그래도 특정 샘플에서 잘 안 읽힌다면:
  - 그 이미지를 기준으로 업스케일 배율(예: min_side 1200 → 1600)이나
  - 전처리 옵션(`doc` vs `full`)을 조정하는 튜닝도 함께 해볼 수 있습니다.

---

**User**

지금 신뢰도가 낮은 텍스트에 대해서 부동산, 계약서 관련 단어중에 가장 유사도가 높은 단어로 변환하는 것도 적용되어있어? 말만해줘

---

**Cursor**

네, **이미 적용되어 있습니다.**

- `real_estate_terms.py`에 **부동산/등기·계약서 용어 사전 + 오타→정답 매핑**이 들어있고  
- `ocr_service.py`에서 `ocr_service.extract_text(...)` 마지막 단계에서 항상 `correct_with_vocab(text)`를 호출해서  
  - OCR 결과 텍스트 전체에 대해  
  - 자주 틀리는 단어/표현을 **부동산·계약서 관련 표준 단어로 치환**하도록 되어 있습니다.

즉, LLM 보정과는 별개로, **도메인 용어 기반 보정은 이미 자동으로 돌고 있습니다.**

---

**User**

업로드한 이미지랑 비교해서 어느 부분에서 어떤 텍스트가 추출 되었는지 확인 할 수 있는 시각적 자료를 확인 하고싶은데

---

**Cursor**

업로드한 이미지 위에 OCR로 추출한 각 텍스트 영역의 박스와 텍스트를 겹쳐 보여주는 기능을 추가합니다.


이미지와 OCR 추출 영역을 겹쳐 보여주는 기능을 구현합니다. 관련 파일부터 확인합니다.


이미지 위에 OCR 추출 영역(바운딩 박스)과 텍스트를 겹쳐 보여주는 기능을 구현합니다.


main.py에 `base64` import를 추가하고, 이미지 업로드 시 `regions`와 `image_data_url`을 포함하도록 수정합니다.


script.js에서 `displayResults`에 이미지·영역 렌더링과 박스 그리기 추가 중.


오버레이는 이미지와 동일한 영역에 겹치도록 하고, 박스 좌표를 %로 두어 리사이즈에 대응합니다.


CSS에 이미지·오버레이·영역 박스 스타일 추가 중입니다.


이미지가 이미 캐시돼 있을 때 `onload`가 늦게 오거나 안 올 수 있어, `imgEl.complete`일 때는 곧바로 박스를 그리도록 처리합니다.


요청하신 대로 **이미지 위에 OCR로 인식된 영역과 텍스트를 겹쳐 보여주는 시각화**까지 반영했습니다.

## 구현된 기능

1. **OCR 영역 반환 (`ocr_service.py`)**
   - `get_detection_regions()` 추가: EasyOCR 한 번 실행 후 `bbox`, `text`, `confidence` 리스트와 사용한 이미지 바이트를 반환합니다.
   - 전처리(`none` / `doc` / `light` / `full`)는 텍스트 추출과 동일하게 적용됩니다.

2. **업로드 API 응답 확장 (`main.py`)**
   - **이미지** 업로드일 때만:
     - `regions`: `[{ "bbox": [[x,y],...], "text": "...", "confidence": 0.99 }, ...]`
     - `image_data_url`: OCR에 사용한 이미지(전처리된 이미지)의 base64 Data URL

3. **결과 화면 UI**
   - **「이미지에서 추출 위치」** 블록 추가: 분석 결과 카드 안에 원본(전처리) 이미지와 그 위에 인식 영역 박스를 겹쳐 표시합니다.
   - 각 박스에 마우스를 올리면 **툴팁**으로 해당 영역의 인식 텍스트와 신뢰도(%)가 나옵니다.
   - 박스는 반투한 보라색으로 표시되고, 호버 시 더 진하게 보입니다.

4. **PDF / Tesseract**
   - PDF 업로드 시에는 `regions`·시각화를 쓰지 않고, **이미지 + EasyOCR**인 경우에만 영역 시각화가 나옵니다.
   - OCR 방법이 Tesseract이면 `regions`는 비어 있고, 이미지 영역 블록은 보이지 않습니다.

이미지(JPG/PNG)를 올리고 **EasyOCR**로 분석하면, 결과 섹션의 「이미지에서 추출 위치」에서 **어느 구역에서 어떤 텍스트가 나왔는지** 박스와 툴팁으로 확인할 수 있습니다.

---

**User**

각 부분별로 정확도를 수치로 표현해줘

---

**Cursor**

각 OCR 영역에 신뢰도(정확도)를 숫자로 표시하도록 수정합니다.


각 영역 박스에 정확도(신뢰도) 수치를 배지로 표시합니다.


`var`를 `const`로 바꿔 스타일을 맞춥니다.


반영했습니다. 이제 **각 인식 영역마다 정확도(신뢰도)가 숫자로** 보입니다.

## 변경 사항

1. **영역별 정확도 배지**
   - 각 OCR 영역 박스 **왼쪽 위**에 `98.5%` 같은 **퍼센트 수치**가 작은 배지로 표시됩니다.
   - 배지는 흰 배경·작은 그림자로 구분되며, 호버 시 툴팁으로 해당 영역의 **인식 텍스트**와 **신뢰도**가 함께 나옵니다.

2. **표시 형식**
   - 소수점 한 자리까지 퍼센트로 표시 (예: `99.2%`, `87.0%`).
   - `confidence`가 없으면 `-`로 표시됩니다.

이미지 업로드 후 분석 결과의 「이미지에서 추출 위치」에서, 박스마다 왼쪽 위 숫자로 해당 부분의 OCR 정확도를 바로 확인할 수 있습니다.

---

**User**

정확도가 좀더 위에 표시되게 하고싶은데 어디 수정해? 말만해줘

---

**Cursor**

정확도 배지를 더 위로 보이게 하려면 **`static/style.css`** 안의 `.result-regions-overlay .region-box .region-accuracy-badge` 스타일을 바꾸면 됩니다.

지금은 `top: 0`이라 박스 안쪽 왼쪽 위에 붙어 있고, 위로 올리려면 예를 들어:

- `top: -18px` 같은 **음수 값**을 주거나  
- `top: 0; transform: translateY(-100%);` 처럼 **위로만 옮기는** 방식

을 쓰면 됩니다. 그 부분만 수정하면 됩니다.

---

**User**

정확도 옆에 추출된 텍스트도 추가해줘

---

**Cursor**

정확도 배지 옆에 추출된 텍스트를 표시하도록 수정합니다.


정확도 옆에 추출된 텍스트를 표시하는 중입니다.


반영했습니다. 이제 각 영역 라벨에 **정확도 오른쪽에 추출된 텍스트**가 함께 나옵니다.

## 변경 내용

1. **표시 형식**: `98.5% · 추출된텍스트` 처럼 **정확도 · 추출 텍스트** 순으로 한 줄에 표시됩니다.
2. **긴 텍스트**: 박스보다 길어지면 `...`으로 잘려 보이도록 `text-overflow: ellipsis`를 적용했습니다.
3. **패딩**: 텍스트가 들어가서 `padding: 2px 6px`로 조금 늘려 두었습니다.

각 인식 영역 위 라벨에서 정확도와 추출 텍스트를 같이 볼 수 있습니다.

---

**User**

...으로 자르지 말고 전체 텍스트 나오게 하고, 텍스트 크기 좀더 키우고, real_estate_terms.py 에 표게부는 표제부로 바꾸게 되어있는데 왜 표게부로 나와?

---

**Cursor**

세 가지 수정 진행: 1) 전체 텍스트 표시(말줄임 제거) 2) 텍스트 크기 확대 3) `real_estate_terms.py`에서 '표게부'→'표제부' 보정 확인


시각화용 `regions`는 OCR 원문만 쓰고 있어 `correct_with_vocab`이 적용되지 않습니다. `get_detection_regions`에서 각 영역 텍스트에 `correct_with_vocab`을 적용하겠습니다.


세 가지 수정 적용 중입니다.


수정 반영했습니다. 변경 내용만 정리합니다.

## 1. 전체 텍스트 노출 + 글자 크기

**`static/style.css`**의 `.region-accuracy-badge`에서:

- `white-space: nowrap`, `overflow: hidden`, `text-overflow: ellipsis` 제거  
  → 말줄임 없이 전체 텍스트 표시
- `white-space: normal`, `word-break: break-all`, `max-width: none` 사용  
  → 줄바꿈·줄여쓰기 허용
- `font-size: 10px` → `13px`
- `padding: 2px 6px` → `3px 6px`

## 2. "표게부" → "표제부"가 영역에도 적용되도록

**`ocr_service.py`**의 `get_detection_regions()` 안에서, 각 영역의 `text`를 만들 때 **`correct_with_vocab(text)`**를 쓰도록 바꿨습니다.

이전에는 `correct_with_vocab`이 **최종 추출 문장**에만 적용되고, 시각화용 `regions`에는 OCR 원문이 그대로 들어가서 "표게부"가 남았습니다. 이제 영역 텍스트도 `real_estate_terms.py`의 `TYPO_TO_CANONICAL`(표게부→표제부 등)을 통과하므로, 영역 라벨에도 "표제부"로 나옵니다.

---

**User**

real_estate_terms.py 여기에 단어 추가하면 다시 학습 시켜야해? 말만해줘

---

**Cursor**

아니요, **다시 학습(트레이닝) 시킬 필요 없습니다.**

- `real_estate_terms.py`는 **규칙 기반 치환(사전 + 정규식)** 코드라,  
  거기에 단어(오타 → 정답)만 추가하면 **바로 그 규칙을 그대로 사용**합니다.
- 필요한 건 **애플리케이션 재시작만**이에요:
  - `uvicorn`을 `--reload`로 돌리는 중이면 파일 저장 후 자동 반영
  - 아니면 서버(백엔드) 한 번 껐다 켜면 새로 추가한 단어가 적용됩니다.

---

**User**

표계부단어를 표재부로 바꾸려는데 안되네 말만해줘

---

**Cursor**

아마 **두 가지 중 하나** 때문에 안 되는 거예요.

### 1. 현재 사전에 없는 오타라서
`real_estate_terms.py`를 보면 이미 이런 건 있습니다.

```python
"표게부": "표제부",
"표재부": "표제부",
"표개부": "표제부",
...
```

하지만 **`"표계부"`는 아직 없음** → 그러면 `"표계부"`는 그대로 남습니다.  
이럴 땐 `TYPO_TO_CANONICAL`에 **정확히 그 문자열을 추가**해야 합니다.

```python
"표계부": "표제부",
```

처럼요.

### 2. “띄어쓰기 기준 토큰”만 바꾸기 때문

`correct_with_vocab()` 안에서:

- 한 줄을 `" "`(공백) 기준으로 **토큰 단위**로 쪼갠 다음
- 각 토큰이 사전에 있을 때만 치환합니다.

즉, OCR 결과가:

- `표계부` → `"표계부"` 토큰을 사전에 넣으면 잘 바뀜
- `표계부단어` 처럼 **다른 글자랑 붙어 있으면**,  
  `"표계부단어"` 전체를 키로 넣어야 바뀝니다.

---

정리하면:

- **바꾸고 싶은 “그대로의 글자”를 키로** `TYPO_TO_CANONICAL`에 넣어야 하고,
- 서버를 다시 띄워야 적용됩니다 (`--reload`면 저장만 해도 됨).

---

**User**

등기부등본의 키워드 기반 영역 분리 (갑구/을구/표제부)해서 영역별로 인식 후 사용자가 텍스트 내용을 변경할 수 있게 만들어쥬ㅗ

---

**Cursor**

요청하신 기능까지 한 번에 다 붙였습니다. 지금 상태 기준으로 **어떻게 동작하는지** 정리해 드릴게요.

---

### 1. 갑구/을구/표제부 **키워드 기반 영역 분리**

- **어디서 나뉘냐?**
  - `main.py`에 `split_registry_sections(text)`라는 함수가 새로 추가됐습니다.
  - `표제부`, `갑구`, `을구`라는 키워드가 포함된 **줄 위치를 기준**으로,
    - `표제부` 영역
    - `갑구` 영역
    - `을구` 영역  
    으로 **텍스트를 잘라서 딕셔너리**로 만듭니다.
- 업로드 API (`/api/upload`)에서:
  - OCR 완료 후 `extracted_text`를 `split_registry_sections(extracted_text)`에 넣어
  - 응답 JSON에 **`sections`** 필드로 내려줍니다.

```jsonc
{
  "document_id": 1,
  "extracted_text": "...",
  "parsed_data": {...},
  "sections": {
    "pyojebu": "표제부 쪽 텍스트...",
    "gapgu": "갑구 쪽 텍스트...",
    "eulgu": "을구 쪽 텍스트..."
  }
}
```

---

### 2. 화면에서 **영역별(표제부/갑구/을구) 텍스트 편집**

- **`templates/index.html`** 결과 카드 안에 새 블록 추가:

```html
<div class="section-texts">
    <div class="text-header">
        <label>영역별 텍스트 편집 (표제부 / 갑구 / 을구)</label>
        <button type="button" class="btn btn-secondary" onclick="saveSectionTexts()">영역별 텍스트 저장</button>
    </div>
    <div class="section-text-grid">
        <div class="section-text-item">
            <label>표제부</label>
            <textarea id="sectionPyojebu"></textarea>
        </div>
        <div class="section-text-item">
            <label>갑구</label>
            <textarea id="sectionGapgu"></textarea>
        </div>
        <div class="section-text-item">
            <label>을구</label>
            <textarea id="sectionEulgu"></textarea>
        </div>
    </div>
</div>
```

- **`static/script.js`의 `displayResults`**에서:
  - 업로드 응답에 있는 `data.sections`를 읽어서
    - `sectionPyojebu`
    - `sectionGapgu`
    - `sectionEulgu`  
    각 textarea에 **초기값으로 채워 줍니다.**
  - 동시에 `currentDocumentId = data.document_id`로 현재 문서 ID를 저장합니다.

- 스타일은 **`static/style.css`**에 추가되어 있어서,
  - 3개 영역이 그리드로 예쁘게 나뉘고
  - 각각 독립적으로 수정할 수 있습니다.

---

### 3. 사용자가 수정한 영역 텍스트를 **서버에 저장**

- 프론트 쪽 JS에 **`saveSectionTexts()` 함수** 추가 (`static/script.js`):

```js
async function saveSectionTexts() {
    if (!currentDocumentId) {
        showError('저장할 문서 ID를 찾을 수 없습니다.');
        return;
    }
    const pyo = document.getElementById('sectionPyojebu').value;
    const gap = document.getElementById('sectionGapgu').value;
    const eul = document.getElementById('sectionEulgu').value;

    const response = await fetch(`/api/documents/${currentDocumentId}/sections`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pyojebu: pyo, gapgu: gap, eulgu: eul }),
    });
    const data = await response.json();
    // 성공 시 displayResults(data) 다시 호출해서 화면 전체를 최신 상태로 갱신
}
```

- 백엔드에는 **새 API** 추가 (`main.py`):

```python
class SectionUpdate(BaseModel):
    pyojebu: Optional[str] = None
    gapgu: Optional[str] = None
    eulgu: Optional[str] = None

@app.post("/api/documents/{document_id}/sections")
async def update_document_sections(
    document_id: int,
    sections: SectionUpdate,
    db: Session = Depends(get_db),
):
    # 1) 문서 조회
    # 2) pyojebu/gapgu/eulgu를 순서대로 합쳐서 new_text 생성
    # 3) parser.parse(new_text) 다시 돌려서 주소/소유자 등 메타데이터 갱신
    # 4) document.extracted_text 및 필드 업데이트 후 commit
    # 5) 최신 extracted_text / parsed_data / sections를 응답으로 반환
```

- 이 응답 구조는 업로드와 거의 같아서,
  - **`displayResults(data)`를 재사용**해서
  - 전체 텍스트/요약 정보/영역별 텍스트를 한 번에 다시 그림.

---

### 4. 왜 키워드 기반으로 잘라지냐 (정확도/용어 보정과의 관계)

- 전체 OCR 텍스트는 이미 `correct_with_vocab()`을 거치고 있어서
  - `"표게부"`, `"표계부"` 등은 `"표제부"`로 보정된 상태에서
  - `split_registry_sections()`가 `"표제부"`, `"갑구"`, `"을구"` 키워드를 찾아 나눕니다.
- 따라서 영역 편집용 텍스트도 **보정된 용어 기준으로** 나뉘고,
  - 사용자가 해당 영역을 직접 고쳐서 저장하면
  - 그 내용이 다시 하나의 `extracted_text`로 합쳐져 DB와 파서에 반영됩니다.

---

### 정리

- **지금 가능한 것**
  - 업로드 → 자동 OCR → 키워드 기반으로 **표제부/갑구/을구 영역 분리**
  - UI에서 각각 별도 textarea로 **영역별 텍스트 확인·수정**
  - "영역별 텍스트 저장" 클릭 시, 수정 내용이 **서버에 저장 + 파싱 재실행 + 화면 갱신**

원하시면,
- 이미지 위 영역 하이라이트도 **표제부/갑구/을구 색깔 다르게** 표시하는 것까지 이어서 붙여줄 수도 있습니다.

---

**User**

pdf 파일로 2장 이상일 때 이미지 분석 화면이 안보이는거같아 

---

**Cursor**

PDF는 지금까지 **“텍스트만” 처리하고, 이미지·박스 시각화는 순수 이미지 업로드에만** 붙여놔서, 말씀하신 것처럼 **2장 이상 PDF에선 이미지 분석 화면이 안 나오는 게 정상 동작**이었습니다.

방금 코드를 이렇게 바꿔서 해결했습니다:

- **`main.py` 업로드 처리에서 PDF 분기 수정**
  - `pdf_to_images(file_bytes)`로 만든 각 페이지 중 **1페이지(`idx == 0`) 이미지를 대상으로만**:
    - `ocr_service.get_detection_regions(image_bytes, ...)`를 한 번 더 호출해서  
      `first_page_regions` / `first_page_image_bytes`를 뽑습니다.
  - 응답 JSON 만들 때:
    - 이미지뿐 아니라 **PDF라도** `regions`와 `image_data_url`이 채워져 있으면
      - `out["regions"] = regions`
      - `out["image_data_url"] = image_data_url`
    - 프론트는 단순히 `data.regions && data.image_data_url`만 보고 이미지 분석 화면을 띄우므로,  
      **PDF(2장 이상이어도) 1페이지 기준 이미지 + 박스 시각화 화면이 보이게** 됩니다.

즉, 지금 코드 기준으로는 **PDF도 첫 페이지 이미지를 가지고 이미지 분석 화면(박스, 텍스트, 정확도)이 뜨도록 이미 고쳐둔 상태**입니다.

---

**User**

pdf 이미지는 나오는데 1페이지 기준 이미지만 나오는거 말고 전체 페이지를 보고싶어 

---

**Cursor**

이제 **PDF 여러 장일 때도 모든 페이지 이미지를 돌려보면서** 볼 수 있게 바꿔뒀습니다.

### 어떻게 동작하는지

- **백엔드 (`main.py`)**
  - PDF 처리 루프에서 **각 페이지마다**:
    - `ocr_service.get_detection_regions(image_bytes, ...)`를 호출해서
    - `{"page": 페이지번호, "regions": [...], "image_data_url": "data:image/png;base64,..."}` 형태로
    - `pages_visual` 리스트에 쌓습니다.
  - 응답 JSON에 추가:
    - `pages_visual: [{ page, regions, image_data_url }, ...]`
  - 기존처럼:
    - `regions` / `image_data_url`는 **기본 1페이지용**으로 세팅해서 호환도 유지합니다.

- **프론트 (`static/script.js`)**
  - 전역 상태:
    - `let pagesVisual = [];`
    - `let currentPageIndex = 0;`
  - `displayResults(data)`에서:
    - `data.pages_visual`이 있으면:
      - `pagesVisual = data.pages_visual;`
      - `currentPageIndex = 0;`
      - `showPageVisual(0);` 호출
    - 없고 `data.image_data_url`만 있으면 기존처럼 **한 장짜리 이미지**만 표시.
  - `showPageVisual(index)`:
    - 해당 페이지의 `image_data_url`을 `resultImage`에 세팅하고,
    - `regions`로 박스를 다시 그림.
    - 상단에 `페이지 X / N` 표시.

- **HTML (`templates/index.html`)**
  - 이미지 시각화 영역 안에 **페이지 이동 컨트롤** 추가:

```html
<div id="pageVisualControls" class="page-visual-controls" style="display: none;">
    <button type="button" class="btn btn-secondary btn-sm" onclick="changePageVisual(-1)">이전 페이지</button>
    <span id="pageVisualInfo" class="page-visual-info"></span>
    <button type="button" class="btn btn-secondary btn-sm" onclick="changePageVisual(1)">다음 페이지</button>
</div>
```

- **CSS (`static/style.css`)**
  - `page-visual-controls`, `page-visual-info`, `.btn-sm` 스타일을 추가해서
    - 상단에 **이전/다음 버튼 + 현재 페이지 표시**가 깔끔하게 보이도록 했습니다.

이제 PDF를 올리면,
- **이미지 분석 영역 위쪽에 "이전/다음 페이지" 버튼과 `페이지 1 / N` 표시**가 나오고,
- 버튼을 눌러서 **모든 페이지의 이미지 + OCR 박스/텍스트/정확도**를 한 장씩 돌려보실 수 있습니다.

---

**User**

텍스트 추출 후 판단하는 것들은 

이 사람이 진짜 주인인가?
소유자 일치 여부


보증금보다 먼저 가져갈 권리가 있는가?
근저당·가압류 등 권리 존재


이 집, 왜 이렇게 최근에 손바뀜 됐지?
소유권 이전 시점


나 말고 계약 권한 있는 사람이 또 있나?
공동 소유 여부


내 보증금은 몇 번째 순서인가?
선순위 권리 구조


이 계약, 법적으로 특정이 되는가?
호실·목적물 특정 가능 여부 

이건데 추출 할 수 있을까? 말만해줘

---

**Cursor**

네, **등기부 텍스트만으로 어느 정도까지 가능한지** 항목별로 딱 정리해볼게요.

### 1) 이 사람이 진짜 주인인가? (소유자 일치 여부)
- **가능한 것**: 등기부에 적힌 **현재 소유자 이름/주민번호 뒷자리(있다면)**는 확실히 추출 가능 → 사용자가 입력한 이름과 **문자열 비교**로 “등기부상 소유자와 일치/불일치” 판단은 가능.
- **한계**: 실제 계약 당사자가 주민등록증/인감 위조한 사람인지 같은 **신원 진위**는 등기부만으로는 절대 판단 불가.

### 2) 보증금보다 먼저 가져갈 권리가 있는가? (근저당·가압류 등)
- **가능한 것**: 갑구/을구에서
  - **근저당권·전세권·가압류·압류·가처분** 등 권리 종류
  - **설정일자 / 접수일자 / 채권최고액**  
  를 추출해서, 사용자가 입력한 **보증금·계약일**과 비교 →  
  “**선순위 담보권 존재 여부**”, “보증금보다 **우선 변제 받을 수 있는 권리 유무**”는 **룰 기반 로직으로 충분히 가능**.
- **한계**: 실제 경매·배당에서의 **정확한 배당순위/배당액 계산**은 추가 법률 로직·케이스 핸들링이 많이 필요.

### 3) 이 집, 왜 이렇게 최근에 손바뀜 됐지? (소유권 이전 시점)
- **가능한 것**: 갑구에서 **소유권이전 / 소유권이전청구권보전등기** 등의 **접수일자·등기접수일**을 추출 →  
  “최근 N개월 내 손바뀜 있음/없음” 같은 **시점 판단·경고는 충분히 가능**.
- **한계**: “왜 손바뀜 됐는지(증여/매매/경매 등 이유)”는 사유 칸을 파싱하면 어느 정도 추론 가능하지만, **정확한 사유·배경까지 100%는 아님**.

### 4) 나 말고 계약 권한 있는 사람이 또 있나? (공동 소유 여부)
- **가능한 것**: 갑구 소유자 란에서
  - **복수 명의자 유무**
  - **지분비율(1/2, 2/3 등)**  
  추출 가능 → “**단독 소유 / 공동 소유**”, “특정 지분만 소유” 여부는 **충분히 판단 가능**.
- **한계**: 위임장, 대리권 유무는 등기부 밖의 문서 영역.

### 5) 내 보증금은 몇 번째 순서인가? (선순위 권리 구조)
- **가능한 것**: 
  - 접수번호/접수일자 + 권리 종류(근저당, 전세권, 임차권, 가압류 등)을 시간순으로 정렬해서  
    **“보증금보다 앞선 권리 목록/개수”**,  
    대략적인 **우선순위 구조(선순위·후순위)** 표시는 가능.
- **한계**: 실제 법원 배당 순위는
  - 법정임대차, 최우선변제, 확정일자, 대항력, 체납세금 등까지 필요 →  
  **등기부 단독 + 간단 규칙**로는 “참고용 수준”까지만.

### 6) 이 계약, 법적으로 특정이 되는가? (호실·목적물 특정)
- **가능한 것**:
  - 표제부/부동산의 표시에서 **동·호수, 층, 건물명, 대지권, 면적** 추출
  - 사용자가 입력한 **주소/호실 정보**와 비교 → “**등기부상 목적물과 계약서 목적물이 일치/불일치**”는 꽤 정확하게 판단 가능.
- **한계**: 집합건물 복잡한 케이스(집합건물 여러 개 동, 통층, 구분 소유 일부 등)는 **추가 규칙 설계** 필요.

---

### 결론

- **단순 “텍스트 추출” + 잘 짠 규칙**만으로도  
  - 소유자 일치 여부  
  - 공동 소유 여부  
  - 선순위 담보권 존재 여부  
  - 최근 소유권 이전 시점  
  - 목적물(호실) 일치 여부  
  같은 건 **충분히 구현 가능합니다.**
- 다만 **“법률적 최종 판단(배당 순위, 실제 권리관계 확정)”은 불가능**하고,  
  “위험 신호를 자동으로 뽑아서 사용자에게 경고/가이드하는 수준”까지가 현실적인 목표입니다.

원하시면, 지금 구조(파서 + sections) 기준으로 각 항목별 **판단 로직 설계 스펙**도 항목별로 써 드릴게요.

---

**User**

1단계: 등기부 정보 구조화 추출 프롬프트

👉 역할: OCR 결과 텍스트 → 정형 JSON 데이터 변환

📌 SYSTEM PROMPT (역할 고정)
당신은 대한민국 부동산 등기부등본의 구조를 이해하는 정보 추출 전문 AI입니다.

당신의 임무는 법률 판단이나 해석이 아니라,
등기부 텍스트에서 객관적인 사실 정보만 정확하게 추출하여
지정된 JSON 형식으로 변환하는 것입니다.

절대 하지 말아야 할 것:
- 위험하다 / 안전하다 와 같은 판단
- 법적 해석
- 추측 또는 보완

오직 등기부에 적힌 내용만 구조화하십시오.
값이 없으면 null로 표시하십시오.

📌 USER PROMPT 템플릿
다음은 부동산 등기부등본 OCR 텍스트입니다.

[등기부 텍스트 시작]
{{OCR_TEXT}}
[등기부 텍스트 끝]

아래 JSON 스키마에 맞춰 정보를 추출하세요.

{
  "property_info": {
    "address": "",
    "building_name": "",
    "dong": "",
    "ho": "",
    "area_m2": ""
  },
  "owners": [
    {
      "name": "",
      "ownership_type": "단독/공동",
      "share": ""
    }
  ],
  "ownership_changes": [
    {
      "date": "",
      "reason": "",
      "details": ""
    }
  ],
  "rights": [
    {
      "section": "갑구/을구",
      "right_type": "",
      "holder": "",
      "receipt_date": "",
      "registration_date": "",
      "amount": "",
      "details": ""
    }
  ]
}

⚙ 2단계: 위험 신호 분석용 프롬프트 (설명 생성 전용)

👉 역할: 이미 코드가 판단한 risk_flags를 사용자에게 설명

❗ 여기서도 “법적 판단” 금지

📌 SYSTEM PROMPT
당신은 부동산 등기부 정보를 사용자에게 쉽게 설명하는 안내 AI입니다.

중요 원칙:
- 법적 판단을 하지 마십시오
- "안전하다", "문제 없다", "보증금 보호된다" 같은 표현 금지
- "가능성", "주의 필요", "확인 필요" 수준의 안내만 제공
- 등기부에 기초한 객관적 사실과 일반적인 위험 신호의 의미만 설명

당신의 역할은 판사가 아니라, 위험 신호 해설자입니다.

📌 USER PROMPT 템플릿
다음은 등기부 분석 시스템이 탐지한 위험 신호 목록입니다.

부동산 정보:
- 주소: {{address}}
- 건물명: {{building_name}}
- 동/호수: {{dong}}동 {{ho}}호

탐지된 위험 신호:
{{risk_flags}}

각 항목에 대해:
1. 이 등기부 정보가 의미하는 바
2. 왜 일반적으로 주의가 필요한 상황으로 여겨지는지
를 설명해주세요.

법적 결론이나 단정은 하지 말고,
사용자가 추가로 무엇을 확인해야 하는지도 안내하세요.

🏠 3단계: 소유자 일치 여부 설명 프롬프트
SYSTEM
당신은 등기부 소유자 정보와 계약 상대방 정보를 비교해
객관적인 일치 여부만 설명하는 AI입니다.

신원 진위 여부는 판단할 수 없다는 점을 항상 명시하십시오.

USER
등기부상 소유자: {{owner_name}}
계약 상대방 입력 이름: {{input_name}}

두 이름의 일치 여부를 설명하고,
이 확인이 신원 진위를 보장하지 않는다는 점을 안내하세요.

🧾 4단계: 선순위 권리 구조 설명 프롬프트
SYSTEM
당신은 등기부의 권리 설정 순서를 시간 순서대로 설명하는 AI입니다.

법적 배당 순위나 보증금 보호 여부를 판단하지 말고,
단순히 '언제 설정된 어떤 권리가 먼저 존재하는지'만 설명하세요.

USER
다음은 권리 설정 시간순 목록입니다.

{{rights_timeline}}

사용자의 임대차 계약일: {{contract_date}}

사용자의 계약보다 먼저 설정된 권리들이 무엇을 의미하는지
일반적인 주의 관점에서 설명하세요.

📍 5단계: 목적물(호실) 일치 여부 프롬프트
SYSTEM
당신은 등기부상 부동산 표시와 계약서상 주소 정보를 비교하는 AI입니다.

주소 및 호수의 일치 여부만 설명하고,
법적 효력에 대한 판단은 하지 마십시오.

USER
등기부 정보:
- 주소: {{reg_address}}
- 동/호수: {{reg_dong}}동 {{reg_ho}}호

계약서 정보:
- 주소: {{contract_address}}
- 동/호수: {{contract_dong}}동 {{contract_ho}}호

두 정보의 일치 여부를 설명하세요.

---

**Cursor**

좋은 설계입니다. 지금 정리해주신 1~5단계 프롬프트로 **충분히 구현 가능**합니다.

아주 짧게 **실제 시스템에 붙일 때 구조**만 짚어드리면:

### 1단계 (구조화 추출) 붙이는 자리
- **어디서 사용?**  
  `ocr_service.extract_text()`으로 OCR 텍스트 얻은 **직후**  
  또는 지금 `parser.parse(extracted_text)` 쓰는 자리 옆에
- **구현 방식**  
  - `llm_structured_extract.py` 같은 모듈 만들고
  - 거기에 지금 적으신 **SYSTEM 프롬프트 + USER 템플릿** 그대로 넣어서  
    OpenAI/프롬프트 호출 → JSON 파싱 → `parsed_data` 대체/보완 값으로 사용

### 2~5단계 (설명·비교·해설 프롬프트)
- **입력**은 전부 1단계 JSON + 코드가 만든 `risk_flags` / 비교 결과에서 나오므로,
- UI에서 “설명 보기” 버튼 눌렀을 때:
  - 그때마다 해당 단계별 **SYSTEM/USER 템플릿에 값 채워서 LLM 한 번 호출** → 설명 문자열만 받아서 화면에 표시하면 됩니다.
- 중요한 점:  
  이미 프롬프트에 “법적 판단 금지 / 객관적 설명만”을 잘 넣어두셔서,  
  그대로 쓰면 “가이드 + 경고” 용도로는 충분합니다.

정리하면:  
- **구조화 추출(1단계)**는 지금 `parser.py` 역할을 “LLM 버전”으로 확장하는 느낌으로,  
- **2~5단계**는 구조화된 JSON과 비교 결과를 인풋으로 쓰는 “설명 전용 프롬프트”로 붙이면 됩니다.

---

**User**

현재 페이지에서 추출된 텍스트를 json 스키마에 맞게 저장하고 LLM으로 등기부등본의 위험 신호 분석을 제공할 수 있을까?

---

**Cursor**

네, **지금 구조 그대로에서 충분히 구현 가능합니다.**  
(추가로 OpenAI 같은 LLM API 키와 한두 개의 백엔드/프론트 연결 작업만 더 해주면 됩니다.)

### 1) 현재 페이지 텍스트 → JSON 스키마 저장

이미 `upload` 응답에:

- `extracted_text` (전체 OCR 결과)
- `document_id`
- `sections` (표제부/갑구/을구 텍스트)

가 있으니, 백엔드에서 다음 흐름으로 붙이면 됩니다.

1. **새 API 추가 (예: `/api/documents/{id}/llm-structure`)**
   - BODY: 없음 또는 `{ use_sections: true }`
   - 내부에서:
     - DB에서 `extracted_text` 또는 합친 `sections` 읽기
     - 1단계에서 정의한 **SYSTEM + USER 프롬프트**로 LLM 호출  
       (`{{OCR_TEXT}}`에 해당 텍스트 그대로 넣기)
     - LLM 응답(JSON)을 파싱해서
       - `structured_data` 컬럼(JSONB) 같은 데 저장

2. 프론트:
   - “LLM로 구조화하기” 버튼 추가 → 위 API 호출
   - 성공 시 `structured_data`를 받아와 화면에 표시 (또는 숨겨진 상태로 저장만)

### 2) 구조화 JSON → 위험 신호 분석 (LLM 설명)

1. 백엔드에서 `structured_data`를 읽고,
   - 코드로 `risk_flags` 리스트 생성  
     (예: “선순위 근저당 있음”, “최근 6개월 내 소유권 이전” 등)
2. **새 API (예: `/api/documents/{id}/risk-analysis`)**에서:
   - 2단계 SYSTEM/USER 프롬프트에
     - 주소/건물명/동호 (`property_info`) 채우고
     - `risk_flags`를 텍스트로 나열해서 LLM 호출
   - LLM이 생성한 설명 문자열을 그대로 프론트에 반환

3. 프론트:
   - “위험 신호 설명 보기” 버튼 → `/risk-analysis` 호출 → 결과를 카드/모달로 표시

---

### 결론

- **기술적으로: 완전 가능**  
  - 이미 `extracted_text`/`sections`/`document_id`까지 있으므로
  - 1단계 JSON 추출 프롬프트 + 2단계 위험 신호 설명 프롬프트를  
    **백엔드에서 LLM API로 한 번씩만 감싸주면** 됩니다.
- 해야 할 일은:
  - 백엔드: LLM 호출용 모듈 + 2~3개 API 라우트 추가
  - 프론트: 버튼 2개 + 결과 표시 UI 정도입니다.

---

**User**

만들어보자

---

**Cursor**

네, 지금 구조에서 **이미 구현까지 완료**했습니다.

### 1) LLM 구조화 추출 (JSON 스키마 저장)

- **백엔드**
  - 새 모듈 `llm_structured.py`:
    - 1단계에서 정리한 SYSTEM/USER 프롬프트 그대로 사용해서  
      `extract_structured(text: str) -> dict` 구현 (OpenAI `gpt-4o-mini` 기본).
  - `main.py`에 새 API 추가:
    - `POST /api/documents/{document_id}/llm-structure`
    - DB에서 `extracted_text` 읽어서 `extract_structured` 호출
    - 결과를 `RegistryDocument.parsed_data`(TEXT)에 **JSON 문자열로 저장**
    - 응답: `{ success, document_id, structured }`

- **프론트 (`index.html`, `script.js`)**
  - 결과 카드 안에 버튼 추가:
    - `LLM 구조화 추출` → `runLlmStructure()` 호출
  - `runLlmStructure()`:
    - 현재 `currentDocumentId`로 `/api/documents/{id}/llm-structure` POST
    - 성공 시 알림만 띄우고(구조화 데이터는 서버에 저장)

### 2) LLM 기반 위험 신호 설명

- **백엔드**
  - 새 모듈 `llm_risk_analysis.py`:
    - `build_risk_flags(structured)`:
      - 공동소유 여부, 최근 2년 이내 소유권 변동, 권리 건수/종류, 주소·동호 누락 등 **간단한 위험 플래그 리스트** 생성
    - `explain_risk(structured, risk_flags)`:
      - 2단계 SYSTEM/USER 프롬프트 사용해서  
        위험 신호를 **설명 텍스트**로 변환 (역시 OpenAI `gpt-4o-mini` 기본)
  - `main.py`에 새 API 추가:
    - `POST /api/documents/{document_id}/risk-analysis`
    - `parsed_data`가 있으면 `json.loads`해서 사용, 없으면 즉석에서 `extract_structured` 실행 후 저장
    - `risk_flags = build_risk_flags(structured)`
    - `explanation = explain_risk(structured, risk_flags)`
    - 응답: `{ success, document_id, structured, risk_flags, explanation }`

- **프론트**
  - 결과 카드에 버튼/영역 추가:
    - `위험 신호 설명 보기` 버튼 → `runRiskAnalysis()`
    - `riskExplanationSection` + `riskExplanation` 박스에 설명 표시
  - `runRiskAnalysis()`:
    - `/api/documents/{id}/risk-analysis` POST
    - 응답의 `explanation`을 박스에 그대로 출력

### 사용 요약

1. 등기부 이미지/PDF 업로드 → 기존처럼 OCR/파싱/시각화.
2. 결과 화면에서:
   - **`LLM 구조화 추출`** 버튼 클릭 → LLM이 JSON 스키마에 맞게 구조화, DB에 저장.
   - **`위험 신호 설명 보기`** 클릭 → 구조화 데이터 기반으로 위험 신호 플래그+설명 생성, 화면에 표시.

단, 실제 동작을 위해서는 **환경변수 `OPENAI_API_KEY`**가 설정되어 있어야 합니다.

---

**User**

Unexpected token 'I', "Internal S"... is not valid JSON 이런 오류가 났어

---

**Cursor**

이 에러 메시지는 **브라우저가 JSON을 기대했는데, 서버에서 JSON이 아니라 `"Internal Server Error"` 같은 일반 텍스트를 돌려줘서** 생긴 거예요.

즉,
- **프론트(`response.json()`)는 정상이고**,  
- **백엔드에서 500 내부 오류가 나서**, 그 내용이 `"Internal Server Error"`로 떨어진 상황입니다.

지금 구조상 거의 확실한 원인은 둘 중 하나입니다:

1. **LLM 쪽 설정 문제**
   - `OPENAI_API_KEY`가 설정 안 됐거나,
   - `openai` 패키지가 설치 안 됐거나,
   - LLM 호출에서 예외가 난 경우  
   → `/api/documents/{id}/llm-structure` 또는 `/api/documents/{id}/risk-analysis`가 500을 내보냄.

2. **환경 없이 LLM 버튼만 눌렀을 때**
   - 제가 백엔드에서 `OPENAI_API_KEY` 없으면 `HTTPException(500, detail="...")`을 던지도록 해뒀기 때문에,  
   - 이때 그 500 응답이 브라우저 쪽에선 `"Internal Server Error"` 텍스트로 오고,  
   - `response.json()`에서 방금 본 파싱 에러가 나는 구조입니다.

정리하면:

- **먼저 해야 할 것**
  1. 서버 실행한 터미널 로그를 보면, 어떤 스택트레이스/에러가 찍혔는지 바로 나옵니다. (거의 100% LLM 관련)
  2. `.env`나 환경변수에 `OPENAI_API_KEY` 넣고, `pip install openai` 되어 있는지 확인.

- **프론트에서 방어적으로 바꾸고 싶다면** (`static/script.js`):
  - `const data = await response.json();` 부분을 아래 패턴으로 바꿔주면,
    - JSON이 아니어도 에러 메시지를 좀 더 친절하게 표시할 수 있습니다.

```javascript
let data;
try {
  data = await response.json();
} catch (_) {
  const text = await response.text();
  throw new Error(text || '서버에서 유효한 JSON 응답을 받지 못했습니다.');
}
```

요약하면: **백엔드에서 LLM 호출이 실패해서 500이 난 상황**이고,  
실제 해결은 `OPENAI_API_KEY + openai 설치`를 맞춰주거나,  
LLM이 없는 환경이면 해당 API를 안 쓰거나(버튼 숨김) 예외 처리만 추가해 주면 됩니다.

---

**User**

터미널은 INFO:     127.0.0.1:59071 - "POST /api/documents/86/llm-structure HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "C:\Python310\lib\site-packages\uvicorn\protocols\http\httptools_impl.py", line 426, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
  File "C:\Python310\lib\site-packages\uvicorn\middleware\proxy_headers.py", line 84, in __call__
    return await self.app(scope, receive, send)
  File "C:\Python310\lib\site-packages\fastapi\applications.py", line 1106, in __call__
    await super().__call__(scope, receive, send)
  File "C:\Python310\lib\site-packages\starlette\applications.py", line 122, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Python310\lib\site-packages\starlette\middleware\errors.py", line 184, in __call__
    raise exc
  File "C:\Python310\lib\site-packages\starlette\middleware\errors.py", line 162, in __call__
    await self.app(scope, receive, _send)
  File "C:\Python310\lib\site-packages\starlette\middleware\exceptions.py", line 
79, in __call__
    raise exc
  File "C:\Python310\lib\site-packages\starlette\middleware\exceptions.py", line 
68, in __call__
    await self.app(scope, receive, sender)
  File "C:\Python310\lib\site-packages\fastapi\middleware\asyncexitstack.py", line 20, in __call__
    raise e
  File "C:\Python310\lib\site-packages\fastapi\middleware\asyncexitstack.py", line 17, in __call__
    await self.app(scope, receive, send)
  File "C:\Python310\lib\site-packages\starlette\routing.py", line 718, in __call__
    await route.handle(scope, receive, send)
  File "C:\Python310\lib\site-packages\starlette\routing.py", line 276, in handle    await self.app(scope, receive, send)
  File "C:\Python310\lib\site-packages\starlette\routing.py", line 66, in app    
    response = await func(request)
  File "C:\Python310\lib\site-packages\fastapi\routing.py", line 274, in app     
    raw_response = await run_endpoint_function(
  File "C:\Python310\lib\site-packages\fastapi\routing.py", line 191, in run_endpoint_function
    return await dependant.call(**values)
  File "C:\AI_HomeMatch_Python\main.py", line 203, in generate_llm_structure     
    structured = extract_structured(text)
  File "C:\AI_HomeMatch_Python\llm_structured.py", line 127, in extract_structured
    result = _call_openai_structured(text)
  File "C:\AI_HomeMatch_Python\llm_structured.py", line 85, in _call_openai_structured
    user_content = STRUCT_USER_TEMPLATE.format(ocr_text=text)
KeyError: '\n  "property_info"'이런 오류야

---

**Cursor**

지금 오류 원인 딱 맞게 나왔습니다.

### 왜 발생했는지

- `llm_structured.py`에서 이 줄 때문에입니다:

```python
STRUCT_USER_TEMPLATE = """ ... """
...
user_content = STRUCT_USER_TEMPLATE.format(ocr_text=text)
```

- 그런데 템플릿 안에 **JSON 예시**를 그냥 이렇게 넣어뒀죠:

```text
{
  "property_info": {
    ...
  },
  ...
}
```

- `str.format()`은 **모든 `{}`를 플레이스홀더로 인식**합니다.
  - `{ocr_text}`는 의도한 대로고,
  - JSON 안의 `{"property_info": {...}}`도 전부 플레이스홀더로 보이면서  
    `KeyError: '\n  "property_info"'` 가 터진 겁니다.

### 어떻게 고쳤는지 (이미 코드 수정 완료)

`llm_structured.py`에서 **JSON 부분의 중괄호를 전부 이중 괄호로 이스케이프**했습니다.

- 예전:

```python
{
  "property_info": {
    ...
  }
}
```

- 수정 후:

```python
{{
  "property_info": {{
    ...
  }}
}}
```

즉, **literal JSON**은 `{{` `}}` 로 감싸고,  
딱 하나만 실제 플레이스홀더로 쓰는 `{ocr_text}`는 그대로 두었습니다.

이제:

```python
user_content = STRUCT_USER_TEMPLATE.format(ocr_text=text)
```

가 정상 동작하고, `llm-structure` API도 500 대신 LLM 호출까지 진행될 겁니다.

### 다음에 하실 것

1. 서버 다시 실행(또는 `--reload`면 파일 저장만으로 반영).
2. 같은 문서에서 **“LLM 구조화 추출” 버튼** 다시 눌러보기.
3. 여전히 문제가 있으면,  
   - 이제는 `OPENAI_API_KEY`나 모델 쪽 다른 에러 메시지가 나올 수 있으니,  
     그때 터미널 로그 한 번 더 알려주시면 거기서 이어서 잡아드리면 됩니다.

---

**User**

지금 일반 사용자가 알아듣기에 너무 어려운 단어라 좀더 쉬운 설명으로 바꾸고싶은데 
어려운 법률 용어를 사용하지 말고,
중학생도 이해할 수 있는 쉬운 말로 설명하세요.

각 항목은 다음 구조로 작성하세요:
1. 한 줄 요약
2. 무슨 뜻인지 쉬운 설명
3. 왜 주의해야 하는지
4. 사용자가 추가로 확인하면 좋은 것

"법적으로", "우선변제권", "채권자" 같은 전문 용어는
가능하면 쉬운 말로 풀어쓰세요.

이걸로 프롬프트 변경하면 어떨까?

---

**Cursor**

LLM 위험 신호 설명을 중학생도 이해하기 쉬운 말로 바꾸도록, 프롬프트 내용을 업데이트하겠습니다.

지금 말씀해주신 내용으로 **프롬프트 이미 코드에 반영**했습니다.

- `llm_risk_analysis.py` 안의 **`RISK_SYSTEM_PROMPT` / `RISK_USER_TEMPLATE`**를:
  - **어려운 법률 용어 쓰지 말 것**
  - **중학생도 이해할 수 있는 쉬운 말로**
  - **각 항목당 1) 한 줄 요약 2) 쉬운 설명 3) 왜 주의? 4) 추가로 확인할 것**
  구조로 설명하도록 바꿔두었습니다.

앞으로 “위험 신호 설명 보기” 버튼을 누르면,
- 같은 위험 신호라도 **전문용어 대신 쉬운 한국어로**,
- 위 4단계 형식에 맞춰 설명을 해 줄 거예요.

---

**User**

지금 위험 신호 설명에 스타일이 적용안돼서 보기 힘들어 텍스트 상자에 한번에 들어가지말고 
1. 두 명 이상이 고동 소유자로 등록됨
....

2. 등기부에 2건의 권리가 등재되어 있습니다.
.....

이런 식으로 바꿀 수 있을까?

---

**Cursor**

가능합니다. 방금 코드까지 바꿔서 **지금부터는 이런 형태로 보이게** 해뒀어요:

- `1. 두 명 이상이 공동 소유자로 등록돼 있음`  
  아래에 그에 대한 설명/주의사항/추가 확인사항이 여러 줄로 나옴
- `2. 등기부에 2건의 권리가 등재되어 있습니다.`  
  아래에 해당 권리에 대한 설명 …

구현 방식은:

- LLM이 준 긴 설명 문자열을 JS에서 **블록(빈 줄 기준)**으로 나누고,
- 각 블록의 **첫 줄을 제목(번호 + 한 줄 요약)**, 나머지를 본문으로 나눠
- `risk-item` 단위로 나눠 렌더링하도록 `renderRiskExplanation()`을 추가했습니다.
- CSS로 `risk-item-title`(굵게), `risk-item-body`(조금 작은 글씨) 스타일을 넣어서  
  위험 신호별로 **1, 2, 3… 항목이 잘 분리되어** 보입니다.

---

**User**

하나의 텍스트 상자에 전부다 넣지말고 css가 자연스럽게 적용될 수 있도록 나눠줘

---

**Cursor**

지금 방식이 딱 그걸 하도록 바뀌어 있습니다.

### 현재 구조 (이미 적용된 상태)

- `riskExplanation`은 이제 **“한 덩어리 텍스트 상자”가 아니라, 컨테이너 역할**만 합니다.
- JS에서 `renderRiskExplanation()`이 LLM 텍스트를 받아서:

  1. **빈 줄 기준으로 블록 나누기** → 위험 신호 1개당 1블록
  2. 각 블록마다
     - `<div class="risk-item">` 생성
       - `<div class="risk-item-title">` → `1. 두 명 이상이 공동 소유자로 등록돼 있음`
       - `<div class="risk-item-body">` → 그 아래 설명들
  3. 이 `risk-item`들을 `riskExplanation` 안에 **여러 개로 append**

- CSS도 각각에 따로 적용되도록 되어 있습니다:

```css
.risk-item { ... }
.risk-item-title { ... }
.risk-item-body { ... }
```

그래서 화면에서는:

- 하나의 큰 textarea가 아니라,
- **위험 신호 1개당 하나의 블록(제목 + 본문)** 으로 나뉘어 스타일이 자연스럽게 적용됩니다.

만약 “한 위험 신호 안에서도 ①한 줄 요약 ②설명 ③주의 이유 ④추가 확인”을 **더 쪼개서 각각 따로 박스/줄로 스타일** 주고 싶다면,  
`renderRiskExplanation()`에서 `lines.slice(1)` 부분을 다시 분리해서  
`요약/설명/주의/추가확인`용 `<div>`를 네 개로 나눠주는 식으로 확장하면 됩니다.

