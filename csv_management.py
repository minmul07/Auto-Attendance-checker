import pandas as pd
from datetime import datetime
import numpy as np

count_goal = 3


#Dataframe 초기화
def initDataFrame(face_list):
    df = pd.DataFrame(columns=["이름", "출석여부", "출석일시", "기록횟수"])
    for name in face_list:
        df = pd.concat(
            [
                df,
                pd.DataFrame({"이름": [name], "출석여부": False, "출석일시": np.nan, "기록횟수": 0}),
            ]
        )
    df.set_index("이름", inplace=True)
    return df


# 인식된 얼굴을 콘솔 + Dataframe에 기록
def record_attendandce(df, name):
    if name == "Unknown":
        return df
    
    
    if df.loc[name, "기록횟수"] < count_goal:
        df.loc[name, "기록횟수"] += 1
    elif df.loc[name, "기록횟수"] == count_goal:
        df.loc[name, "기록횟수"] += 1
        record_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # type: ignore
        df.loc[name, "출석일시"] = record_time
        df.loc[name, "출석여부"] = True
        print(f"{name} 학생이 {record_time}에 출석했습니다.")  # type: ignore // possibly unbound warning
    else:
        pass

    return df


# 출석 기록 csv에 저장
def release_csv(df):
    df.pop("기록횟수")
    df.reset_index(inplace=True)
    df.to_csv("attendence_record.csv", index=False, encoding="utf-8-sig")
