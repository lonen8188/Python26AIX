from LMS.common import Session
from LMS.domain import Member
from LMS.domain import Order


class OrderService:

    @classmethod
    def add_order(cls, total_price):
        """구매 확정 시 호출: DB에 주문 정보 저장"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # SQL: 누가, 얼마를 냈는지 저장 (status는 기본 'PAID')
                sql = "INSERT INTO orders (member_id, total_price) VALUES (%s, %s)"
                cursor.execute(sql, (Session.login_member.id, total_price))
                conn.commit()
        finally:
            conn.close()

    @classmethod
    def my_orders(cls):
        if not Session.is_login(): return

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 주문 요약 목록 가져오기
                sql = "SELECT * FROM orders WHERE member_id = %s ORDER BY id DESC"
                cursor.execute(sql, (Session.login_member.id,))
                orders = cursor.fetchall()

                if not orders:
                    print("주문 내역이 없습니다.")
                    return

                for row in orders:
                    print(f"\n[주문번호: {row['id']}] 날짜: {row['created_at']} | 상태: {row['status']}")

                    # 2. 해당 주문의 상세 상품 정보 가져오기 (JOIN 활용)
                    sql_detail = """
                                 SELECT oi.*, i.name
                                 FROM order_items oi
                                          JOIN items i ON oi.item_id = i.id
                                 WHERE oi.order_id = %s \
                                 """
                    cursor.execute(sql_detail, (row['id'],))
                    details = cursor.fetchall()

                    for d in details:
                        print(f"   - {d['name']} | {d['price']}원 | {d['qty']}개")
                    print(f"   > 총 결제금액: {row['total_price']}원")
        finally:
            conn.close()

    @classmethod
    def cancel_order(cls):
        """주문 취소: PAID 상태를 CANCELED로 변경"""
        cls.my_orders()  # 목록 먼저 보여주기
        order_id = input("\n취소할 주문 번호(ID) 입력: ")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 본인 주문이고 PAID 상태인 것만 취소 가능
                sql = "UPDATE orders SET status='CANCELED' WHERE id=%s AND member_id=%s AND status='PAID'"
                cursor.execute(sql, (order_id, Session.login_member.id))
                conn.commit()

                if cursor.rowcount > 0:
                    print(f"[{order_id}]번 주문이 취소되었습니다.")
                else:
                    print("취소할 수 없는 주문이거나 번호가 잘못되었습니다.")
        finally:
            conn.close()

    @classmethod
    def request_refund(cls):
        """환불 요청: CANCELED 상태인 주문을 REFUND_REQ로 변경"""
        print("\n--- 환불 요청 가능 목록 (취소된 주문) ---")
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT o.*, m.name FROM orders o JOIN members m ON o.member_id=m.id WHERE o.member_id=%s AND o.status='CANCELED'"
                cursor.execute(sql, (Session.login_member.id,))
                rows = cursor.fetchall()

                for row in rows: print(Order.from_db(row))

                order_id = input("\n환불 요청할 주문 번호(ID): ")
                cursor.execute("UPDATE orders SET status='REFUND_REQ' WHERE id=%s AND member_id=%s",
                               (order_id, Session.login_member.id))
                conn.commit()
                print("환불 요청이 완료되었습니다.")
        finally:
            conn.close()

    @classmethod
    def all_orders(cls):
        """관리자 전용: 전체 주문 조회"""
        if not Session.is_manager(): return

        print("\n[관리자: 전체 판매 내역]")
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT o.*, m.name FROM orders o JOIN members m ON o.member_id = m.id ORDER BY o.id DESC"
                cursor.execute(sql)
                for row in cursor.fetchall():
                    print(Order.from_db(row))
        finally:
            conn.close()


    @classmethod
    def cancel_order(cls):
        """[사용자] 주문 취소 (PAID -> CANCELED) 및 재고 즉시 복구"""
        cls.my_orders()
        order_id = input("\n취소할 주문 번호(ID) 입력: ")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 상태 확인 (본인 주문이고 결제완료 상태인지)
                cursor.execute("SELECT * FROM orders WHERE id=%s AND member_id=%s AND status='PAID'",
                               (order_id, Session.login_member.id))
                order = cursor.fetchone()

                if not order:
                    print("취소 가능한 주문이 아닙니다.")
                    return

                # 2. 상세 내역(order_items)을 조회해서 각 상품 재고 복구
                cursor.execute("SELECT item_id, qty FROM order_items WHERE order_id=%s", (order_id,))
                items = cursor.fetchall()
                for item in items:
                    cursor.execute("UPDATE items SET stock = stock + %s WHERE id = %s",
                                   (item['qty'], item['item_id']))

                # 3. 주문 상태 변경
                cursor.execute("UPDATE orders SET status='CANCELED' WHERE id=%s", (order_id,))

                conn.commit()
                print(f"주문 번호 [{order_id}] 취소 및 재고 복구가 완료되었습니다.")
        except Exception as e:
            conn.rollback()
            print(f"취소 실패: {e}")
        finally:
            conn.close()

    @classmethod
    def request_refund(cls):
        """[사용자] 환불 요청 (CANCELED -> REFUND_REQ)"""
        order_id = input("\n환불 요청할 주문 번호(ID): ")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 취소된 주문에 대해서만 환불 요청 가능
                sql = "UPDATE orders SET status='REFUND_REQ' WHERE id=%s AND member_id=%s AND status='CANCELED'"
                cursor.execute(sql, (order_id, Session.login_member.id))
                conn.commit()

                if cursor.rowcount > 0:
                    print("환불 요청이 접수되었습니다. 관리자 승인을 기다려주세요.")
                else:
                    print("환불 요청이 불가능한 주문입니다. (취소된 주문만 가능)")
        finally:
            conn.close()

    @classmethod
    def approve_refund(cls):
        """[관리자] 환불 승인 (REFUND_REQ -> REFUNDED)"""
        if not Session.is_manager(): return

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT o.*, m.name FROM orders o JOIN members m ON o.member_id=m.id WHERE o.status='REFUND_REQ'")
                rows = cursor.fetchall()
                if not rows:
                    print("환불 대기 중인 주문이 없습니다.")
                    return

                for r in rows: print(f"ID:{r['id']} | 요청자:{r['name']} | 금액:{r['total_price']}")

                order_id = input("\n승인할 주문 번호(ID): ")
                cursor.execute("UPDATE orders SET status='REFUNDED' WHERE id=%s AND status='REFUND_REQ'", (order_id,))
                conn.commit()
                print(f"주문 번호 [{order_id}] 환불 승인 완료.")
        finally:
            conn.close()