import os

def welcomePage():
    os.system("cls")
    print(f"******************************")
    print("""
2023203068 어승경
2023203042 이동진

환영합니다! 얼굴 인식 기반의 자동 출석 시스템입니다.
""")
    print(f"******************************\n\n")
    
def exportCSV():
    os.system("cls")
    print("""**** 프로그램 종료 ****
출석 기록을 attendence_record.csv 에 저장합니다...""")