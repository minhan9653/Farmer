"""
Farmer 통합 Flask API 서버
- 병해충 AI 진단 API
- 게시판 CRUD API
- 질병 도감 데이터 API
"""
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import Flask
from flask_cors import CORS

from extensions import db, bcrypt


def create_app():
    app = Flask(__name__)
    app.secret_key = 'farmer-secret-key-2024'

    # CORS 설정 (React 개발 서버 허용)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # MySQL 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://page:page@localhost/pages'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)

    # 블루프린트 등록
    from routes.diagnosis import diagnosis_bp
    from routes.board import board_bp
    from routes.encyclopedia import encyclopedia_bp

    app.register_blueprint(diagnosis_bp, url_prefix='/api/diagnosis')
    app.register_blueprint(board_bp, url_prefix='/api/board')
    app.register_blueprint(encyclopedia_bp, url_prefix='/api/encyclopedia')

    # 업로드 파일 서빙
    from flask import send_from_directory

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # 모델 프리로드
    with app.app_context():
        from services.model import load_model
        print("[시작] YOLO 모델 로딩 중...")
        load_model()
        print("[완료] 모델 로딩 완료, 서버 준비됨")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_reloader=False, port=5000)
