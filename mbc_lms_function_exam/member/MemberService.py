import os
from Member import Member

class MemberService:
    def __init__(self, file_name="members.txt"):
        self.file_name = file_name
        self.members = []
        self.session = None
        self.load_members()

    # ===============================
    # 파일 로드
    # ===============================
    def load_members(self):
        if not os.path.exists(self.file_name):
            self.save_members()
            return

        with open(self.file_name, "r", encoding="utf-8") as f:
            for line in f:
                self.members.append(Member.from_line(line))

    # ===============================
    # 파일 저장
    # ===============================
    def save_members(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            for m in self.members:
                f.write(m.to_line())

    # ===============================
    # 회원가입
    # ===============================
    def member_add(self):
        print("\n[회원가입]")
        uid = input("아이디 : ")

        if self.find_member(uid):
            print("이미 존재하는 아이디")
            return

        pw = input("비밀번호 : ")
        name = input("이름 : ")

        print("1.admin  2.manager  3.user")
        r = input("권한 : ")
        role = "admin" if r == "1" else "manager" if r == "2" else "user"

        self.members.append(Member(uid, pw, name, role))
        self.save_members()
        print("회원가입 완료")

    # ===============================
    # 로그인
    # ===============================
    def member_login(self):
        print("\n[로그인]")
        uid = input("아이디 : ")
        pw = input("비밀번호 : ")

        member = self.find_member(uid)

        if not member:
            print("존재하지 않는 아이디")
            return

        if not member.active:
            print("비활성화 계정")
            return

        if member.pw == pw:
            self.session = member
            print(f"{member.name}님 로그인 성공 ({member.role})")

            if member.role == "admin":
                self.member_admin()
        else:
            print("비밀번호 오류")

    # ===============================
    # 관리자 기능
    # ===============================
    def member_admin(self):
        while True:
            print("\n[관리자 메뉴]")
            print("1. 회원 리스트 조회")
            print("2. 비밀번호 변경")
            print("3. 블랙리스트 처리")
            print("4. 권한 변경")
            print("0. 종료")

            sel = input("선택 : ")

            # 회원 목록 보기
            if sel == "1":
                self.show_member_list()

            # 비밀번호 변경
            elif sel == "2":
                uid = input("대상 아이디 : ")
                member = self.find_member(uid)
                if member:
                    member.pw = input("새 비밀번호 : ")
                    self.save_members()
                    print("비밀번호 변경 완료")
                else:
                    print("회원 없음")

            # 블랙리스트
            elif sel == "3":
                uid = input("대상 아이디 : ")
                member = self.find_member(uid)
                if member:
                    member.active = False
                    self.save_members()
                    print("블랙리스트 처리 완료")
                else:
                    print("회원 없음")

            # 권한 변경
            elif sel == "4":
                uid = input("대상 아이디 : ")
                member = self.find_member(uid)
                if member:
                    member.role = input("admin / manager / user : ")
                    self.save_members()
                    print("권한 변경 완료")
                else:
                    print("회원 없음")

            elif sel == "0":
                break

    def show_member_list(self):
        """
        관리자용 회원 전체 목록 출력
        """
        print("\n[회원 목록]")
        print("-" * 60)
        print(f"{'ID':10} {'이름':10} {'권한':10} {'상태'}")
        print("-" * 60)

        for m in self.members:
            status = "활성" if m.active else "비활성"
            print(f"{m.id:10} {m.name:10} {m.role:10} {status}")

        print("-" * 60)

    # ===============================
    # 로그아웃
    # ===============================
    def member_logout(self):
        self.session = None
        print("로그아웃 완료")

    # ===============================
    # 내정보 수정
    # ===============================
    def member_modify(self):
        if not self.session:
            print("로그인 필요")
            return

        print("1. 이름 변경")
        print("2. 비밀번호 변경")
        sel = input("선택 : ")

        if sel == "1":
            self.session.name = input("새 이름 : ")
        elif sel == "2":
            self.session.pw = input("새 비밀번호 : ")

        self.save_members()
        print("수정 완료")

    # ===============================
    # 회원탈퇴
    # ===============================
    def member_delete(self):
        if not self.session:
            print("로그인 필요")
            return

        print("1. 완전 탈퇴")
        print("2. 비활성화")
        sel = input("선택 : ")

        if sel == "1":
            self.members.remove(self.session)
        elif sel == "2":
            self.session.active = False

        self.session = None
        self.save_members()
        print("처리 완료")

    # ===============================
    # 회원 검색
    # ===============================
    def find_member(self, uid):
        for m in self.members:
            if m.id == uid:
                return m
        return None

    # ===============================
    # 메뉴
    # ===============================
    def main_menu(self):
        print("""
==== 회원관리 프로그램 (Member 객체 기반) ====
1. 회원가입
2. 로그인
3. 로그아웃
4. 회원정보수정
5. 회원탈퇴
9. 종료
""")

    def run(self):
        while True:
            self.main_menu()
            sel = input(">>> ")

            if sel == "1": self.member_add()
            elif sel == "2": self.member_login()
            elif sel == "3": self.member_logout()
            elif sel == "4": self.member_modify()
            elif sel == "5": self.member_delete()
            elif sel == "9": break

