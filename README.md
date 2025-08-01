# paddle-ocr
基于paddle的ocr识别
# 服务测试

## curl测试
```shell
# 证件识别
curl -F "file=@x1.jpg" http://127.0.0.1:20005/ocr

curl -F "file=@x1.jpg" -F "type_of_card=2" http://127.0.0.1:20005/ocr
```

## python requests测试
```python
import requests

file_path = "E:./obama.jpg"
url = "http://127.0.0.1:20005/ocr"       # 服务器地址
with open(file_path, 'rb') as image_file:
    files = {'file': ('image.jpg', image_file),
             'type_of_card': (None, 1)}
    response = requests.post(url, files=files)

response.json()
print(response.json())
```
