import json
import os

# ===============================
# 전역 변수
# ===============================
run = True
session = None
DATA_FILE = "members.json"

ids = ["kkw"]
pws = ["1234"]
names = ["김기원"]
roles = ["admin"]
active = [True]


# ===============================
# 파일 처리
# ===============================
def load_data():
    global ids, pws, names, roles, active

    if not os.path.exists(DATA_FILE):
        save_data()
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    ids = data["ids"]
    pws = data["pws"]
    names = data["names"]
    roles = data["roles"]
    active = data["active"]


def save_data():
    data = {
        "ids": ids,
        "pws": pws,
        "names": names,
        "roles": roles,
        "active": active
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ===============================
# 회원가입
# ===============================
def member_add():
    print("\n[회원가입]")
    uid = input("아이디 : ")

    if uid in ids:
        print("이미 존재하는 아이디")
        return

    pw = input("비밀번호 : ")
    name = input("이름 : ")

    member_add_menu()
    r = input("권한 선택 : ")
    role = "user"
    if r == "1":
        role = "admin"
    elif r == "2":
        role = "manager"

    ids.append(uid)
    pws.append(pw)
    names.append(name)
    roles.append(role)
    active.append(True)

    save_data()
    print("회원가입 완료")


# ===============================
# 로그인
# ===============================
def member_login():
    global session
    print("\n[로그인]")

    uid = input("아이디 : ")
    pw = input("비밀번호 : ")

    if uid in ids:
        idx = ids.index(uid)

        if not active[idx]:
            print("비활성화된 계정")
            return

        if pws[idx] == pw:
            session = idx
            print(f"{names[idx]}님 로그인 성공 ({roles[idx]})")

            if roles[idx] == "admin":
                member_admin()
        else:
            print("비밀번호 오류")
    else:
        print("존재하지 않는 아이디")


# ===============================
# 관리자 기능
# ===============================
def member_admin():
    print("\n[관리자 메뉴]")
    print("1. 비밀번호 변경")
    print("2. 블랙리스트")
    print("3. 권한 변경")
    print("0. 종료")

    sel = input("선택 : ")

    if sel == "1":
        uid = input("대상 아이디 : ")
        if uid in ids:
            idx = ids.index(uid)
            pws[idx] = input("새 비밀번호 : ")

    elif sel == "2":
        uid = input("대상 아이디 : ")
        if uid in ids:
            active[ids.index(uid)] = False

    elif sel == "3":
        uid = input("대상 아이디 : ")
        if uid in ids:
            idx = ids.index(uid)
            roles[idx] = input("admin/manager/user : ")

    save_data()
    print("관리자 작업 완료")


# ===============================
# 로그아웃
# ===============================
def member_logout():
    global session
    session = None
    print("로그아웃 완료")


# ===============================
# 회원정보 수정
# ===============================
def member_modify():
    if session is None:
        print("로그인 필요")
        return

    print("1. 이름 변경")
    print("2. 비밀번호 변경")
    sel = input("선택 : ")

    if sel == "1":
        names[session] = input("새 이름 : ")
    elif sel == "2":
        pws[session] = input("새 비밀번호 : ")

    save_data()
    print("정보 수정 완료")


# ===============================
# 회원탈퇴 / 비활성
# ===============================
def member_delete():
    global session
    if session is None:
        print("로그인 필요")
        return

    print("1. 완전 탈퇴")
    print("2. 계정 비활성")
    sel = input("선택 : ")

    if sel == "1":
        ids.pop(session)
        pws.pop(session)
        names.pop(session)
        roles.pop(session)
        active.pop(session)
        session = None
    elif sel == "2":
        active[session] = False
        session = None

    save_data()
    print("처리 완료")


# ===============================
# 메뉴
# ===============================
def main_menu():
    print("""
==== 회원관리 프로그램 ====
1. 회원가입
2. 로그인
3. 로그아웃
4. 회원정보수정
5. 회원탈퇴
9. 종료
""")


def member_add_menu():
    print("""
1. 관리자
2. 팀장
3. 일반사용자
""")


# ===============================
# 프로그램 시작
# ===============================
load_data()

while run:
    main_menu()
    sel = input(">>> ")

    if sel == "1":
        member_add()
    elif sel == "2":
        member_login()
    elif sel == "3":
        member_logout()
    elif sel == "4":
        member_modify()
    elif sel == "5":
        member_delete()
    elif sel == "9":
        run = False
