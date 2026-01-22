from packageExam.LMS.domain import Board
from packageExam.LMS.common import Session
import os

FILE_PATH = "data/board.txt"

class BoardService:

    boards = []

    @classmethod
    def load(cls):
        if not os.path.exists(FILE_PATH):
            return
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            cls.boards = [Board.from_line(line) for line in f]

    @classmethod
    def save(cls):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            for b in cls.boards:
                f.write(b.to_line() + "\n")

    @classmethod
    def write(cls):
        if not Session.is_login():
            print("로그인 필요")
            return

        title = input("제목: ")
        content = input("내용: ")
        writer = Session.login_member.uid

        no = len(cls.boards) + 1
        cls.boards.append(Board(no, title, content, writer))

        cls.save()
        print("글 등록 완료")

    @classmethod
    def list(cls):
        print("\n[게시글 목록]")
        print(f"No. 제목 / 작성자 / 내용")
        for b in cls.boards:
            if b.active:
                print(f"{b.no}. {b.title} / {b.writer}  / {b.content}")

    @classmethod
    def delete(cls):

        if not Session.is_login():
            print("로그인 필요")
            return
        no = int(input("삭제할 글 번호: "))

        for b in cls.boards:
            if b.no == no:
                if (Session.login_member.uid == b.writer or
                        Session.login_member.role == "admin"):
                    b.active = False
                    cls.save()
                    print("삭제 완료")
                else:
                    print("권한 없음")
                return

        print("글 없음")

    @classmethod
    def run(cls):
        cls.load()

        while True:
            print("""
    [게시판]
    1. 글쓰기
    2. 글목록
    3. 글삭제
    0. 뒤로가기
    """)
            sel = input(">>> ")

            if sel == "1":
                cls.write()
            elif sel == "2":
                cls.list()
            elif sel == "3":
                cls.delete()
            elif sel == "0":
                break