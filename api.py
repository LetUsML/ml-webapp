import uvicorn
from fastapi import FastAPI, UploadFile, File
from tensorflow import keras
import cv2
import numpy as np

app = FastAPI()

# 加载模型
model_new = keras.models.load_model('keras_model_9.h5')
catgory_list = ['bear', 'butterfly', 'fish', 'dog', 'duck', 'ant', 'cat', 'bee', 'bird']

# 图像预处理函数
def preprocess_image(image):
    img_resized = cv2.resize(image, (28, 28))
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    input_image = img_gray.reshape((1, 28, 28, 1))
    return input_image

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
    result = catgory_list[int(np.argmax(pred[0]))]

    return {"result": result, "percent": pred[0].tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
