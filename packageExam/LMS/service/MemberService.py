import os # 텍스트 파일 처리용

from packageExam.LMS.common import Session
from packageExam.LMS.domain import *

# 상위폴더 폴더 모듈           클래스

# 회원 데이터 파일 경로
# FILE_PATH = "../data/member.txt"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "..", "data", "member.txt")

class MemberService:
    # 회원관련 비즈니스로직 담당하는 클래스
    # CRUD를 담당함

    # 여기도 __init__() 메서드는 생략 -> @classmethod로 구현 연습
    members = [] # 회원들을 보관하는 리스트

    @classmethod
    def load(cls):  # 사용법 MemberService.load()
        # 파일에 있는 데이터를 1줄씩 읽어 Member객체로 만들고 리스트에 추가
        cls.members = []

        if not os.path.exists(FILE_PATH):
            cls.save()
            return

        with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                cls.members.append(Member.from_line(line))
                #                  Member객체에 있는 .from_line()메서드 실행
                #   members 리스트에 추가해라!!!

    @classmethod
    def save(cls):
        # 메모리에 있는 members[]를 텍스트 파일로 저장!!
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            for m in cls.members: # members[]에 있는 1줄씩 m 변수에 넣음
                f.write(m.to_line() + "\n")
                #       Member객체에 있는 .to_line()메서드
                #   f"{self.uid}|{self.pw}|{self.name}|{self.role}|{self.active}"
                # f.write()는 파일에 기록해라!

    @classmethod
    def login(cls): # 로그인 처리 메서드
        print("\n[로그인]")

        uid = input("아이디: ")
        pw = input("비밀번호: ")

        for m in cls.members:
            if m.uid == uid:
                if not m.active:
                    print("비활성화된 계정입니다.")
                    return

                if m.pw == pw:
                    Session.login(m) # 로그인성공시 세션객체에 member객체를 넣음
                    print(f"{m.name}님 로그인 성공 ({m.role})")
                    print(m) # def __str__(self): 활용
                    return
                else:
                    print("비밀번호가 틀렸습니다.")
                    return

        print("존재하지 않는 아이디입니다.")

    @classmethod
    def logout(cls):
        if not Session.is_login():
            print("로그인 상태가 아닙니다.")
            return

        Session.logout() # session = None
        print("로그아웃 완료")

    @classmethod
    def signup(cls):
        print("\n[회원가입]")
        uid = input("아이디: ")
        # 아이디 중복 체크
        if any(m.uid == uid for m in cls.members):
            #                        텍스트파일에 있는 내용을 members 리스트에 넣었었음
            #                   m 변수에 1개씩 꺼내서 넣음
            #               for 반복
            #  m.uid for에서 찾은 객체의 uid
            #        == uid
            # 객체로 만든 members에서 1개씩 찾아와 uid와 같은게 있으면 true
            # any() -> True가 나오면 즉시 종료
            #    하나로도 True면 True / 전부 False면 False 처리함
            print("이미 존재하는 아이디입니다.")
            return
        pw = input("비밀번호: ")
        name = input("이름: ")
        member = Member(uid, pw, name)
        cls.members.append(member)
        cls.save()

        print("회원가입 완료")

    @classmethod
    def modify(cls):
        if not Session.is_login():
            print("로그인 후 이용 가능합니다.")
            return

        member = Session.login_member

        print("""
    [내 정보 수정]
    1. 이름 변경
    2. 비밀번호 변경
    0. 취소
    """)
        sel = input("선택: ")

        if sel == "1":
            member.name = input("새 이름: ")
        elif sel == "2":
            member.pw = input("새 비밀번호: ")
        else:
            return

        cls.save()
        print("정보 수정 완료")

    # ===============================
    # 회원탈퇴 / 비활성화 (Delete)
    # ===============================
    @classmethod
    def delete(cls):
        if not Session.is_login():
            print("로그인 후 이용 가능합니다.")
            return

        member = Session.login_member

        print("""
    [회원 탈퇴]
    1. 완전 탈퇴
    2. 계정 비활성화
    """)
        sel = input("선택: ")

        if sel == "1":
            cls.members.remove(member)
            Session.logout()
            cls.save()
            print("회원 탈퇴 완료")

        elif sel == "2":
            member.active = False
            Session.logout()
            cls.save()
            print("계정 비활성화 완료")

    # ===============================
    # 관리자 메뉴
    # ===============================
    @classmethod
    def admin_menu(cls):
        if not Session.is_login() or not Session.login_member.is_admin():
            print("관리자만 접근 가능합니다.")
            return

        while True:
            print("""
    [관리자 메뉴]
    1. 회원 목록 조회
    2. 권한 변경
    3. 블랙리스트 처리
    0. 뒤로가기
    """)
            sel = input("선택: ")

            if sel == "1":
                cls.list_members()
            elif sel == "2":
                cls.change_role()
            elif sel == "3":
                cls.block_member()
            elif sel == "0":
                break

    # ===============================
    # 관리자 기능들
    # ===============================
    @classmethod
    def list_members(cls):
        print("\n[회원 목록]")
        for m in cls.members:
            print(m)

    @classmethod
    def change_role(cls):
        uid = input("대상 아이디: ")
        for m in cls.members:
            if m.uid == uid:
                m.role = input("admin / manager / user: ")
                cls.save()
                print("권한 변경 완료")
                return
        print("회원 없음")

    @classmethod
    def block_member(cls):
        uid = input("대상 아이디: ")
        for m in cls.members:
            if m.uid == uid:
                m.active = False
                cls.save()
                print("블랙리스트 처리 완료")
                return
        print("회원 없음")
