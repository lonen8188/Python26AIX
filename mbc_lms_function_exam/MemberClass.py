import os
# MemberManager
#  ├─ file_name 변수
#  ├─ members
#  ├─ session
#  ├─ load_members() 메서드
#  ├─ save_members()
#  ├─ member_add()
#  ├─ member_login()
#  ├─ member_admin()
#  ├─ member_logout()
#  ├─ member_modify()
#  ├─ member_delete()
#  ├─ main_menu()
#  └─ run()

class MemberManager: # 객체를 담당하는 클래스 사용법은 변수 = MemberManager() 생성

    # 클래스에서 self는 객체의 주소를 가져고 있음.
    # def __init__(self) 클래스 구현시 필수
    def __init__(self, file_name="members.txt"):  # 객체생성시 만드는 기본값 (생성자)
        self.file_name = file_name  # 객체에 파일이름을 넣는다.
        self.members = []           # 객체에 members 리스트를 만든다.
        self.session = None         # 객체에 세션변수를 만들고 기본값으로 None 처리(정수)
        self.load_members()         # 아래에 선언된 load_members() 메서드를 호출한다.

    # ===============================
    # 파일 로드
    # ===============================
    def load_members(self): # 앞으로만들 메서드는 ()괄호 안에 self가 필수
        self.members = [] # 빈배열로 생성 (혹시나, 이전에 리스트가 남아있을 수 있음)

        if not os.path.exists(self.file_name): # 동일 디렉토리에 파일명이 없으면????
            self.save_members()     # save_members()메서드를 호출 ( open()으로 파일생성)
            return                  # load_members()메서드를 빠져나와라~

        with open(self.file_name, "r", encoding="utf-8") as f:
            #    members.txt     읽기전용      한글처리필수  -> f라는 변수에 넣어라
            for line in f:  # f변수에 있는 파일객체를 줄단위로 반복함
                data = line.strip().split("|")
                # 1줄 읽은 값을 엔터제거 | 를 기준으로 잘라 -> 1차원 리스트로 생성
                # ["kkw","1234","김기원","admin","True"]
                data[4] = True if data[4] == "True" else False
                # 리스트 5번째 값이 문자열 True이면 불타입 True로 변경 아니면 False
                self.members.append(data)
                # 2차원 배열인 members 맨뒤에 추가~~~ for 종료까지

    # ===============================
    # 파일 저장
    # ===============================
    def save_members(self): # members 2차원 리스트 값을 파일로 덮어쓴다.
        # 왜??? 파일처리는 수정을 하지 않는다. r(읽기전용), w(덮어쓰기) , a(마지막에 추가)
        with open(self.file_name, "w", encoding="utf-8") as f:
            #      members.txt   덮어쓰기         한글처리  -> f 변수에 넣어라.

            for m in self.members: # 메모리에 있는 members 2차원 리스트를 1줄씩 가져와!
                # m 변수에 넣어라.
                # m =     ["kkw","1234","김기원","admin","True"]
                f.write(f"{m[0]}|{m[1]}|{m[2]}|{m[3]}|{m[4]}\n")
                #            kkw|1234|김기원|admin|True엔터  -> write 저장
                #                                          -> for가 종료될때까지

    # ===============================
    # 회원가입
    # ===============================
    def member_add(self):  # self는 클래스의 객체 주소
        print("\n[회원가입]")
        uid = input("아이디 : ") # 키보드로 입력한 값을 uid변수에 넣음

        for m in self.members: # 2차원 배열인 members에 1차원 리스트를 가져와 (1줄)
            if m[0] == uid:
                print("이미 존재하는 아이디입니다.")
                return # member_add() 메서드를 빠져나온다.

        # 중복 id가 없으면 아래쪽 코드 실행 -> else : 로 처리해도 되나 -> 들여쓰기 필수
        pw = input("비밀번호 : ")
        name = input("이름 : ")

        print("1.admin  2.manager  3.user")
        r = input("권한 선택 : ")

        role = "user"
        if r == "1":
            role = "admin"
        elif r == "2":
            role = "manager"

        # 여기까지가 변수에 입력 완료
        self.members.append([uid, pw, name, role, True])
        # 메모리에 있는 2차원리스트 members 뒤에 추가!!! .append()
        self.save_members() # 파일로 저장
        self.load_members()  # 다시 파일에 있는 내용 불러오기
        print("회원가입 완료")

    # ===============================
    # 로그인
    # ===============================
    def member_login(self):
        print("\n[로그인]")
        uid = input("아이디 : ")
        pw = input("비밀번호 : ")

        # enumerate() -> 2차원 배열을 인덱스와 리스트를 추출한다.
        for i, m in enumerate(self.members):
        #  idx, member
            if m[0] == uid: # for문 중에 같은 아이디가 있으면
                if not m[4]:  # active가 false인지 확인
                    print("비활성화된 계정입니다.")
                    return    # member_login()메서드를 빠져나온다.

                # ["kkw","1234","김기원","admin","True"]
                #    0      1      2       3       4
                # active가 True이면
                if m[1] == pw:  # member[]
                    self.session = i # session 변수에 인덱스를 넣는다. (회원주소)
                    print(f"{m[2]}님 로그인 성공 ({m[3]})")

                    if m[3] == "admin":  # 관리자 이면
                        self.member_admin() # 메서드를 호출한다. (관리자 메뉴)
                    return  # member_login()메서드를 빠져나온다.
                else:  # if m[1] == pw: 결과가 false 이면
                    print("비밀번호 오류")
                    return  # member_login()메서드를 빠져나온다.

        print("존재하지 않는 아이디") # for문에 return이 안걸리면 여기까지 온다.

    # ===============================
    # 관리자 기능
    # ===============================
    def member_admin(self): # 로그인시 admin = role이면 진입
        print("\n[관리자 메뉴]")
        print("1. 비밀번호 변경")
        print("2. 블랙리스트")
        print("3. 권한 변경")
        print("0. 종료")

        sel = input("선택 : ")    # 관리자 메뉴 선택용
        uid = input("대상 아이디 : ") # 대상 id 찾는 입력

        for m in self.members: # members에 2차원 배열을 반복
            if m[0] == uid:    # 대상 id를 찾으면
                if sel == "1": # 비밀번호 변경
                    m[1] = input("새 비밀번호 : ")
                elif sel == "2": # 블랙리스트 처리
                    m[4] = False
                elif sel == "3": # 권한 변경 입력
                    m[3] = input("admin / manager / user : ")

                self.save_members() # 파일로 저장
                self.load_members()  # 다시 파일에 있는 내용 불러오기
                print("관리자 작업 완료")
                return

        print("대상 회원 없음")

    # ===============================
    # 로그아웃
    # ===============================
    def member_logout(self):
        self.session = None # 세션값에 있는 인덱스를 None 처리함
        print("로그아웃 완료")

    # ===============================
    # 내정보 수정
    # ===============================
    def member_modify(self):
        if self.session is None: # 현재 세션에 값이 None이면???
            print("로그인 필요")
            return

        print("\n[내 정보 수정]")
        print("1. 이름 변경")
        print("2. 비밀번호 변경")

        sel = input("선택 : ")

        if sel == "1":  # 이름변경
            self.members[self.session][2] = input("새 이름 : ")
            #   2차원배열   로그인인덱스  이름필드
        elif sel == "2":
            self.members[self.session][1] = input("새 비밀번호 : ")
            #   2차원배열   로그인인덱스  암호필드

        self.save_members()
        self.load_members()  # 다시 파일에 있는 내용 불러오기
        print("수정 완료")

    # ===============================
    # 회원탈퇴
    # ===============================
    def member_delete(self):
        if self.session is None:
            print("로그인 필요")
            return

        print("\n[회원 탈퇴]")
        print("1. 완전 탈퇴")
        print("2. 계정 비활성화")

        sel = input("선택 : ")

        if sel == "1":
            self.members.pop(self.session)
        elif sel == "2":
            self.members[self.session][4] = False

        self.session = None
        self.save_members()  # 파일로 저장
        self.load_members()  # 다시 파일에 있는 내용 불러오기
        print("처리 완료")

    # ===============================
    # 메뉴
    # ===============================
    def main_menu(self):
        print("""
==== 회원관리 프로그램 (Class 기반) ====
1. 회원가입
2. 로그인
3. 로그아웃
4. 회원정보수정
5. 회원탈퇴
9. 종료
""")

    # ===============================
    # 실행
    # ===============================
    def run(self):
        while True:
            self.main_menu()
            sel = input(">>> ")

            if sel == "1":
                self.member_add()
            elif sel == "2":
                self.member_login()
            elif sel == "3":
                self.member_logout()
            elif sel == "4":
                self.member_modify()
            elif sel == "5":
                self.member_delete()
            elif sel == "9": break


# ===============================
# 프로그램 시작
# ===============================
app = MemberManager()  # 가장 중요한 포인트 (지금까지 만든 클래스를 객체로 만들고)
app.run()  # 객체있는 .run()메서드를 실행한다.
