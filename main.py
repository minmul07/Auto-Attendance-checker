import ui

ui.welcomePage()

import face_recognition
import cv2
import threading
import numpy as np
import pandas as pd

# conda install -c conda-forge face_recognition opencv
# pip install pandas

import csv_management as csvm
import face_management as fm

df = pd.DataFrame(columns=["이름", "기록시간"])


# 멀티스레드
class FaceRecognitionThread(threading.Thread):
    def __init__(self, image):
        threading.Thread.__init__(self)
        self.image = image

    def run(self):
        face_locations = face_recognition.face_locations(self.image)
        face_encodings = face_recognition.face_encodings(self.image, face_locations)
        # 얼굴 인식 결과를 저장하고 사용할 수 있도록 리턴값으로 반환
        self.result = (face_locations, face_encodings)


# 하위 디렉토리에서 모든 jpg 형식의 얼굴사진 학습
# 이미지 파일과 실제 이름을 딕셔너리로 저장
known_faces, face_list = fm.getFaceDataFromSubdirectory()

# 저장된 딕셔너리를 통해 Dataframe 구조화
df = csvm.initDataFrame(face_list)
print(df)

# 이미지에서 얼굴 위치와 벡터 추출
known_face_encodings = []
known_face_names = []
face_count = 0
for name, face_management in known_faces.items():
    face_count += 1
    face_encoding = face_recognition.face_encodings(face_management)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)
    print(f"{name} 학생 얼굴 학습 완료 ({face_count}/{len(known_faces)})")

# 웹캠 연결
cap = cv2.VideoCapture(0)
print("\n비디오 장치가 시작되었습니다.")

while True:
    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()

    # 이미지 크기 조정
    frame = cv2.resize(frame, (0, 0), fx=1, fy=1)  # type: ignore

    # 얼굴 인식을 수행할 이미지 리스트 생성
    images = []
    images.append(frame)

    # 멀티스레드를 사용하여 얼굴 인식 실행
    threads = []
    for image in images:
        thread = FaceRecognitionThread(image)
        thread.start()
        threads.append(thread)

    # 각 스레드에서 반환된 얼굴 인식 결과를 수집
    face_locations_list = []
    face_encodings_list = []
    for thread in threads:
        thread.join()
        face_locations, face_encodings = thread.result
        face_locations_list.append(face_locations)
        face_encodings_list.append(face_encodings)

    # 인식된 얼굴에 대해 신원 확인
    for face_locations, face_encodings in zip(face_locations_list, face_encodings_list):
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # 가장 유사한 얼굴 찾기
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            # 인식된 얼굴에 사각형 그리기
            top, right, bottom, left = [dim for dim in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # 인식된 얼굴 위에 이름 표시
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)

            df = csvm.record_attendandce(df, name)

    # 화면에 출력
    cv2.imshow("Video", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        ui.exportCSV()
        csvm.release_csv(df)
        break

cap.release()
cv2.destroyAllWindows()
