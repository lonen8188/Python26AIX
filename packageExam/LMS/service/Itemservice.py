# service/ItemService.py

import os
from packageExam.LMS.domain import *
from packageExam.LMS.service import *
from packageExam.LMS.service.OrderService import OrderService

from packageExam.LMS.common import Session

FILE_PATH = "data/item.txt"


class ItemService:
    items = []

    @classmethod
    def load(cls):
        cls.items = []
        if not os.path.exists(FILE_PATH):
            os.makedirs("data", exist_ok=True)
            cls.save()
            return

        with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                cls.items.append(Item.from_line(line))

    @classmethod
    def save(cls):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            for item in cls.items:
                f.write(item.to_line())

    # =========================
    # 기능 영역
    # =========================

    @classmethod
    def add_item(cls):
        if not Session.is_manager():
            print("manager만 등록 가능합니다.")
            return

        code = input("아이템 코드: ")
        if any(i.code == code for i in cls.items):
            print("이미 존재하는 코드입니다.")
            return

        name = input("아이템 이름: ")
        price = int(input("가격: "))
        stock = int(input("재고 수량: "))

        print("\n카테고리 선택")
        for idx, cat in enumerate(Item.CATEGORIES, start=1):
            print(f"{idx}. {cat}")

        sel = int(input("번호 선택: "))
        if sel < 1 or sel > len(Item.CATEGORIES):
            print("잘못된 선택입니다.")
            return

        category = Item.CATEGORIES[sel - 1]
        cls.items.append(Item(code, name, price, stock, category))
        cls.save()
        print("아이템 등록 완료")

    @classmethod
    def list_items(cls):
        print("\n[아이템 목록]")
        if not cls.items:
            print("등록된 아이템이 없습니다.")
            return

        for item in cls.items:
            print(item)

        if not Session.is_login():
            print("\n※ 로그인 후 장바구니 이용 가능")
            return

        code = input("장바구니에 담을 상품 코드(엔터:취소): ")
        if code == "":
            return

        qty = int(input("수량: "))

        for cart in Session.cart:
            if cart["item"].code == code:
                cart["qty"] += qty
                print("장바구니 수량 증가")
                return

        for item in cls.items:
            if item.code == code:
                Session.cart.append({"item": item, "qty": qty})
                print("장바구니에 추가됨")
                return

        print("상품을 찾을 수 없습니다.")

    @classmethod
    def print_items(cls):
        print("\n[상품 목록]")
        for item in cls.items:
            print(item)

    @classmethod
    def view_cart(cls):
        if not Session.cart:
            print("장바구니가 비어 있습니다.")
            return

        print("\n[장바구니]")
        total = 0
        for cart in Session.cart:
            item = cart["item"]
            qty = cart["qty"]
            price = item.price * qty
            total += price
            print(f"[{item.code}] {item.name} | 단가:{item.price}원 | 수량:{qty} | 합계:{price}원")

        print(f"총 금액: {total}원")

    @classmethod
    def modify_item(cls):
        cls.print_items()
        code = input("수정할 상품 코드: ")

        for item in cls.items:
            if item.code == code:
                item.name = input("새 상품명: ")
                item.price = int(input("새 가격: "))
                print("상품 수정 완료")
                cls.save()
                return

        print("해당 상품이 없습니다.")

    @classmethod
    def update_stock(cls):
        if not Session.is_manager():
            print("manager만 수정 가능합니다.")
            return
        cls.print_items()
        code = input("수정할 아이템 코드: ")
        for item in cls.items:
            if item.code == code:
                item.stock = int(input("새 재고 수량: "))
                cls.save()
                print("재고 수정 완료")
                return

        print("아이템을 찾을 수 없습니다.")



    @classmethod
    def delete_item(cls):
        if not Session.is_manager():
            print("manager만 삭제 가능합니다.")
            return
        cls.print_items()
        code = input("삭제할 아이템 코드: ")
        for i, item in enumerate(cls.items):
            if item.code == code:
                cls.items.pop(i)
                cls.save()
                print("아이템 삭제 완료")
                return

        print("아이템을 찾을 수 없습니다.")

    @classmethod
    def modify_cart_qty(cls):
        if not Session.cart:
            print("장바구니가 비어 있습니다.")
            return

        cls.view_cart()

        code = input("수량 변경할 상품 코드: ")
        qty = int(input("변경할 수량(0이면 삭제): "))

        for cart in Session.cart:
            if cart["item"].code == code:
                if qty <= 0:
                    Session.cart.remove(cart)
                    print("장바구니에서 제거되었습니다.")
                else:
                    cart["qty"] = qty
                    print("수량이 변경되었습니다.")
                return

        print("해당 상품이 장바구니에 없습니다.")


    @classmethod
    def purchase(cls): # 장바구니 및 결재 용
        if not Session.is_login():
            print("로그인 후 이용 가능합니다.")
            return

        if not Session.cart:
            print("장바구니가 비어 있습니다.")
            return

        while True:
            print("\n[구매 진행]")
            cls.view_cart()

            print("""
        1. 수량 변경
        2. 구매 확정
        0. 취소
        """)

            sel = input("선택: ")

            if sel == "1":
                cls.modify_cart_qty()
            elif sel == "2":
                break
            elif sel == "0":
                return
            else:
                print("잘못된 선택")

        # 재고 확인
        for cart in Session.cart:
            item = cart["item"]
            qty = cart["qty"]
            if item.stock < qty:
                print(f"{item.name} 재고 부족")
                return

        total = 0
        for cart in Session.cart:
            item = cart["item"]
            qty = cart["qty"]

            item.decrease_stock(qty)
            OrderService.add_order(item, qty)
            total += item.price * qty

        cls.save()
        Session.cart.clear()

        print(f"\n구매 완료! 총 결제 금액: {total}원")
        print(f"{Session.login_member.name}님 감사합니다 ")

    @classmethod
    def restore_stock(cls, code, qty): # 주문취소시 재고복귀
        for item in cls.items:
            if item.code == code:
                item.stock += qty
                cls.save()
                return

    @classmethod
    def admin_menu(cls):
        # 로그인 & 관리자 권한 체크
        if not Session.is_login():
            print("로그인 후 이용 가능합니다.")
            return

        if Session.login_member.role != "manager":
            print("manager만 접근 가능합니다.")
            return

        while True:
            print("""
    ==========================
       상품 관리자 메뉴
    ==========================
    1. 상품 등록
    2. 상품 목록
    3. 상품 수정
    4. 재고 관리
    5. 상품 삭제
    6. 판매 내역보기
    7. 환불 승인
    
    0. 이전 메뉴
    """)

            sel = input(">>> ")

            if sel == "1":
                cls.add_item()
            elif sel == "2":
                cls.print_items()
            elif sel == "3":
                cls.modify_item()
            elif sel == "4":
                cls.update_stock()
            elif sel == "5":
                cls.delete_item()
            elif sel == "6":
                OrderService.all_orders()
            elif sel == "7":
                OrderService.approve_refund()
            elif sel == "0":
                break
            else:
                print("메뉴 번호를 다시 선택하세요.")

    @classmethod
    def run(cls):
        cls.load()

        subrun = True
        while subrun:
            print("""
==========================
  상품 관리 시스템
==========================
1. 상품 목록 및 구매
2. 장바구니 보기
3. 구매
4. 구매 내역보기
5. 구매 취소
6. 환불 처리

9. 상품 관리(관리자)

0. 이전 메뉴
""")

            sel = input(">>> ")

            if sel == "1":
                cls.list_items()  # 상품 목록 + 장바구니 담기
            elif sel == "2":
                cls.view_cart()  # 장바구니 보기
            elif sel == "3":
                cls.purchase()  # 구매 → 재고 감소
            elif sel == "4":
                OrderService.my_orders() # 내 구매내역
            elif sel == "5":
                OrderService.cancel_order() # 구매취소
            elif sel == "6":
                OrderService.request_refund() # 환불 처리
            elif sel == "9":
                cls.admin_menu()  # 관리자 상품 관리
            elif sel == "0":
                subrun = False
            else:
                print("메뉴 번호를 다시 선택하세요.")