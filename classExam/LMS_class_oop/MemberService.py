# Member객체를 CRUD 기능을 넣는다.
# 메뉴 구현
# 텍스트파일 처리 (파일 읽기, 파일 저장)
# 회원가입, 로그인, 로그아웃, 회원수정, 회원탈퇴
import os

from Member import Member # 회원 객체 추가연결
# 사용법 member = Member() -> 객체가 생성됨
#       member.필드/메서드 = ????

class MemberService:
    def __init__(self, file_name="members.txt"):
    # 클래스가 생성할때 초기값 관리
        self.file_name = file_name
        self.members = []  # 회원들을 리스트로 만들어 Member()객체를 담는다.
        self.session = None # 로그인상태를 담당(members의 인덱스 보관용)
        self.load_members() # 아래쪽에 메서드 호출

    def run(self):
        run = True
        while run:
            self.main_menu()
            sel = input(">>> ")

            if sel == "1": self.member_add()
            elif sel == "2": self.member_login()
            elif sel == "3": self.member_logout()
            elif sel == "4": self.member_modify()
            elif sel == "5": self.member_delete()
            elif sel == "9": run = False
            else :
                print("잘못 입력하셨습니다.")

    def load_members(self): # 파일에서 메모리로 불러온다.
        if not os.path.exists(self.file_name): # 맨위에 import os
            self.save_members()
            return

        self.members = [] # 메모리에 남은 값을 초기화
        with open(self.file_name, "r", encoding="utf-8") as f:
            for line in f:
                self.members.append(Member.from_line(line))
                #                   Member객체에 .from_line() 메서드 실행
                #                               1줄을 가져와 클래스로 만듬
                #    members리스트 뒷부분에 추가

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

    def member_add(self):
        print("\n[회원가입]")
        uid = input("아이디 : ")

        if self.find_member(uid): # 자주쓰는 중복코드로 메서드 처리함!!!
            print("이미 존재하는 아이디")
            return

        pw = input("비밀번호 : ")
        name = input("이름 : ")
        role = "user"

        self.members.append(Member(uid, pw, name, role))
        #                   Member클래스의 init메서드로 바로 들어가 객체 생성
        self.save_members()
        self.load_members()
        print("회원가입 완료")

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
                self.member_admin()  # 관리자용 메서드로 들어감!!!
        else:
            print("비밀번호 오류")

    def member_logout(self):
        self.session = None
        print("로그아웃 완료")

    def member_modify(self):
        if not self.session:
            print("로그인 필요")
            self.member_login()
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

    # 파일 저장용 코드
    def save_members(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            for member in self.members:
                f.write(member.to_line())
                #       Member객체의 메서드를 사용하여 1줄씩 기록

    # id를 이용해 members에서 찾는 공통 메서드
    def find_member(self, uid):
        for member in self.members:
        # members 리스트에서 1개씩 member객체를 가져와
            if member.id == uid: # 가져온 member객체.id와 전달받은 id가 같은지
                print(member.name ,"님을 찾았습니다.")
                # 예전에는 member[2]으로 찾는데 지금은 변수명으로 찾을 수 있음

                return member # 같은게 있으면 member객체를 리턴
        return None # None으로 리턴

    def member_admin(self):
        # role = "admin"에 진입 가능한 메서드
        subrun = True
        while subrun:
            print("\n[관리자 메뉴]")
            print("1. 회원 리스트 조회")
            print("2. 비밀번호 변경")
            print("3. 블랙리스트 처리")
            print("4. 권한 변경")
            print("9. 종료")

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

            elif sel == "9":
                subrun = False

    def show_member_list(self):
        # 관리자가 볼수 있는 회원 리스트
        print("\n[회원 목록]")
        print("-" * 60)
        print(f"{'ID':10} {'이름':10} {'권한':10} {'상태'}")
        print("-" * 60)

        for member in self.members:
        # members 리스트에 있는 객체를 하나씩 가져와 member에 넣음
            status = "활성" if member.active else "비활성"
            # member.active == True면 status변수에 "활성"을 넣고 아니면 "비활성"
            print(f"{member.id:10} {member.name:10} {member.role:10} {status}")
            #                                                     "활성 " , "비활성"
        print("-" * 60)