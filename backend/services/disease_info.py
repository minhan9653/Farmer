"""
병해충 클래스별 한국어 이름, 설명, 상세 링크를 관리하는 모듈
"""

# 클래스명 → 한국어 정보 매핑 딕셔너리
DISEASE_MAP = {
    "Pumpkin powdery mildew": {
        "display_name": "호박 흰가루병",
        "description": "잎 표면에 흰색 가루 형태의 곰팡이가 발생하는 병입니다.",
        "link": "https://terms.naver.com/entry.naver?docId=800796&cid=42555&categoryId=42557",
    },
    "Sweet pumpkin spot disease": {
        "display_name": "단호박 점무늬병",
        "description": "잎에 갈색 반점이 나타나는 병해입니다.",
        "link": "https://www.daum.net/",
    },
    "pepper-mild-mottle-virus": {
        "display_name": "고추 연모틀바이러스",
        "description": "고추 잎에 연한 모자이크 무늬가 나타나는 바이러스 병입니다.",
        "link": "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-6-1.html",
    },
    "TYLCV": {
        "display_name": "토마토 황화잎말림바이러스",
        "description": "토마토 잎이 황화되고 말리는 바이러스 병입니다.",
        "link": "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-5-2.html",
    },
    "tomato-leaf-mould": {
        "display_name": "토마토 잎곰팡이병",
        "description": "잎 뒷면에 회백색 곰팡이가 발생하는 병입니다.",
        "link": "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-5-1.html",
    },
    "normal-tomato": {
        "display_name": "토마토 (정상)",
        "description": "정상적인 토마토 잎입니다. 병해충이 감지되지 않았습니다.",
        "link": "",
    },
    "normal-pepper-leap": {
        "display_name": "고추 (정상)",
        "description": "정상적인 고추 잎입니다. 병해충이 감지되지 않았습니다.",
        "link": "",
    },
    "class:normal-pepper-leap": {
        "display_name": "고추 (정상)",
        "description": "정상적인 고추 잎입니다. 병해충이 감지되지 않았습니다.",
        "link": "",
    },
    "normal-pepper": {
        "display_name": "고추 (정상)",
        "description": "정상적인 고추 잎입니다. 병해충이 감지되지 않았습니다.",
        "link": "",
    },
    "Melon-powderymildew": {
        "display_name": "멜론 흰가루병",
        "description": "멜론 잎에 흰가루 형태의 곰팡이가 발생하는 병입니다.",
        "link": "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-2-1.html",
    },
    "Downy-mildew": {
        "display_name": "노균병",
        "description": "잎 뒷면에 곰팡이가 자라며 황갈색 반점이 생기는 병입니다.",
        "link": "https://www.naver.com/",
    },
    "Melon-normal": {
        "display_name": "멜론 (정상)",
        "description": "정상적인 멜론 잎입니다. 병해충이 감지되지 않았습니다.",
        "link": "",
    },
    "cucumber_powdery-mildew": {
        "display_name": "오이 흰가루병",
        "description": "오이 잎에 흰가루 형태의 곰팡이가 발생하는 병입니다.",
        "link": "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-3-5.html",
    },
    "cucumber_normal": {
        "display_name": "오이 (정상)",
        "description": "정상적인 오이 잎입니다. 병해충이 감지되지 않았습니다.",
        "link": "",
    },
    "cucumber_downy-mildew": {
        "display_name": "오이 노균병",
        "description": "오이 잎 뒷면에 곰팡이가 발생하며 황갈색 반점이 생기는 병입니다.",
        "link": "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-3-1.html",
    },
    "Ascochyta-leaf-spot": {
        "display_name": "아스코키타 점무늬병",
        "description": "잎에 갈색 점무늬가 나타나는 곰팡이 병입니다.",
        "link": "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-6-2.html",
    },
    "sweet-pumpkin": {
        "display_name": "단호박 (정상)",
        "description": "정상적인 단호박 잎입니다. 병해충이 감지되지 않았습니다.",
        "link": "",
    },
    "object": {
        "display_name": "기타 객체",
        "description": "분류되지 않은 객체가 감지되었습니다.",
        "link": "",
    },
}


def get_disease_info(class_name):
    """클래스명으로 병해충 정보를 조회합니다.

    Args:
        class_name: YOLO 모델이 반환한 클래스명

    Returns:
        dict: display_name, description, link 키를 포함하는 딕셔너리
    """
    if class_name in DISEASE_MAP:
        return DISEASE_MAP[class_name]

    # 매핑에 없는 클래스의 경우 기본값 반환
    return {
        "display_name": class_name,
        "description": "해당 클래스에 대한 상세 정보가 준비 중입니다.",
        "link": "",
    }
