import base64
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)

# MySQL 데이터베이스 연결 정보 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://page:page@localhost/pages'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 업로드 및 정적 파일 설정
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['STATIC_URL_PATH'] = '/static'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# 'uploads' 라우트 정의를 'uploaded_file'로 변경
@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 데이터베이스 연동 설정 초기화
db = SQLAlchemy(app)




# 게시물 모델 정의
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    views = db.Column(db.Integer, default=0)

    # 비밀번호 해시를 저장할 컬럼 추가
    password_hash = db.Column(db.String(60), nullable=False)

    # 이미지를 저장할 필드 추가
    image = db.Column(db.String(255))  # 이미지 파일 경로를 저장할 필드

    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan')

# 댓글 모델 정의 (수정하지 않음)
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

# 루트 경로: 게시판 목록 표시
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

# 함수를 통해 업로드 파일의 확장자 검사
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# 게시물 작성
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        password = request.form['password']
        image = request.files['image']

        if image and allowed_file(image.filename):  # 이미지 파일이 업로드된 경우와 확장자가 허용된 경우에만 처리
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f'uploads/{filename}'
        else:
            image_path = None

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        post = Post(title=title, content=content, author=author, image=image_path, password_hash=hashed_password)
        db.session.add(post)
        db.session.commit()
        flash('게시물이 성공적으로 작성되었습니다.', 'success')
        return redirect(url_for('index'))
    return render_template('create.html')
# 게시물 수정
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        # 비밀번호를 입력 받습니다.
        password = request.form['password']

        # 저장된 비밀번호 해시와 사용자가 입력한 비밀번호를 비교
        if bcrypt.check_password_hash(post.password_hash, password):
            post.title = request.form['title']
            post.content = request.form['content']
            
            # 이미지 업로드 처리
            if 'image' in request.files:
                image = request.files['image']
                if image:
                    filename = secure_filename(image.filename)
                    image.save(f'uploads/{filename}')  # 이미지를 uploads 폴더에 저장
                    post.image = f'uploads/{filename}'  # 이미지 파일 경로 저장

            db.session.commit()
            flash('게시물이 수정되었습니다.', 'success')
            return redirect(url_for('index'))
        else:
            flash('비밀번호가 올바르지 않습니다. 수정이 거부되었습니다.', 'error')

    return render_template('edit.html', post=post)

# 게시물 삭제
@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    post = Post.query.get(id)
    
    if request.method == 'POST':
        password = request.form['password']  # 사용자가 입력한 비밀번호

        # 저장된 비밀번호 해시와 사용자가 입력한 비밀번호를 비교
        if bcrypt.check_password_hash(post.password_hash, password):
            db.session.delete(post)
            db.session.commit()
            flash('게시물이 삭제되었습니다.', 'success')
            return redirect(url_for('index'))
        else:
            flash('비밀번호가 올바르지 않습니다.', 'error')

    return render_template('delete.html', post=post)

# 게시물 보기
@app.route('/view/<int:id>')
def view(id):
    post = Post.query.get(id)
    if post:
        post.views += 1
        db.session.commit()
        comments = Comment.query.filter_by(post_id=id).all()
        return render_template('show_post.html', post=post, comments=comments)
    else:
        flash('게시물을 찾을 수 없습니다.', 'error')
        return redirect(url_for('index'))

# 댓글 생성
@app.route('/add_comment/<int:id>', methods=['POST'])
def add_comment(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        comment_text = request.form['comment_text']
        comment = Comment(text=comment_text, post_id=id)
        db.session.add(comment)
        db.session.commit()
        flash('댓글이 성공적으로 추가되었습니다.', 'success')
        return render_template('show_post.html', post=post, comments=Comment.query.filter_by(post_id=id).all())  # 리디렉션 대신 해당 게시물 페이지로 이동
    return render_template('show_post.html', post=post, comments=Comment.query.filter_by(post_id=id).all())

# 댓글 삭제
@app.route('/delete_comment/<int:id>', methods=['POST'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        flash('댓글이 삭제되었습니다.', 'success')
    
    # 댓글 삭제 후 show_post 페이지를 렌더링
    post_id = comment.post_id if comment else 0  # 댓글이 있는 경우 해당 게시물로, 없는 경우 0으로 설정
    post = Post.query.get(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    
    return render_template('show_post.html', post=post, comments=comments)

# 게시물 검색
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    # 게시물 검색 쿼리: 제목 또는 내용에 키워드가 포함된 게시물을 검색
    posts = Post.query.filter(
        (Post.title.like(f"%{keyword}%")) |
        (Post.content.like(f"%{keyword}%"))
    ).all()
    return render_template('index.html', posts=posts)




if __name__ == '__main__':
    app.run(debug=True, port=5001)
