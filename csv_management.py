import pandas as pd
from datetime import datetime

# df = pd.DataFrame(columns=["이름", "기록시간"])
# main.py에서 df 선언


# 인식된 얼굴을 콘솔 + Dataframe에 기록
def record_attendandce(df, name):
    df["기록시간"] = pd.to_datetime(df["기록시간"], format="%Y-%m-%d %H:%M:%S")
    record_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # type: ignore
    df = pd.concat([df, pd.DataFrame({"이름": [name], "기록시간": [record_time]})], ignore_index=True)

    print(f"{name} 학생이 {record_time}에 출석했습니다.")

    return df


# 출석 기록 csv에 저장
def release_csv(df):
    df.to_csv("output.csv", index=False)
