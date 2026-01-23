import os

from packageExam.LMS.domain import *
from packageExam.LMS.service import *
from packageExam.LMS.common import Session

FILE_PATH = "data/orders.txt"

class OrderService:
    orders = []

    @classmethod
    def load(cls):
        cls.orders = []

        if not os.path.exists(FILE_PATH):
            os.makedirs("data", exist_ok=True)
            open(FILE_PATH, "w", encoding="utf-8").close()
            return

        with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                cls.orders.append(Order.from_line(line))

    @classmethod
    def save(cls):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            for order in cls.orders:
                f.write(order.to_line())

    @classmethod
    def add_order(cls, item, qty):
        member = Session.login_member
        order = Order(member.uid, item.code, item.name, qty, item.price)
        cls.orders.append(order)
        cls.save()

    @classmethod
    def my_orders(cls):
        if not Session.is_login():
            print("로그인 후 이용 가능합니다.")
            return

        print("\n[내 구매 내역]")
        for order in cls.orders:
            if order.user_id == Session.login_member.uid:
                print(order)

    @classmethod
    def all_orders(cls):
        if Session.login_member.role != "manager":
            print("manager만 조회 가능합니다.")
            return

        print("\n[전체 구매 내역]")
        for order in cls.orders:
            print(order)

    @classmethod
    def cancel_order(cls): # 주문취소 기능 추가
        if not Session.is_login():
            print("로그인 후 이용 가능합니다.")
            return

        my_orders = [
            o for o in cls.orders
            if o.user_id == Session.login_member.uid and o.status == "PAID"
        ]

        if not my_orders:
            print("취소 가능한 주문이 없습니다.")
            return

        print("\n[구매 취소]")
        for i, o in enumerate(my_orders):
            print(f"{i}. {o}")

        idx = int(input("취소할 번호 선택: "))
        order = my_orders[idx]

        # 재고 복구
        from packageExam.LMS.service.ItemService import ItemService
        ItemService.restore_stock(order.item_code, order.qty)

        order.status = "CANCELED"
        cls.save()

        print("구매가 취소되었습니다.")

    @classmethod
    def request_refund(cls): # 사용자가 환불 요청
        if not Session.is_login():
            print("로그인 후 이용 가능합니다.")
            return

        orders = [
            o for o in cls.orders
            if o.user_id == Session.login_member.uid and o.status == "CANCELED"
        ]

        if not orders:
            print("환불 요청 가능한 주문이 없습니다.")
            return

        print("\n[환불 요청]")
        for i, o in enumerate(orders):
            print(f"{i}. {o}")

        idx = int(input("환불 요청할 번호: "))
        orders[idx].status = "REFUND_REQ"
        cls.save()

        print("환불 요청이 접수되었습니다.")

    @classmethod
    def approve_refund(cls):
        if not Session.is_login() or Session.login_member.role != "manager":
            print("manage만 승인 가능합니다.")
            return

        req_orders = [o for o in cls.orders if o.status == "REFUND_REQ"]

        if not req_orders:
            print("환불 승인 대기 주문이 없습니다.")
            return

        print("\n[환불 승인 대기 목록]")
        for i, o in enumerate(req_orders):
            print(f"{i}. {o} / 사용자: {o.user_id}")

        idx = int(input("승인할 번호 선택: "))
        order = req_orders[idx]

        # 재고 복구
        from packageExam.LMS.service.ItemService import ItemService
        ItemService.restore_stock(order.item_code, order.qty)

        order.status = "REFUNDED"
        cls.save()

        print("환불이 승인되었습니다.")