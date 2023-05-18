import face_recognition
import os


# 하위 디렉토리에서 모든 jpg 형식의 얼굴사진 학습
# 이미지 파일과 실제 이름을 딕셔너리로 저장
def getFaceDataFromSubdirectory(): 
    known_faces = {}

    filenames = os.listdir(".\\faces")
    for filename in filenames:
        known_faces[filename.split(".")[0]] = face_recognition.load_image_file(f".\\faces\\{filename}")
        print(f"{filename.split('.')[0]} 학생 얼굴을 이미지를 가져왔습니다.")
    
    print("\n")
    return known_faces
