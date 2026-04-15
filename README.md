# 🌱 FARMER - YOLO를 활용한 병해충 진단 시스템

**나사렛대학교 IT융합학부 졸업작품 프로젝트**

농업 분야에서 병해충 진단을 위한 혁신적인 접근 방식을 제공하는 웹 애플리케이션입니다. 인공지능을 활용하여 병해충을 식별하고, 사용자가 이미지를 업로드하여 진단 결과를 획득할 수 있으며, 커뮤니티 게시판을 통해 농업인들 간 정보 교환 및 소통을 지원합니다.

---

## 📋 목차

1. [주요 기능](#-주요-기능)
2. [스크린샷](#-스크린샷)
3. [기술 스택](#-기술-스택)
4. [프로젝트 구조](#-프로젝트-구조)
5. [실행 방법](#-실행-방법)
6. [API 엔드포인트](#-api-엔드포인트)
7. [프로젝트 비전 및 발전 방향](#-프로젝트-비전-및-발전-방향)
8. [트러블슈팅](#-트러블슈팅)
9. [팀원](#-팀원)
10. [참고 문헌](#-참고-문헌)
11. [라이선스](#-라이선스)

---

## 📌 주요 기능

| 기능 | 설명 |
|------|------|
| **AI 병해충 진단** | YOLOv5 기반 이미지 업로드 → 병해충 자동 탐지 및 결과 시각화 |
| **질병 도감** | 작물별 병해충 정보 (발생환경, 증상, 방제방법) 조회 |
| **커뮤니티 게시판** | 게시물 CRUD, 이미지 첨부, 댓글, 검색 기능 |

## 📸 스크린샷

| 페이지 | 미리보기 |
|--------|----------|
| **메인 홈** | ![홈](docs/screenshots/home.png) |
| **AI 병해충 진단** | ![진단](docs/screenshots/diagnosis.png) |
| **진단 결과** | ![결과](docs/screenshots/result.png) |
| **질병 도감** | ![도감](docs/screenshots/encyclopedia.png) |
| **커뮤니티 게시판** | ![게시판](docs/screenshots/board.png) |
| **게시물 상세** | ![상세](docs/screenshots/post-detail.png) |

> 📌 스크린샷을 추가하려면 `docs/screenshots/` 폴더에 이미지를 넣으세요.

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
- **YOLOv5s** 커스텀 학습 모델 (PyTorch 프레임워크)
- **데이터 출처**: AI-Hub 시설 작물 질병 이미지
- **라벨링**: Polygon 기법으로 정교한 객체 식별
- **탐지 대상**: 고추, 단호박, 오이, 참외, 토마토 등 5개 작물의 병해충 17클래스

### 학습 데이터셋 및 정확도

| 작물 | 데이터 수 | 학습 | 검증 | 테스트 | 정확도 |
|------|-----------|------|------|--------|--------|
| 고추 | 2,536 | 2,206 | 202 | 128 | **80%** |
| 단호박 | 2,253 | 1,960 | 180 | 113 | **77%** |
| 오이 | 1,414 | 1,230 | 113 | 71 | **69%** |
| 참외 | 2,228 | 1,938 | 178 | 112 | **76%** |
| 토마토 | 2,714 | 2,361 | 217 | 136 | **78%** |
| **합계** | **11,145** | **9,695** | **890** | **560** | **평균 76%** |

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

## 🚀 실행 방법

### 사전 요구사항
- Python 3.10+
- Node.js 18+
- MySQL 서버 (database: `pages`, user: `page`)

> **터미널 2개**를 열어 백엔드와 프론트엔드를 **동시에** 실행해야 합니다.

### 0. 데이터베이스 초기 설정 (최초 1회)

MySQL에 접속하여 아래 SQL을 실행합니다:

```sql
-- 데이터베이스 및 사용자 생성
CREATE DATABASE IF NOT EXISTS pages DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'page'@'localhost' IDENTIFIED BY 'page';
GRANT ALL PRIVILEGES ON pages.* TO 'page'@'localhost';
FLUSH PRIVILEGES;

USE pages;

-- 게시물 테이블
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    author VARCHAR(255) NOT NULL,
    views INT DEFAULT 0,
    password_hash VARCHAR(60) NOT NULL,
    image VARCHAR(255)
);

-- 댓글 테이블
CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    post_id INT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);
```

> DB 접속 정보를 변경하려면 `backend/app.py`의 `SQLALCHEMY_DATABASE_URI`를 수정하세요.
> ```
> mysql+pymysql://유저명:비밀번호@호스트/데이터베이스명
> ```

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

### 프로젝트 배경

현재 농업은 많은 국가에서 중요한 산업이며, 젊은 층의 농업 종사자가 늘어나면서 병해충을 수월하게 진단할 수 있는 시스템이 필요합니다. 기존 농법으로는 다양한 변화에 대처하기 어려우며, 안전한 농산물 공급과 수급 안정화를 위한 새로운 기술 도입이 시급한 상황입니다.

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
| **비용 절감** | 정확한 진단으로 불필요한 농약 사용 최소화, 비용 절감 및 환경 보호 |
| **접근성 향상** | 전문가 없이도 누구나 스마트폰으로 진단 가능, 초보 농업인 지원 |
| **데이터 축적** | 전국 단위 병해충 데이터 수집 → 국가 농업 정책 수립 기초자료 |
| **경제적 안정** | 비용 감소 + 생산성 증대 → 농부 수익 증가 및 경제적 안정성 향상 |

## ❓ 트러블슈팅

<details>
<summary><b>ModuleNotFoundError: No module named 'flask_sqlalchemy'</b></summary>

```bash
pip install flask-sqlalchemy flask-bcrypt pymysql flask-cors
```
</details>

<details>
<summary><b>ModuleNotFoundError: No module named 'models.common' (YOLOv5 충돌)</b></summary>

`models.py`라는 파일명이 YOLOv5의 내부 `models` 패키지와 충돌합니다.  
이 프로젝트에서는 `db_models.py`로 이름을 변경하여 해결했습니다.
</details>

<details>
<summary><b>MySQL 연결 오류: No module named 'MySQLdb'</b></summary>

DB URI에 `+pymysql`을 추가해야 합니다:
```python
# ❌ 잘못된 예
'mysql://page:page@localhost/pages'

# ✅ 올바른 예
'mysql+pymysql://page:page@localhost/pages'
```
</details>

<details>
<summary><b>OMP: Error #15: Initializing libiomp5md.dll</b></summary>

`app.py` 상단에 이미 아래 코드가 포함되어 있습니다:
```python
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
```
</details>

<details>
<summary><b>프론트엔드에서 API 호출 시 CORS 에러</b></summary>

백엔드가 실행 중인지 확인하세요. Vite 프록시(`vite.config.js`)가 `/api/*` 요청을 `localhost:5000`으로 전달합니다.  
백엔드가 꺼져있으면 CORS 에러처럼 보일 수 있습니다.
</details>

## 👨‍💻 팀원

| 이름 | 담당 업무 | 연락처 |
|------|----------|--------|
| **이건창** | 이미지 라벨링, AWS 서버관리, 게시판 개발, YOLO 페이지 개발 | rjsckd822@naver.com |
| **신재호** | 이미지 라벨링, 프론트 웹 개발, 자료조사 | wogh014@naver.com |
| **김민한** | 이미지 라벨링, 게시판 개발, YOLO 페이지 개발 | minhan9653@naver.com |
| **박경호** | 이미지 라벨링, 프론트 웹 개발, 인공지능 학습, 자료조사 | qkrrud9327@naver.com |

> 나사렛대학교 IT융합학부 4학년 (2018년 입학)

## 📚 참고 문헌

1. 성경일 외, “ICT 기반 스마트농업 현황분석 및 활성화 방안 연구,” 미래창조과학부, 2016.
2. 김연중 외, “스마트 팼 운영실태 분석 및 발전방향 연구,” 한국농촌경제연구원, 2016.
3. Redmon, J. et al., “You only look once: Unified, real-time object detection,” IEEE CVPR, pp. 779-788, 2016.
4. Jocher, G., [YOLOv5 GitHub](https://github.com/ultralytics/yolov5), 2020.

## 📄 라이선스

나사렛대학교 IT인공지능학부 졸업작품 프로젝트로 제작되었습니다.
