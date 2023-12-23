from flask import Flask, request, render_template
import torch
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

app = Flask(__name__)

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error="이미지 파일이 업로드되지 않았습니다")
        
        image_file = request.files['image']
        
        if image_file.filename == '':
            return render_template('index.html', error="선택된 이미지 파일이 없습니다")
        
        image = Image.open(image_file)
        
        # 이미지를 RGBA 모드에서 RGB 모드로 변환
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # YOLOv5를 사용하여 추론 수행
        results = model(image)
        
        # 결과 처리
        detected_objects = []
        for detection in results.pred[0]:
            class_index = int(detection[5])
            class_name = model.model.names[class_index]
            box = detection[:4]  # 바운딩 박스 좌표
            detected_objects.append({"class_name": class_name, "box": box})
        
        # 이미지에 바운딩 박스와 라벨 그리기
        draw = ImageDraw.Draw(image)
        for obj in detected_objects:    
            x1, y1, x2, y2 = map(int, obj["box"])
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            
            font = ImageFont.truetype("arial.ttf", 36)  # 필요에 따라 폰트와 크기 변경
            
            label = obj['class_name']
            draw.text((x1, y1), label, fill="red", font=font)
            
         # 감지된 객체를 확인하고 클래스 이름에 따라 링크 추가
            if label == "Pumpkin powdery mildew":
                link = "https://terms.naver.com/entry.naver?docId=800796&cid=42555&categoryId=42557"
            elif label == "Sweet pumpkin spot disease":
                 link = "https://www.daum.net/"
            elif label == "pepper-mild-mottle-virus":
                 link = "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-6-1.html"
            elif label == "TYLCV":
                 link = "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-5-2.html"
            elif label == "tomato-leaf-mould":
                 link ="http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-5-1.html"
            elif label == "normal-tomato":
                 link = ""
            elif label == "normal-pepper-leap":
                 link = ""
            elif label == "Melon-powderymildew":
                 link = "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-2-1.html"
            elif label == "Downy-mildew":
                 link = "https://www.naver.com/"
            elif label == "Melon-normal":
                 link = ""
            elif label == "cucumber_powdery-mildew":
                 link = "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-3-5.html"
            elif label == "cucumber_normal":
                 link = ""
            elif label == "cucumber_downy-mildew":
                 link = "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-3-1.html"   
            else:
                 label== "Ascochyta-leaf-spot"     
                 link = "http://farmerai.knuit.com.s3-website.ap-northeast-2.amazonaws.com/list-6-2.html" 
            obj["link"] = link
        
        # 이미지를 HTML에서 표시하기 위해 base64로 변환
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return render_template('index.html', img_base64=img_base64, detected_objects=detected_objects)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
