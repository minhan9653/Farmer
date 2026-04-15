"""
병해충 AI 진단 API
"""
from flask import Blueprint, request, jsonify
from PIL import Image

from services.model import run_inference
from services.image_utils import draw_detections, image_to_base64
from services.disease_info import get_disease_info

diagnosis_bp = Blueprint('diagnosis', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@diagnosis_bp.route('/analyze', methods=['POST'])
def analyze():
    """이미지를 받아 병해충 진단 결과를 JSON으로 반환"""
    if 'image' not in request.files:
        return jsonify({'error': '이미지 파일이 업로드되지 않았습니다.'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': '선택된 이미지 파일이 없습니다.'}), 400

    if not allowed_file(image_file.filename):
        return jsonify({'error': '지원하지 않는 파일 형식입니다.'}), 400

    try:
        image = Image.open(image_file)
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        detected_objects = run_inference(image)

        results = []
        for obj in detected_objects:
            info = get_disease_info(obj["class_name"])
            results.append({
                'class_name': obj['class_name'],
                'confidence': round(obj['confidence'] * 100, 1),
                'display_name': info['display_name'],
                'description': info['description'],
                'link': info['link'],
                'box': [float(v) for v in obj['box']],
            })

        # 바운딩 박스가 그려진 이미지를 base64로
        for obj in detected_objects:
            info = get_disease_info(obj["class_name"])
            obj.update(info)
        annotated_image = draw_detections(image, detected_objects)
        img_base64 = image_to_base64(annotated_image)

        return jsonify({
            'success': True,
            'image': img_base64,
            'detections': results,
        })

    except Exception as e:
        return jsonify({'error': f'이미지 처리 중 오류: {str(e)}'}), 500
