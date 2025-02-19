import os
import streamlit as st
from PIL import Image
import glob
import pandas as pd

df = pd.read_csv('_test.csv')

base_folder = 'misclassify'
folder = os.path.join(base_folder, 'val50')

# Sidebar에 폴더 목록 표시
st.sidebar.title("Folder Navigation")
folders = sorted(os.listdir(folder), key=lambda x: int(x.split('_')[0]))
selected_folder = st.sidebar.selectbox("Select a folder", folders)

# 선택된 폴더의 이미지 파일 목록 불러오기
folder_path = os.path.join(folder, selected_folder)
if os.path.isdir(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
    image_files = sorted(image_files, key=lambda x: int(x.split('_')[2]))
else:
    image_files = []

# 웹 페이지에 이미지 표시
st.title(f"Images in folder {selected_folder}")
if image_files:
    for image_file in image_files:
        origin_name = image_file.split('_')[:3]
        origin_path = f'{"_".join(origin_name)}.JPEG'
        matching_row = df[df['data_path'].str.contains(origin_path, na=False)]

        cols = st.columns(2)

        mislabel = image_file.split('_')[3]  # 모델이 착각한 클래스의 레이블
        mis_class_name = '_'.join(image_file.split('_')[3:])[:-5]

        # 이미지 경로 설정
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)

        # 왼쪽 컬럼에 이미지 출력
        cols[0].write(f'GT label: {selected_folder}')
        cols[0].image(image, caption=f"Original Image:\n{'_'.join(image_file.split('_')[:3])}.JPEG", use_container_width=True)

        # 오른쪽 컬럼에 특정 텍스트만 빨갛게 표시, 글자 크기는 전체적으로 키움
        cols[1].markdown(
            f"<h2>Mispredicted label: <span style='color: red;'>{mis_class_name}</span></h2>",
            unsafe_allow_html=True
        )

        # 정답 데이터 출력
        if not matching_row.empty and pd.notna(matching_row.iloc[0]['answer']):
            st.write(matching_row.iloc[0]['answer'])
else:
    st.write("No images found in this folder.")

