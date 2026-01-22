# ===============================
# 전역 변수
# ===============================
run = True
session = None   # 로그인한 사용자 인덱스

ids = ["kkw", "lhj", "ljj"]
pws = ["1234", "5678", "8888"]
names = ["김기원", "임효정", "이재정"]
roles = ["admin", "manager", "user"]
active = [True, True, True]


# ===============================
# 회원가입
# ===============================
def member_add():
    print("\n[회원가입]")

    new_id = input("아이디 : ")
    if new_id in ids:
        print("이미 존재하는 아이디입니다.")
        return

    new_pw = input("비밀번호 : ")
    new_name = input("이름 : ")

    member_add_menu()
    role_sel = input("권한 선택 : ")

    if role_sel == "1":
        new_role = "admin"
    elif role_sel == "2":
        new_role = "manager"
    else:
        new_role = "user"

    ids.append(new_id)
    pws.append(new_pw)
    names.append(new_name)
    roles.append(new_role)
    active.append(True)

    print("회원가입 완료")


# ===============================
# 로그인
# ===============================
def member_login():
    global session
    print("\n[로그인]")

    if session is not None:
        print("이미 로그인 상태입니다.")
        return

    uid = input("아이디 : ")
    upw = input("비밀번호 : ")

    if uid in ids:
        idx = ids.index(uid)

        if not active[idx]:
            print("비활성화/차단된 계정입니다.")
            return

        if pws[idx] == upw:
            session = idx
            print(f"{names[idx]}님 로그인 성공 ({roles[idx]})")

            if roles[idx] == "admin":
                member_admin()
        else:
            print("비밀번호가 틀렸습니다.")
    else:
        print("존재하지 않는 아이디입니다.")


# ===============================
# 관리자 기능
# ===============================
def member_admin():
    print("\n[관리자 메뉴]")
    print("1. 회원 비밀번호 변경")
    print("2. 회원 블랙리스트 처리")
    print("3. 권한 변경")
    print("0. 종료")

    sel = input("선택 : ")

    if sel == "1":
        uid = input("대상 아이디 : ")
        if uid in ids:
            idx = ids.index(uid)
            pws[idx] = input("새 비밀번호 : ")
            print("비밀번호 변경 완료")

    elif sel == "2":
        uid = input("대상 아이디 : ")
        if uid in ids:
            idx = ids.index(uid)
            active[idx] = False
            print("블랙리스트 처리 완료")

    elif sel == "3":
        uid = input("대상 아이디 : ")
        if uid in ids:
            idx = ids.index(uid)
            print("admin / manager / user")
            roles[idx] = input("새 권한 : ")
            print("권한 변경 완료")


# ===============================
# 로그아웃
# ===============================
def member_logout():
    global session
    if session is None:
        print("로그인 상태가 아닙니다.")
    else:
        print(f"{names[session]}님 로그아웃")
        session = None


# ===============================
# 회원정보 수정
# ===============================
def member_modify():
    if session is None:
        print("로그인 후 이용 가능합니다.")
        return

    print("\n[내 정보 수정]")
    print("1. 이름 변경")
    print("2. 비밀번호 변경")

    sel = input("선택 : ")

    if sel == "1":
        names[session] = input("새 이름 : ")
        print("이름 변경 완료")

    elif sel == "2":
        pws[session] = input("새 비밀번호 : ")
        print("비밀번호 변경 완료")


# ===============================
# 회원탈퇴 / 비활성화
# ===============================
def member_delete():
    global session
    if session is None:
        print("로그인 후 이용 가능합니다.")
        return

    print("\n[회원 탈퇴]")
    print("1. 완전 탈퇴")
    print("2. 계정 비활성화")

    sel = input("선택 : ")

    if sel == "1":
        ids.pop(session)
        pws.pop(session)
        names.pop(session)
        roles.pop(session)
        active.pop(session)
        session = None
        print("회원 탈퇴 완료")

    elif sel == "2":
        active[session] = False
        session = None
        print("계정 비활성화 완료")


# ===============================
# 메뉴
# ===============================
def main_menu():
    print("""
==== 엠비씨아카데미 회원관리 프로그램 ====
1. 회원가입
2. 로그인
3. 로그아웃
4. 회원정보수정
5. 회원탈퇴
9. 프로그램 종료
""")


def member_add_menu():
    print("""
----- 회원가입 권한 선택 -----
1. 관리자
2. 팀장
3. 일반사용자
""")


# ===============================
# 프로그램 시작
# ===============================
while run:
    main_menu()
    select = input(">>> ")

    if select == "1":
        member_add()
    elif select == "2":
        member_login()
    elif select == "3":
        member_logout()
    elif select == "4":
        member_modify()
    elif select == "5":
        member_delete()
    elif select == "9":
        run = False
