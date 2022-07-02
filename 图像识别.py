import pytesseract
from PIL import Image

image = Image.open('1.png')

# 如果没有设置上边提到的两个环境变量，则需要以下代码来分别指定tesseract.exe和训练集的路径
# tesseract.exe的路径
# pytesseract.pytesseract.tesseract_cmd = 'tesseract.exe的路径'
# 指定训练集的路径
# tessdata_dir_config = r'--tessdata-dir "D:\Tesseract-OCR\tessdata"'

result = pytesseract.image_to_string(image)
print(result)
