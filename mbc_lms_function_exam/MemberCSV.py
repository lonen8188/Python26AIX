import csv
import os

FILE_NAME = "members.csv"
run = True
session = None
members = []  # 전체 회원 데이터


# ===============================
# CSV 파일 로드
# ===============================
def load_members():
    global members
    members = []

    if not os.path.exists(FILE_NAME):
        save_members()
        return

    with open(FILE_NAME, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # header skip
        for row in reader:
            row[4] = True if row[4] == "True" else False
            members.append(row)


# ===============================
# CSV 파일 저장
# ===============================
def save_members():
    with open(FILE_NAME, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "pw", "name", "role", "active"])
        for m in members:
            writer.writerow(m)


# ===============================
# 회원가입
# ===============================
def member_add():
    print("\n[회원가입]")
    uid = input("아이디 : ")

    for m in members:
        if m[0] == uid:
            print("이미 존재하는 아이디")
            return

    pw = input("비밀번호 : ")
    name = input("이름 : ")

    print("1.admin  2.manager  3.user")
    r = input("권한 : ")
    role = "user"
    if r == "1":
        role = "admin"
    elif r == "2":
        role = "manager"

    members.append([uid, pw, name, role, True])
    save_members()
    print("회원가입 완료")


# ===============================
# 로그인
# ===============================
def member_login():
    global session
    print("\n[로그인]")

    uid = input("아이디 : ")
    pw = input("비밀번호 : ")

    for i, m in enumerate(members):
        if m[0] == uid:
            if not m[4]:
                print("비활성화된 계정")
                return
            if m[1] == pw:
                session = i
                print(f"{m[2]}님 로그인 성공 ({m[3]})")
                if m[3] == "admin":
                    member_admin()
                return
            else:
                print("비밀번호 오류")
                return

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

    uid = input("대상 아이디 : ")

    for m in members:
        if m[0] == uid:
            if sel == "1":
                m[1] = input("새 비밀번호 : ")
            elif sel == "2":
                m[4] = False
            elif sel == "3":
                m[3] = input("admin/manager/user : ")
            save_members()
            print("처리 완료")
            return

    print("대상 회원 없음")


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
        members[session][2] = input("새 이름 : ")
    elif sel == "2":
        members[session][1] = input("새 비밀번호 : ")

    save_members()
    print("수정 완료")


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
        members.pop(session)
        session = None
    elif sel == "2":
        members[session][4] = False
        session = None

    save_members()
    print("처리 완료")


# ===============================
# 메뉴
# ===============================
def main_menu():
    print("""
==== 회원관리 프로그램(CSV) ====
1. 회원가입
2. 로그인
3. 로그아웃
4. 회원정보수정
5. 회원탈퇴
9. 종료
""")


# ===============================
# 프로그램 시작
# ===============================
load_members()

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
