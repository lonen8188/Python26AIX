import os
from packageExam.LMS.domain import Score
from packageExam.LMS.common import Session

FILE_PATH = "data/score.txt"


class ScoreService:
    scores = []

    @classmethod
    def load(cls):
        cls.scores = []

        if not os.path.exists(FILE_PATH):
            cls.save()
            return

        with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                print(line)
                cls.scores.append(Score.from_line(line))

    @classmethod
    def save(cls):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            for s in cls.scores:
                f.write(s.to_line())

    # =========================
    # 성적 메뉴
    # =========================
    @classmethod
    def run(cls):
        if Session.login_member is None:
            print("로그인 후 이용 가능합니다.")
            return

        member = Session.login_member
        cls.load() # 파일로 저장된 목록을 불러온다.
        while True:
            print("\n====== 성적 관리 ======")
            if member.role in ("manager", "admin"):
                print("1. 학생 성적 입력/수정")
            print("2. 내 성적 조회")
            if member.role == "admin":
                print("3. 전체 성적 조회")
            print("0. 뒤로가기")

            sel = input(">>> ")

            if sel == "1" and member.role in ("manager", "admin"):
                cls.add_score()
            elif sel == "2":
                cls.view_my_score()
            elif sel == "3" and member.role == "admin":
                cls.view_all()
            elif sel == "0":
                break

    # =========================
    # 성적 입력
    # =========================
    @classmethod
    def add_score(cls):
        member = Session.login_member

        # 권한 체크
        if member.role not in ("manager", "admin"):
            print("성적 입력 권한이 없습니다.")
            return

        uid = input("성적 입력할 학생 아이디: ")

        # 기존 성적 제거 (있으면 수정 개념)
        cls.scores = [s for s in cls.scores if s.uid != uid]

        kor = int(input("국어: "))
        eng = int(input("영어: "))
        math = int(input("수학: "))

        cls.scores.append(Score(uid, kor, eng, math))
        cls.save()

        print("성적 입력 완료")

    # =========================
    # 내 성적 조회
    # =========================
    @classmethod
    def view_my_score(cls):
        member = Session.login_member

        for s in cls.scores:
            if s.uid == member.uid:
                cls.print_score(s)
                return

        print("등록된 성적이 없습니다.")

    # =========================
    # 전체 성적 조회 (관리자)
    # =========================
    @classmethod
    def view_all(cls):
        member = Session.login_member

        if member.role != "admin":
            print("관리자만 접근 가능합니다.")
            return

        print("\n[전체 성적 목록]")
        for s in cls.scores:
            cls.print_score(s)

    # =========================
    # 출력 공통 함수
    # =========================
    @staticmethod
    def print_score(s):
        print(
            f"ID:{s.uid} | "
            f"국어:{s.kor} 영어:{s.eng} 수학:{s.math} | "
            f"총점:{s.total} 평균:{s.avg} | 등급 : {s.grade}"
        )
