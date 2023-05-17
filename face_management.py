import face_recognition
import numpy as np
import pandas as pd
import os


# 하위 디렉토리에서 모든 jpg 형식의 얼굴사진 학습
# 이미지 파일과 실제 이름을 딕셔너리로 저장
def getFaceDataFromSubdirectory():
    known_faces = {}

    filenames = os.listdir(".\\faces")
    for filename in filenames:
        known_faces[filename] = face_recognition.load_image_file(f".\\faces\\{filename}")

    return known_faces
