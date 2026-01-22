# pip install pymysql
import pymysql

# CREATE DATABASE mbc;
# USE mbc;
#
# CREATE TABLE members (
#     id VARCHAR(20) PRIMARY KEY,
#     pw VARCHAR(100) NOT NULL,
#     name VARCHAR(20) NOT NULL,
#     role ENUM('admin','manager','user') DEFAULT 'user',
#     active BOOLEAN DEFAULT TRUE
# );

# ===============================
# 전역 변수
# ===============================
run = True
session = None   # 로그인한 사용자 정보(dict)

# ===============================
# DB 연결
# ===============================
def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",   # 본인 DB 비밀번호
        db="mbc",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )

# ===============================
# 회원가입 (C)
# ===============================
def member_add():
    conn = get_conn()
    cur = conn.cursor()

    uid = input("아이디 : ")
    pw = input("비밀번호 : ")
    name = input("이름 : ")

    print("1.admin  2.manager  3.user")
    r = input("권한 : ")
    role = "user"
    if r == "1": role = "admin"
    elif r == "2": role = "manager"

    try:
        cur.execute(
            "INSERT INTO members(id,pw,name,role) VALUES(%s,%s,%s,%s)",
            (uid, pw, name, role)
        )
        conn.commit()
        print("회원가입 완료")
    except:
        print("이미 존재하는 아이디")
    finally:
        conn.close()

# ===============================
# 로그인 (R + session)
# ===============================
def member_login():
    global session
    conn = get_conn()
    cur = conn.cursor()

    uid = input("아이디 : ")
    pw = input("비밀번호 : ")

    cur.execute(
        "SELECT * FROM members WHERE id=%s AND pw=%s AND active=TRUE",
        (uid, pw)
    )
    user = cur.fetchone()
    conn.close()

    if user:
        session = user
        print(f"{user['name']}님 로그인 성공 ({user['role']})")
        if user["role"] == "admin":
            member_admin()
    else:
        print("로그인 실패")

# ===============================
# 관리자 기능 (R/U)
# ===============================
def member_admin():
    conn = get_conn()
    cur = conn.cursor()

    print("\n[관리자 메뉴]")
    print("1. 비밀번호 변경")
    print("2. 블랙리스트")
    print("3. 권한 변경")
    print("0. 종료")

    sel = input("선택 : ")
    uid = input("대상 아이디 : ")

    if sel == "1":
        new_pw = input("새 비밀번호 : ")
        cur.execute("UPDATE members SET pw=%s WHERE id=%s", (new_pw, uid))

    elif sel == "2":
        cur.execute("UPDATE members SET active=FALSE WHERE id=%s", (uid,))

    elif sel == "3":
        role = input("admin/manager/user : ")
        cur.execute("UPDATE members SET role=%s WHERE id=%s", (role, uid))

    conn.commit()
    conn.close()
    print("관리자 작업 완료")

# ===============================
# 로그아웃
# ===============================
def member_logout():
    global session
    session = None
    print("로그아웃 완료")

# ===============================
# 회원정보 수정 (U)
# ===============================
def member_modify():
    if session is None:
        print("로그인 필요")
        return

    conn = get_conn()
    cur = conn.cursor()

    print("1. 이름 변경")
    print("2. 비밀번호 변경")
    sel = input("선택 : ")

    if sel == "1":
        name = input("새 이름 : ")
        cur.execute("UPDATE members SET name=%s WHERE id=%s",
                    (name, session["id"]))
    elif sel == "2":
        pw = input("새 비밀번호 : ")
        cur.execute("UPDATE members SET pw=%s WHERE id=%s",
                    (pw, session["id"]))

    conn.commit()
    conn.close()
    print("수정 완료")

# ===============================
# 회원탈퇴 / 비활성 (D)
# ===============================
def member_delete():
    global session
    if session is None:
        print("로그인 필요")
        return

    conn = get_conn()
    cur = conn.cursor()

    print("1. 완전 탈퇴")
    print("2. 계정 비활성")
    sel = input("선택 : ")

    if sel == "1":
        cur.execute("DELETE FROM members WHERE id=%s",
                    (session["id"],))
    elif sel == "2":
        cur.execute("UPDATE members SET active=FALSE WHERE id=%s",
                    (session["id"],))

    conn.commit()
    conn.close()
    session = None
    print("처리 완료")

# ===============================
# 메뉴
# ===============================
def main_menu():
    print("""
==== 회원관리 프로그램 (MariaDB) ====
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
while run:
    main_menu()
    sel = input(">>> ")

    if sel == "1": member_add()
    elif sel == "2": member_login()
    elif sel == "3": member_logout()
    elif sel == "4": member_modify()
    elif sel == "5": member_delete()
    elif sel == "9": run = False
