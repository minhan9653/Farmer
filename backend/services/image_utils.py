"""
이미지 후처리(바운딩 박스 그리기, base64 변환)를 담당하는 모듈
"""
import base64
from io import BytesIO

from PIL import ImageDraw, ImageFont


def draw_detections(image, detected_objects):
    """이미지에 바운딩 박스와 라벨을 그립니다.

    Args:
        image: PIL Image 객체
        detected_objects: 탐지된 객체 목록

    Returns:
        PIL Image: 바운딩 박스가 그려진 이미지
    """
    draw = ImageDraw.Draw(image)

    # 시스템에 따라 폰트가 없을 수 있으므로 예외 처리
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except OSError:
        font = ImageFont.load_default()

    for obj in detected_objects:
        x1, y1, x2, y2 = map(int, obj["box"])
        label = obj.get("display_name", obj["class_name"])

        # 정상 상태는 초록색, 병해는 빨간색으로 표시
        is_normal = not obj.get("link", "")
        color = "#28a745" if is_normal else "#FF4444"

        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

        # 라벨 배경 그리기 (가독성 향상)
        text_bbox = draw.textbbox((x1, y1 - 40), label, font=font)
        draw.rectangle(text_bbox, fill=color)
        draw.text((x1, y1 - 40), label, fill="white", font=font)

    return image


def image_to_base64(image):
    """PIL 이미지를 base64 문자열로 변환합니다.

    Args:
        image: PIL Image 객체

    Returns:
        str: base64 인코딩된 이미지 문자열
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
