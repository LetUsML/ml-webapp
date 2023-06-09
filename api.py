import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tensorflow import keras
import cv2
import numpy as np
import logging

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建文件处理器
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# 创建格式化器并将其附加到文件处理器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到日志记录器
logger.addHandler(file_handler)

app = FastAPI()

# 加载模型
model_new = keras.models.load_model('keras_model_9.h5')
category_list = ['bear', 'butterfly', 'fish', 'dog', 'duck', 'ant', 'cat', 'bee', 'bird']

# 图像预处理函数
def preprocess_image(image):
    img_resized = cv2.resize(image, (28, 28))
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    input_image = img_gray.reshape((1, 28, 28, 1))
    return input_image

# 添加跨域支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的请求
    allow_methods=["POST"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头部
)

# 定义根路由
@app.get("/")
def index():
    return {"ok": True}

# 定义预测路由
@app.post("/predict")
async def predict(img: UploadFile = File(...)):
    contents = await img.read()
    nparr = np.frombuffer(contents, np.uint8)
    img_color = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 图像预处理
    input_image = preprocess_image(img_color)

    # 进行预测
    pred = model_new.predict(input_image)
    result = category_list[int(np.argmax(pred[0]))]

    # 记录日志
    logger.info(f"Prediction result: {result}")

    return {"result": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
