"""
YOLOv5 모델 로드 및 추론을 담당하는 모듈
"""
import os
import torch

# 모듈 레벨 변수 (앱 시작 시 한 번만 로드)
_model = None

# 로컬 모델 파일 경로 (code/yolov5s.pt)
_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'yolov5s.pt')


def load_model():
    """YOLOv5 모델을 로드합니다. 이미 로드된 경우 캐시된 모델을 반환합니다."""
    global _model
    if _model is None:
        if os.path.exists(_MODEL_PATH):
            # 로컬 커스텀 모델 파일 사용
            _model = torch.hub.load('ultralytics/yolov5', 'custom', path=_MODEL_PATH, trust_repo=True)
        else:
            # 로컬 파일이 없으면 기본 모델 다운로드
            _model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)
        print(f"[모델 로드 완료] 클래스: {_model.model.names}")
    return _model


def run_inference(image):
    """이미지에 대해 YOLO 추론을 수행합니다.

    Args:
        image: PIL Image 객체

    Returns:
        list: 탐지된 객체 목록 (class_name, confidence, box 포함)
    """
    model = load_model()
    model.conf = 0.25  # 신뢰도 임계값 (0.25 이상만 탐지)
    results = model(image)

    print(f"[\ucd94\ub860] \ud0d0\uc9c0\ub41c \uac1d\uccb4 \uc218: {len(results.pred[0])}")
    detected_objects = []
    for detection in results.pred[0]:
        class_index = int(detection[5])
        class_name = model.model.names[class_index]
        confidence = float(detection[4])
        box = detection[:4]

        print(f"  - {class_name} ({confidence:.2%}) [{box[0]:.0f},{box[1]:.0f},{box[2]:.0f},{box[3]:.0f}]")
        detected_objects.append({
            "class_name": class_name,
            "confidence": confidence,
            "box": box,
        })

    return detected_objects
