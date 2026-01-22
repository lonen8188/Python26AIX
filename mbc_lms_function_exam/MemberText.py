import os

# ===============================
# 전역 변수 영역
# ===============================

FILE_NAME = "members.txt"   # 회원 정보를 저장할 메모장 파일명
run = True                  # 프로그램 전체 실행 여부
session = None              # 로그인 상태 저장 (로그인한 회원의 인덱스)
members = []                # 회원 정보 저장 리스트
# members 구조:
# [아이디, 비밀번호, 이름, 권한(admin/manager/user), 활성화여부(True/False)]


# ===============================
# 파일에서 회원 정보 읽기
# ===============================
def load_members():
    """
    members.txt 파일을 읽어서 members 리스트에 저장
    """
    global members
    members = []  # 기존 데이터 초기화

    # 파일이 없으면 새 파일 생성
    if not os.path.exists(FILE_NAME):
        save_members()
        return

    # 파일 열어서 한 줄씩 읽기
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        for line in f:
            # 줄 끝의 개행 제거 후 | 기준으로 분리
            data = line.strip().split("|")

            # 문자열 True/False → Boolean 타입으로 변환
            data[4] = True if data[4] == "True" else False

            members.append(data)


# ===============================
# 회원 정보를 파일에 저장
# ===============================
def save_members():
    """
    members 리스트 내용을 members.txt 파일에 저장
    """
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for m in members:
            # 리스트 데이터를 | 로 연결하여 한 줄로 저장
            line = f"{m[0]}|{m[1]}|{m[2]}|{m[3]}|{m[4]}\n"
            f.write(line)


# ===============================
# 회원가입 (Create)
# ===============================
def member_add():
    print("\n[회원가입]")
    uid = input("아이디 : ")

    # 아이디 중복 검사
    for m in members:
        if m[0] == uid:
            print("이미 존재하는 아이디입니다.")
            return

    pw = input("비밀번호 : ")
    name = input("이름 : ")

    # 권한 선택
    print("1.admin  2.manager  3.user")
    r = input("권한 선택 : ")

    role = "user"   # 기본 권한
    if r == "1":
        role = "admin"
    elif r == "2":
        role = "manager"

    # 회원 정보 추가
    members.append([uid, pw, name, role, True])

    save_members()  # 파일 저장
    print("회원가입 완료")


# ===============================
# 로그인 (Read + session)
# ===============================
def member_login():
    global session
    print("\n[로그인]")

    uid = input("아이디 : ")
    pw = input("비밀번호 : ")

    # 회원 목록에서 아이디 검색
    for i, m in enumerate(members):
        if m[0] == uid:
            # 비활성화 계정 체크
            if not m[4]:
                print("비활성화된 계정입니다.")
                return

            # 비밀번호 확인
            if m[1] == pw:
                session = i   # 로그인 성공 → 인덱스 저장
                print(f"{m[2]}님 로그인 성공 ({m[3]})")

                # 관리자일 경우 관리자 메뉴 호출
                if m[3] == "admin":
                    member_admin()
                return
            else:
                print("비밀번호가 틀렸습니다.")
                return

    print("존재하지 않는 아이디입니다.")


# ===============================
# 관리자 기능 (권한자만)
# ===============================
def member_admin():
    print("\n[관리자 메뉴]")
    print("1. 비밀번호 변경")
    print("2. 블랙리스트 처리")
    print("3. 권한 변경")
    print("0. 종료")

    sel = input("선택 : ")
    uid = input("대상 아이디 : ")

    for m in members:
        if m[0] == uid:
            # 비밀번호 변경
            if sel == "1":
                m[1] = input("새 비밀번호 : ")

            # 블랙리스트(비활성화)
            elif sel == "2":
                m[4] = False

            # 권한 변경
            elif sel == "3":
                m[3] = input("admin / manager / user : ")

            save_members()
            print("관리자 작업 완료")
            return

    print("대상 회원이 없습니다.")


# ===============================
# 로그아웃
# ===============================
def member_logout():
    global session
    session = None  # 로그인 상태 초기화
    print("로그아웃 완료")


# ===============================
# 회원정보 수정 (Update)
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
        members[session][2] = input("새 이름 : ")
    elif sel == "2":
        members[session][1] = input("새 비밀번호 : ")

    save_members()
    print("정보 수정 완료")


# ===============================
# 회원탈퇴 / 비활성화 (Delete)
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

    # 완전 삭제
    if sel == "1":
        members.pop(session)
        session = None

    # 비활성화 처리
    elif sel == "2":
        members[session][4] = False
        session = None

    save_members()
    print("처리 완료")


# ===============================
# 메인 메뉴 출력
# ===============================
def main_menu():
    print("""
==== 회원관리 프로그램 (TXT 파일 기반) ====
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

load_members()  # 프로그램 시작 시 파일 로드

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
