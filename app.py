import uuid
from flask import Flask, request, jsonify
import boto3
import io
from PIL import Image

app = Flask(__name__)

BUCKET_NAME = 'aeadae9a-9e785156-fb10-444c-b5e2-1aed9a8f54d3' 

# Инициализация клиента для S3
s3 = boto3.client(
    's3',
    endpoint_url='https://s3.timeweb.cloud',
    region_name='ru-1',
    aws_access_key_id='IQZ7JCZ37BDUBKE7CHEZ', 
    aws_secret_access_key='vjBcc0SeNFxqWDDXQiIV0slcFKjPwf5CdZgkd6QS', 
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
            file_key = str(uuid.uuid4()) + '.jpg'
            
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

