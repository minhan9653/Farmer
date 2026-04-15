"""
질병 도감 데이터 API
"""
from flask import Blueprint, jsonify

encyclopedia_bp = Blueprint('encyclopedia', __name__)

# 작물별 질병 데이터 (public_html 정적 페이지에서 추출)
CROPS = [
    {"id": "eggplant", "name": "가지", "image": "https://images.unsplash.com/photo-1613743983303-b3e89f8a2b80?w=400"},
    {"id": "tomato", "name": "토마토", "image": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=400"},
    {"id": "lettuce", "name": "상추", "image": "https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=400"},
    {"id": "cabbage", "name": "배추", "image": "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=400"},
    {"id": "carrot", "name": "당근", "image": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400"},
    {"id": "radish", "name": "무", "image": "https://images.unsplash.com/photo-1585500671198-63e978bca498?w=400"},
    {"id": "strawberry", "name": "딸기", "image": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400"},
    {"id": "pepper", "name": "고추", "image": "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=400"},
]

DISEASES = {
    "eggplant": [
        {
            "id": "eggplant-1",
            "name": "갈색둥근무늬병",
            "category": "병",
            "environment": "1차 전염원에 대하여 아직 정확한 연구결과는 없으나 병원균은 병든 잎의 잔재에서 분생포자나 균사의 형태로 겨울을 나는 것으로 생각된다. 1차 전염원에서 형성된 분생포자는 비산되어 전반되며, 8~9월 또는 초가을 비료가 부족하고, 비가 많은 해에 발생이 심하다.",
            "symptoms": "주로 잎에 발생한다. 병반은 처음 황갈색의 작은 반점으로 나타나고, 진전되면 5~6mm의 큰 병반으로 확대되기도 한다. 병반 주위는 연한 갈색의 병무늬로 나타나고, 점차 진한 병무늬가 형성되며, 병반의 중앙은 회백색으로 변한다.",
            "treatment": "건전 종자를 사용한다. 균형시비를 하여 건전한 생육을 유도한다. 과습하지 않도록 한다. 병든 잎은 모아 태우거나 땅에 묻는다.",
        },
        {
            "id": "eggplant-2",
            "name": "갈색무늬병",
            "category": "병",
            "environment": "비가 자주 내리고 다습한 환경에서 발생이 심하며, 질소 과잉 시비 시 발생이 증가한다.",
            "symptoms": "잎에 갈색 원형 또는 부정형의 병반이 나타나며, 진전되면 병반이 합쳐져 잎 전체가 갈변한다.",
            "treatment": "적절한 환기와 배수 관리를 한다. 이병 잔재물을 제거하고, 등록된 약제를 살포한다.",
        },
        {
            "id": "eggplant-3",
            "name": "겹무늬병",
            "category": "병",
            "environment": "고온다습한 환경에서 잘 발생하며, 시설재배에서 많이 나타난다.",
            "symptoms": "잎에 동심원 형태의 겹무늬가 나타나며, 심하면 잎이 마른다.",
            "treatment": "환기를 잘 하고, 이병 식물체를 제거한다.",
        },
        {
            "id": "eggplant-4",
            "name": "잎곰팡이병",
            "category": "병",
            "environment": "다습하고 통풍이 불량한 조건에서 발생이 심하다.",
            "symptoms": "잎 뒷면에 회백색~갈색의 곰팡이가 발생하고, 잎 앞면에는 황색 반점이 나타난다.",
            "treatment": "하우스 환기를 철저히 하고, 밀식을 피한다.",
        },
        {
            "id": "eggplant-5",
            "name": "잿빛곰팡이병",
            "category": "병",
            "environment": "저온 다습한 조건에서 많이 발생하며, 시설재배에서 흔하다.",
            "symptoms": "꽃, 잎, 줄기, 과실에 회색 곰팡이가 발생한다.",
            "treatment": "환기를 잘 하여 습도를 낮추고, 이병 부위를 제거한다.",
        },
        {
            "id": "eggplant-6",
            "name": "흰가루병",
            "category": "병",
            "environment": "건조하고 서늘한 환경에서 발생이 심하다.",
            "symptoms": "잎 표면에 흰색 가루 형태의 곰팡이가 발생한다.",
            "treatment": "적절한 관수와 환기를 하고, 등록된 약제를 살포한다.",
        },
        {
            "id": "eggplant-7",
            "name": "점박이응애",
            "category": "해충",
            "environment": "고온 건조한 환경에서 다발생한다.",
            "symptoms": "잎 뒷면에 기생하며 흡즙하여 잎이 황백색으로 변한다.",
            "treatment": "천적을 이용하거나, 등록된 살비제를 살포한다.",
        },
        {
            "id": "eggplant-8",
            "name": "아메리카잎굴파리",
            "category": "해충",
            "environment": "시설재배에서 연중 발생하며, 노지에서는 봄~가을에 발생한다.",
            "symptoms": "유충이 잎 속을 굴을 파며 식해하여 구불구불한 흰색 터널이 생긴다.",
            "treatment": "황색 끈끈이 트랩을 설치하고, 이병 잎을 제거한다.",
        },
    ],
    "tomato": [
        {
            "id": "tomato-1",
            "name": "잎곰팡이병",
            "category": "병",
            "environment": "다습한 환경, 시설재배에서 많이 발생한다.",
            "symptoms": "잎 뒷면에 올리브색~갈색 곰팡이가 발생하고, 앞면에 황색 반점이 나타난다.",
            "treatment": "환기를 잘 하고 습도를 낮춘다. 저항성 품종을 재배한다.",
        },
        {
            "id": "tomato-2",
            "name": "황화잎말림바이러스(TYLCV)",
            "category": "병",
            "environment": "담배가루이가 매개하며, 고온 건조한 환경에서 발생이 심하다.",
            "symptoms": "새 잎이 황화되고 위로 말리며 생육이 위축된다.",
            "treatment": "담배가루이 방제가 중요하다. 저항성 품종을 재배한다.",
        },
    ],
    "lettuce": [
        {
            "id": "lettuce-1",
            "name": "노균병",
            "category": "병",
            "environment": "서늘하고 다습한 조건에서 발생이 심하다.",
            "symptoms": "잎에 황색 반점이 생기고 뒷면에 흰색 곰팡이가 발생한다.",
            "treatment": "환기를 잘 하고, 등록된 약제를 살포한다.",
        },
    ],
    "cabbage": [
        {
            "id": "cabbage-1",
            "name": "무름병",
            "category": "병",
            "environment": "고온다습한 환경에서 발생이 심하다.",
            "symptoms": "줄기나 잎 밑부분이 물러지며 악취가 난다.",
            "treatment": "배수를 잘 하고, 상처가 나지 않도록 관리한다.",
        },
    ],
    "carrot": [
        {
            "id": "carrot-1",
            "name": "검은잎마름병",
            "category": "병",
            "environment": "다습한 환경에서 발생한다.",
            "symptoms": "잎에 갈색~검은색의 반점이 나타나고 잎이 마른다.",
            "treatment": "적절한 윤작과 등록된 약제를 사용한다.",
        },
    ],
    "radish": [
        {
            "id": "radish-1",
            "name": "검은무늬병",
            "category": "병",
            "environment": "다습한 환경에서 발생한다.",
            "symptoms": "잎에 검은 원형 반점이 생기며 진전되면 잎이 마른다.",
            "treatment": "이병 잔재물을 제거하고 등록된 약제를 살포한다.",
        },
    ],
    "strawberry": [
        {
            "id": "strawberry-1",
            "name": "잿빛곰팡이병",
            "category": "병",
            "environment": "저온 다습한 조건에서 많이 발생한다.",
            "symptoms": "과실, 꽃, 잎에 회색 곰팡이가 발생한다.",
            "treatment": "환기를 잘 하여 습도를 낮추고 이병 과실을 제거한다.",
        },
    ],
    "pepper": [
        {
            "id": "pepper-1",
            "name": "탄저병",
            "category": "병",
            "environment": "고온다습한 환경에서 발생이 심하다.",
            "symptoms": "과실에 갈색~검은색의 함몰된 병반이 나타난다.",
            "treatment": "이병 과실을 제거하고 등록된 약제를 살포한다.",
        },
        {
            "id": "pepper-2",
            "name": "연모틀바이러스",
            "category": "병",
            "environment": "접촉 전염 및 종자 전염이 주요 전반 경로이다.",
            "symptoms": "잎에 연한 모자이크 무늬가 나타나고 생육이 불량해진다.",
            "treatment": "저항성 품종을 재배하고, 건전 종자를 사용한다.",
        },
    ],
}


@encyclopedia_bp.route('/crops', methods=['GET'])
def get_crops():
    """작물 목록 조회"""
    return jsonify(CROPS)


@encyclopedia_bp.route('/crops/<crop_id>/diseases', methods=['GET'])
def get_diseases(crop_id):
    """특정 작물의 질병 목록 조회"""
    crop = next((c for c in CROPS if c['id'] == crop_id), None)
    if not crop:
        return jsonify({'error': '작물을 찾을 수 없습니다.'}), 404

    diseases = DISEASES.get(crop_id, [])
    return jsonify({
        'crop': crop,
        'diseases': diseases,
    })


@encyclopedia_bp.route('/diseases/<disease_id>', methods=['GET'])
def get_disease_detail(disease_id):
    """특정 질병 상세 조회"""
    for crop_id, diseases in DISEASES.items():
        for disease in diseases:
            if disease['id'] == disease_id:
                crop = next((c for c in CROPS if c['id'] == crop_id), None)
                return jsonify({
                    'crop': crop,
                    'disease': disease,
                })
    return jsonify({'error': '질병을 찾을 수 없습니다.'}), 404
