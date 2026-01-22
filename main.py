# 대부분 프로그래밍에서 1번이 되는(start) 파일을 main 으로 만듬

# 목표 : MBC아카데미 LMS 프로그램을 만들어 보자.
# 회원관리 : 시스템담당자, 교수, 행정, 학생, 손님, 학부모
# 성적관리 : 교수가성적등록,수정,
#           행정담당자가 학기마다 백업(이전->삭제)
#           학생은 개인성적일람, 성적출력
#           손님은 학교소개페이지 열람
#           학부모는 자녀학사관리
# 게시판 : 회원제, 비회원제, 문의사항, Q/A

# 필요한 변수
run = True  # 메인 메뉴용 while
# subRun = True # 보조 메뉴용 while
session = None  # 로그인한 사용자의 인덱스를 기억

# 필요한 리스트
# 회원에 대한 리스트
sns = [1]  # 회원에 대한 번호
ids = ["kkw"]  # id에 대한 리스트
pws = ["1234"]  # 암호에 대한 리스트
group = ["admin"]  # 회원등급
# admin (관리자), stu(학생), guest(손님) ....

# 성적에 대한 리스트
pythonScore = []  # 파이썬 점수들
dataBaseScore = []  # 데이터베이스 점수들
wwwScore = []  # 프론트 점수들
totalScore = []  # 총점 들
avgScore = []  # 평균 들
gradeScore = []  # 등급 들
stuIdx = []  # 학생의 인덱스 (학번) <-> 회원의 sns

# 게시판에 대한 리스트
board_no = []  # 게시물의 번호
board_title = []  # 게시물의 제목
board_content = []  # 게시물의 내용
board_writer = []  # 게시물 작성자 <-> 회원의 sns

# 메뉴 구성
mainMenu = """
==========================
엠비씨아카데미 LMS에 오신걸 환영합니다.

1. 로그인(회원가입)
2. 성적관리
3. 게시판
4. 관리자메뉴
9. 프로그램종료

"""

memberMenu = """
---------------------------
회원관리 메뉴입니다.

1. 로그인
2. 회원가입
3. 회원수정
4. 회원탈퇴

9. 회원관리 메뉴 종료

"""

scoreMenu = """
----------------------------
성적관리 메뉴입니다. 

1. 성적입력(교수전용)
2. 성적보기(개인용)
3. 성적수정(교수전용)
4. 성적백업(행정직원전용)

9. 성적관리 메뉴 종료
"""

boardMenu = """
-----------------------------
회원제 게시판 입니다. 

1.
2.
3.
4.
5. 

9.

"""

# 주 실행문 구현
while run:
    print(mainMenu)  # 메인메뉴 출력용
    select = input(">>>")  # 사용자가 주메뉴선택 값을 select 넣는다.

    if select == "1":
        print("로그인(회원가입)메뉴로 진입합니다.")

        subRun = True
        while subRun:  # 부메뉴 반복용
            print(memberMenu)  # 회원관리 메뉴가 출력

            subSelect = input(">>>")  # 회원 부메뉴 선택값을 subSelect에 넣음

            if subSelect == "1":
                print("로그인 메뉴로 진입합니다.")

            elif subSelect == "2":
                print("회원가입 메뉴로 진입합니다.")

            elif subSelect == "3":
                print("회원 수정 메뉴로 진입합니다.")

            elif subSelect == "4":
                print("회원 탈퇴 메뉴로 진입합니다.")

            elif subSelect == "9":
                print("회원 관리 메뉴를 종료 합니다.")
                subRun = False  # 회원 while 종료

            else:  # 1,2,3,4,9 말고 다른 키를 넣을 경우
                print("잘못된 메뉴를 선택하였습니다.")
