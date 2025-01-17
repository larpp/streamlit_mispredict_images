import os
import streamlit as st
from PIL import Image
import glob
import pandas as pd


df = pd.read_csv('updated_final_categorize.csv')

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

        mislabel = image_file.split('_')[3] # 모델이 착각한 클래스의 레이블
        mislabel_path = f'comparative_images/{mislabel}'
        mislabel_img = os.listdir(mislabel_path)
        mislabel_files = glob.glob(f'misclassify/val50/{mislabel}_*/*')
        mislabel_files = [i.split('_')[-3] for i in mislabel_files]
        
        mis_image_path = os.path.join(mislabel_path, mislabel_img[0])
        mis_image = Image.open(mis_image_path)

        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)

        cols[0].write(f'GT label: {selected_folder}')
        mis_class_name = '_'.join(image_file.split('_')[3:])[:-5]
        cols[1].write(f'Mispredicted label: {mis_class_name}')
        
        # 이미지와 착각한 클래스의 이미지를 각각의 컬럼에 넣어서 출력
        cols[0].image(image, caption=f"Original Image:\n{'_'.join(image_file.split('_')[:3])}.JPEG", use_container_width=True)
        cols[1].image(mis_image, caption=f"Mispredicted:\n{'_'.join(image_file.split('_')[3:])[:-5]}", use_container_width=True)

        if not matching_row.empty and pd.notna(matching_row.iloc[0]['category']):
            st.write(matching_row.iloc[0]['category'])
else:
    st.write("No images found in this folder.")
