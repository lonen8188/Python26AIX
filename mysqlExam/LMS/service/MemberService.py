from LMS.common import Session
from LMS.domain import Member


class MemberService:
    @classmethod
    def load(cls):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as cnt FROM members")
                count = cursor.fetchone()['cnt']
                print(f"시스템: 현재 등록된 회원 수는 {count}명입니다.")
        finally:
            conn.close()

    @classmethod
    def login(cls):
        print("\n[로그인]")
        uid = input("아이디: ")
        pw = input("비밀번호: ")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 아이디와 비밀번호가 일치하는 회원 조회
                sql = "SELECT * FROM members WHERE uid = %s AND password = %s"
                cursor.execute(sql, (uid, pw))
                row = cursor.fetchone()

                if row:
                    member = Member.from_db(row)
                    # 2. 계정 활성화 여부 체크
                    if not member.active:
                        print("비활성화된 계정입니다. 관리자에게 문의하세요.")
                        return

                    Session.login(member)
                    print(f"{member.name}님 로그인 성공 ({member.role})")
                else:
                    print("아이디 또는 비밀번호가 틀렸습니다.")
        finally:
            conn.close()

    # MemberService 클래스 내부에 추가하세요
    @classmethod
    def logout(cls):
        # 1. 먼저 세션에 로그인 정보가 있는지 확인
        if not Session.is_login():
            print("\n[알림] 현재 로그인 상태가 아닙니다.")
            return

        # 2. 세션의 로그인 정보 삭제
        Session.logout()
        print("\n[성공] 로그아웃 되었습니다. 안녕히 가세요!")

    @classmethod
    def signup(cls):
        print("\n[회원가입]")
        uid = input("아이디: ")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 중복 체크
                check_sql = "SELECT id FROM members WHERE uid = %s"
                cursor.execute(check_sql, (uid,))
                if cursor.fetchone():
                    print("이미 존재하는 아이디입니다.")
                    return

                pw = input("비밀번호: ")
                name = input("이름: ")

                # 2. 데이터 삽입
                insert_sql = "INSERT INTO members (uid, password, name) VALUES (%s, %s, %s)"
                cursor.execute(insert_sql, (uid, pw, name))
                conn.commit()
                print("회원가입 완료! 로그인해 주세요.")
        except Exception as e:
            conn.rollback()
            print(f"회원가입 오류: {e}")
        finally:
            conn.close()

    @classmethod
    def modify(cls):
        if not Session.is_login():
            print("로그인 후 이용 가능합니다.")
            return

        member = Session.login_member
        print("\n[내 정보 수정]\n1. 이름 변경  2. 비밀번호 변경  0. 취소")
        sel = input("선택: ")

        new_name = member.name
        new_pw = member.pw

        if sel == "1":
            new_name = input("새 이름: ")
        elif sel == "2":
            new_pw = input("새 비밀번호: ")
        else:
            return

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE members SET name = %s, password = %s WHERE id = %s"
                cursor.execute(sql, (new_name, new_pw, member.id))
                conn.commit()

                # 메모리(세션) 정보도 동기화
                member.name = new_name
                member.pw = new_pw
                print("정보 수정 완료")
        finally:
            conn.close()

    @classmethod
    def delete(cls):
        if not Session.is_login(): return
        member = Session.login_member

        print("\n[회원 탈퇴]\n1. 완전 탈퇴  2. 계정 비활성화")
        sel = input("선택: ")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                if sel == "1":
                    sql = "DELETE FROM members WHERE id = %s"
                    cursor.execute(sql, (member.id,))
                    print("회원 탈퇴 완료")
                elif sel == "2":
                    sql = "UPDATE members SET active = FALSE WHERE id = %s"
                    cursor.execute(sql, (member.id,))
                    print("계정 비활성화 완료")

                conn.commit()
                Session.logout()
        finally:
            conn.close()

    @classmethod
    def list_members(cls):
        print("\n[회원 목록 조회]")
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM members")
                rows = cursor.fetchall()
                for row in rows:
                    print(Member.from_db(row))
        finally:
            conn.close()

    # ===============================
    # 관리자 기능 (Admin Only)
    # ===============================

    @classmethod
    def admin_menu(cls):
        # 1. 권한 체크: 로그인 여부와 관리자 권한 확인
        if not Session.is_login() or not Session.login_member.is_admin():
            print("\n[경고] 관리자 권한이 필요합니다.")
            return

        while True:
            print(f"""
    [ 관리자 시스템 - 접속자: {Session.login_member.name} ]
    1. 전체 회원 목록 조회
    2. 회원 권한 변경 (admin/manager/user)
    3. 계정 차단/복구 (Active 설정)
    0. 메인 메뉴로 돌아가기
    """)
            sel = input("메뉴 선택: ")

            if sel == "1":
                cls.list_members()
            elif sel == "2":
                cls.change_role()
            elif sel == "3":
                cls.toggle_active()
            elif sel == "0":
                break
            else:
                print("잘못된 입력입니다.")

    @classmethod
    def list_members(cls):
        print("\n" + "=" * 50)
        print(f"{'ID':<5} | {'UID':<12} | {'NAME':<10} | {'ROLE':<8} | {'STATUS'}")
        print("-" * 50)

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM members ORDER BY id ASC")
                rows = cursor.fetchall()
                for row in rows:
                    m = Member.from_db(row)
                    status = "활동" if m.active else "차단"
                    print(f"{m.id:<5} | {m.uid:<12} | {m.name:<10} | {m.role:<8} | {status}")
        finally:
            conn.close()
        print("=" * 50)

    @classmethod
    def change_role(cls):
        target_uid = input("권한을 변경할 회원의 아이디(uid): ")
        new_role = input("부여할 권한 (admin, manager, user): ").lower()

        if new_role not in ['admin', 'manager', 'user']:
            print("존재하지 않는 권한 타입입니다.")
            return

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE members SET role = %s WHERE uid = %s"
                result = cursor.execute(sql, (new_role, target_uid))
                conn.commit()

                if result > 0:
                    print(f"[{target_uid}]님의 권한이 {new_role}(으)로 변경되었습니다.")
                else:
                    print("해당 아이디를 찾을 수 없습니다.")
        finally:
            conn.close()

    @classmethod
    def toggle_active(cls):
        target_uid = input("상태를 변경할 회원의 아이디(uid): ")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 먼저 현재 상태를 확인
                cursor.execute("SELECT active FROM members WHERE uid = %s", (target_uid,))
                row = cursor.fetchone()

                if not row:
                    print("해당 회원이 존재하지 않습니다.")
                    return

                # 현재 상태 반전 (1 -> 0, 0 -> 1)
                new_status = not bool(row['active'])
                cursor.execute("UPDATE members SET active = %s WHERE uid = %s", (new_status, target_uid))
                conn.commit()

                status_str = "활성화(복구)" if new_status else "비활성화(차단)"
                print(f"[{target_uid}] 계정이 {status_str} 처리되었습니다.")
        finally:
            conn.close()