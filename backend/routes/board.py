"""
게시판 CRUD API
"""
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from db_models import Post, Comment
from extensions import db, bcrypt

board_bp = Blueprint('board', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@board_bp.route('/posts', methods=['GET'])
def get_posts():
    """게시물 목록 조회"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts])


@board_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """게시물 상세 조회 (조회수 증가)"""
    post = Post.query.get_or_404(post_id)
    post.views += 1
    db.session.commit()
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()
    return jsonify({
        **post.to_dict(),
        'comments': [c.to_dict() for c in comments],
    })


@board_bp.route('/posts', methods=['POST'])
def create_post():
    """게시물 작성"""
    title = request.form.get('title')
    content = request.form.get('content')
    author = request.form.get('author')
    password = request.form.get('password')

    if not all([title, content, author, password]):
        return jsonify({'error': '모든 필드를 입력해주세요.'}), 400

    image_path = None
    if 'image' in request.files:
        image = request.files['image']
        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            image_path = filename

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    post = Post(title=title, content=content, author=author,
                image=image_path, password_hash=hashed_password)
    db.session.add(post)
    db.session.commit()

    return jsonify({'success': True, 'post': post.to_dict()}), 201


@board_bp.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """게시물 수정"""
    post = Post.query.get_or_404(post_id)
    password = request.form.get('password')

    if not password or not bcrypt.check_password_hash(post.password_hash, password):
        return jsonify({'error': '비밀번호가 올바르지 않습니다.'}), 403

    post.title = request.form.get('title', post.title)
    post.content = request.form.get('content', post.content)

    if 'image' in request.files:
        image = request.files['image']
        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            post.image = filename

    db.session.commit()
    return jsonify({'success': True, 'post': post.to_dict()})


@board_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """게시물 삭제"""
    post = Post.query.get_or_404(post_id)
    password = request.json.get('password') if request.is_json else request.form.get('password')

    if not password or not bcrypt.check_password_hash(post.password_hash, password):
        return jsonify({'error': '비밀번호가 올바르지 않습니다.'}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({'success': True})


@board_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    """댓글 작성"""
    Post.query.get_or_404(post_id)
    data = request.get_json()
    text = data.get('text') if data else None

    if not text:
        return jsonify({'error': '댓글 내용을 입력해주세요.'}), 400

    comment = Comment(text=text, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'success': True, 'comment': comment.to_dict()}), 201


@board_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """댓글 삭제"""
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'success': True})


@board_bp.route('/posts/search', methods=['GET'])
def search_posts():
    """게시물 검색"""
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify([])

    posts = Post.query.filter(
        (Post.title.like(f"%{keyword}%")) |
        (Post.content.like(f"%{keyword}%"))
    ).order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts])
