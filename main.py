import streamlit as st
from streamlit_drawable_canvas import st_canvas
import random
import requests
from PIL import Image
import json

st.set_page_config(layout="wide")
subject_dic = {
    '题目1': 'bear',
    '题目2': 'butterfly',
    '题目3': 'fish',
    '题目4': 'dog',
    '题目5': 'duck',
    '题目6': 'ant',
    '题目7': 'cat',
    '题目8': 'bee',
    '题目9': 'bird',
}

change = st.sidebar.button("Change the title")
if "subject" not in st.session_state or change:
    st.session_state["subject"] = random.choice(list(subject_dic.keys()))
subject = st.session_state["subject"]

col1, col2, col3 = st.columns([2, 6, 2])
col4, col5, col6, col7 = st.columns([2, 2, 4, 2])
col8, col9, col10, col11 = st.columns([2, 2, 4, 2])
col12, col13, col14, col15 = st.columns([2, 2, 4, 2])
col16, col17, col18, col19 = st.columns([2, 2, 4, 2])
col20, col21, col22 = st.columns([2, 6, 2])
with col2:
    st.write("<h2 style='text-align: center'>{}</h2>".format(subject), unsafe_allow_html=True)
    user_res = st.text_input("please enter your answer")

    # Specify canvas parameters in application

    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 2)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        height=500,
        width=830,
        drawing_mode="freedraw",
        key="canvas",
    )
    if st.button("identify") and canvas_result:
        url = 'http://49.234.32.232:8000/predict'
        im = Image.fromarray(canvas_result.image_data)
        im = im.convert('RGB')
        im.save('test.jpg')

        result = requests.post(url, files={'img': open("test.jpg", 'rb')})
        if result.status_code == 200:
            try:
                result = result.json()
                result = result["result"]
                # 进一步处理结果
            except json.JSONDecodeError as e:
                # 处理JSON解析错误
                print("Failed to parse JSON response:", e)
        else:
            # 处理请求失败
            print("Request failed with status code:", result.status_code)
        if subject_dic[subject] == result:
            sign = 'correctly'
        else:
            sign = 'error'
        flag = [user_res == subject_dic[subject], result == subject_dic[subject]]

        if flag == [True, True]:
            with col5:
                st.image('images/1.jpg')
            with col6:
                st.subheader('This battle is a victory for the rats!')
        elif flag == [True, False]:
            with col5:
                st.image('images/2-1.jpg')
            with col6:
                st.subheader('This battle is a victory for the rats!')
            with col9:
                st.image('images/2-2.jpg')
            with col10:
                st.subheader("Mouse machines are dreadfully clever! I'll have to figure it out myself.")
        elif flag == [False, True]:
            with col5:
                st.image('images/3-1.jpg')
            with col6:
                st.subheader("Uncle Jerry, you're gonna have to find your own way out……")
            with col9:
                st.image('images/3-2.jpg')
            with col10:
                st.subheader("I failed! I failed! What to do!")
        elif flag == [False, False]:
            with col5:
                st.image('images/4-1.jpg')
            with col6:
                st.subheader("I caught the mouse! Eat it now!")
            with col9:
                st.image('images/4-2.jpg')
            with col10:
                st.subheader("What a sad fate for a little mouse……")
            with col13:
                st.image('images/4-3.jpg')
            with col14:
                st.subheader("I'm gonna help Tom keep an eye on Jerry before he gets away! I'm Tom's good assistant!")
            with col17:
                st.image('images/4-4.jpg')
            with col18:
                st.subheader("Mouse, mouse, get in my stomach!")
        with col21:
            st.subheader("Your results: {}，Correct results: {}".format(user_res, subject_dic[subject]))
            st.subheader("Draw {}，recognition result: {}".format(sign, result))
