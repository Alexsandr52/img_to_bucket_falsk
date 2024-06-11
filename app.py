from flask import Flask, request, jsonify
from decouple import config
import boto3
import uuid
import io
from PIL import Image

app = Flask(__name__)

BUCKET_NAME = config('BUCKET_NAME')
AWS_ACCESS_KEY_ID = config('aws_access_key_id')
AWS_SECRET_ACCESS_KEY = config('aws_secret_access_key')

# Инициализация клиента для S3
s3 = boto3.client(
    's3',
    endpoint_url='https://s3.timeweb.cloud',
    region_name='ru-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Получаем изображение из POST запроса
    image_file = request.files['image']
    
    if image_file:
        try:
            # Чтение изображения с использованием библиотеки Pillow
            image = Image.open(io.BytesIO(image_file.read()))
            
            # Генерация уникального имени файла
            file_key = 'fruc/' + str(uuid.uuid4()) + '.jpg'  # Добавление префикса fruc/
            
            # Сохранение изображения в S3
            image_stream = io.BytesIO()
            image.save(image_stream, format='JPEG')
            image_stream.seek(0)
            s3.upload_fileobj(image_stream, BUCKET_NAME, file_key)
            
            # Формирование ссылки на загруженное изображение
            image_url = f"https://s3.timeweb.cloud/{BUCKET_NAME}/{file_key}"
            
            # Возвращаем ссылку в виде JSON
            return jsonify({'image_url': image_url}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No image provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
