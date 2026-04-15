# 🌱 FARMER - 농업 병해충 AI 진단 플랫폼

농작물 병해충을 AI로 진단하고, 질병 정보를 조회하며, 농업인들이 소통할 수 있는 커뮤니티 게시판을 제공하는 웹 플랫폼입니다.

## 📌 주요 기능

| 기능 | 설명 |
|------|------|
| **AI 병해충 진단** | YOLOv5 기반 이미지 업로드 → 병해충 자동 탐지 및 결과 시각화 |
| **질병 도감** | 작물별 병해충 정보 (발생환경, 증상, 방제방법) 조회 |
| **커뮤니티 게시판** | 게시물 CRUD, 이미지 첨부, 댓글, 검색 기능 |

## 🏗 프로젝트 구조

```
Farmer/
├── backend/                 # Flask REST API 서버
│   ├── app.py               # 앱 팩토리 및 서버 엔트리포인트
│   ├── db_models.py         # SQLAlchemy 모델 (Post, Comment)
│   ├── extensions.py        # DB, Bcrypt 인스턴스
│   ├── requirements.txt     # Python 의존성
│   ├── yolov5s.pt           # YOLOv5 커스텀 모델 가중치
│   ├── uploads/             # 게시판 이미지 업로드 저장소
│   ├── routes/
│   │   ├── diagnosis.py     # POST /api/diagnosis/analyze
│   │   ├── board.py         # /api/board/posts CRUD + 댓글 + 검색
│   │   └── encyclopedia.py  # /api/encyclopedia/crops, diseases
│   └── services/
│       ├── model.py         # YOLO 모델 로딩/추론
│       ├── image_utils.py   # 바운딩박스, Base64 변환
│       └── disease_info.py  # 병해충 클래스별 한국어 정보
│
├── frontend/                # React + Vite SPA
│   ├── src/
│   │   ├── App.jsx          # 라우팅 설정
│   │   ├── main.jsx         # 앱 엔트리포인트
│   │   ├── index.css        # Tailwind CSS
│   │   ├── components/
│   │   │   ├── Navbar.jsx   # 네비게이션 바
│   │   │   └── Footer.jsx   # 푸터
│   │   └── pages/
│   │       ├── Home.jsx         # 메인 페이지
│   │       ├── Diagnosis.jsx    # AI 진단 (이미지 업로드 → 결과)
│   │       ├── Encyclopedia.jsx # 작물 목록
│   │       ├── CropDiseases.jsx # 작물별 질병 목록
│   │       ├── DiseaseDetail.jsx# 질병 상세 정보
│   │       ├── Board.jsx        # 게시판 목록/검색
│   │       ├── PostDetail.jsx   # 게시물 상세/댓글
│   │       ├── CreatePost.jsx   # 글쓰기
│   │       └── EditPost.jsx     # 글 수정
│   ├── vite.config.js       # Vite + Tailwind + API 프록시
│   └── package.json
│
└── README.md
```

## 🛠 기술 스택

### Backend
- **Python 3.13** / **Flask 3.x**
- **Flask-SQLAlchemy** + **PyMySQL** (MySQL)
- **Flask-Bcrypt** (비밀번호 해싱)
- **Flask-CORS** (Cross-Origin 허용)
- **PyTorch** + **YOLOv5** (커스텀 학습 모델, 17클래스)

### Frontend
- **React 19** + **Vite 8**
- **Tailwind CSS 4**
- **React Router 7**

### AI 모델
- **YOLOv5s** 커스텀 학습 모델
- 탐지 대상: 오이(노균병, 흰가루병), 호박(흰가루병, 점무늬병), 멜론(노균병, 흰가루병), 고추(연모틀바이러스), 토마토(TYLCV, 잎곰팡이병) 등 17클래스

## 🚀 실행 방법

### 사전 요구사항
- Python 3.10+
- Node.js 18+
- MySQL 서버 (database: `pages`, user: `page`)

> **터미널 2개**를 열어 백엔드와 프론트엔드를 **동시에** 실행해야 합니다.

### 1. Backend 실행 (터미널 1)

```bash
cd backend
pip install -r requirements.txt
python app.py
```
- Flask API 서버가 **http://localhost:5000** 에서 실행됩니다
- YOLO 모델 로딩에 수 초 소요 → `[완료] 모델 로딩 완료, 서버 준비됨` 메시지 확인

### 2. Frontend 실행 (터미널 2)

```bash
cd frontend
npm install      # 최초 1회만
npm run dev
```
- React 개발 서버가 **http://localhost:5173** 에서 실행됩니다
- `/api/*` 요청은 자동으로 백엔드(5000번)로 프록시됩니다
- 브라우저에서 **http://localhost:5173** 접속하여 사용

### 3. 프로덕션 빌드 (배포 시)

```bash
cd frontend
npm run build
# → dist/ 폴더에 정적 파일 생성
```

## 📡 API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| `POST` | `/api/diagnosis/analyze` | 이미지 업로드 → 병해충 진단 |
| `GET` | `/api/encyclopedia/crops` | 작물 목록 조회 |
| `GET` | `/api/encyclopedia/crops/:id/diseases` | 작물별 질병 목록 |
| `GET` | `/api/encyclopedia/diseases/:id` | 질병 상세 정보 |
| `GET` | `/api/board/posts` | 게시물 목록 |
| `POST` | `/api/board/posts` | 게시물 작성 |
| `GET` | `/api/board/posts/:id` | 게시물 상세 (조회수 증가) |
| `PUT` | `/api/board/posts/:id` | 게시물 수정 (비밀번호 필요) |
| `DELETE` | `/api/board/posts/:id` | 게시물 삭제 (비밀번호 필요) |
| `POST` | `/api/board/posts/:id/comments` | 댓글 작성 |
| `DELETE` | `/api/board/comments/:id` | 댓글 삭제 |
| `GET` | `/api/board/posts/search?q=` | 게시물 검색 |

## 🔮 프로젝트 비전 및 발전 방향

### 현재 프로젝트가 보여주는 가능성

이 프로젝트는 **AI + 농업** 융합의 실용적 프로토타입으로, 다음과 같은 미래를 제시합니다.

> 농업인이 스마트폰으로 작물 사진을 찍으면 즉시 병해충을 진단하고, 적절한 방제법을 안내받으며, 커뮤니티에서 경험을 공유하는 **스마트팜 생태계**

### 단기 발전 방향 (3~6개월)

| 분야 | 내용 |
|------|------|
| **모델 고도화** | 탐지 클래스 확대 (현재 17종 → 50종+), 정확도 개선, 실시간 영상 진단 |
| **모바일 최적화** | PWA 적용으로 앱 설치 없이 모바일에서 카메라 촬영 → 즉시 진단 |
| **사용자 인증** | 회원가입/로그인 시스템 도입, 진단 이력 관리 |
| **알림 시스템** | 지역별 병해충 발생 경보, 기상 연계 예방 알림 |

### 중장기 발전 방향 (6개월~2년)

| 분야 | 내용 |
|------|------|
| **드론/IoT 연동** | 드론 촬영 이미지 자동 분석, 센서 데이터(온도·습도·토양) 연계 종합 진단 |
| **방제 추천 AI** | 진단 결과에 따른 농약/유기농 방제법 자동 추천, 약제 살포 시기 예측 |
| **빅데이터 분석** | 지역·시기별 병해충 발생 패턴 분석, 예측 모델 구축 |
| **전문가 매칭** | 커뮤니티 내 농업 전문가 상담 연결, 실시간 Q&A |
| **다국어 지원** | 동남아 등 농업 개발도상국 진출을 위한 다국어 서비스 |

### 산업적 확장 가능성

```
┌─────────────────────────────────────────────────────────┐
│                   스마트팜 통합 플랫폼                      │
│                                                         │
│  📸 AI 진단  →  💊 방제 추천  →  🛒 농자재 연계 구매       │
│                                                         │
│  🌡 IoT 모니터링  →  📊 생육 분석  →  📈 수확량 예측       │
│                                                         │
│  👥 농업인 커뮤니티  →  🎓 교육 콘텐츠  →  💰 유통 연계     │
└─────────────────────────────────────────────────────────┘
```

- **농자재 이커머스 연동**: 진단 결과 → 필요 농약/비료 자동 추천 → 바로 구매
- **정부/지자체 연계**: 농업 기술센터 데이터 연동, 정책 지원 정보 제공
- **보험 연계**: AI 진단 기록을 기반으로 농작물 보험 심사 자동화
- **글로벌 확장**: 기후변화로 병해충 이슈가 커지는 전 세계 농업 시장 진출

### 기대 효과

| 효과 | 설명 |
|------|------|
| **조기 진단** | 육안 판별 불가능한 초기 병해 탐지로 피해 최소화 |
| **비용 절감** | 불필요한 농약 살포 감소, 정밀 방제로 30~50% 비용 절감 예상 |
| **접근성 향상** | 전문가 없이도 누구나 스마트폰으로 진단 가능 |
| **데이터 축적** | 전국 단위 병해충 데이터 수집 → 국가 농업 정책 수립 기초자료 |

## 📄 라이선스

이 프로젝트는 학습 목적으로 제작되었습니다.
