# domain/Item.py

class Item:
    # 카테고리 상수
    CATEGORY_ETC = "잡화"
    CATEGORY_DRINK = "음료"
    CATEGORY_IT = "IT"
    CATEGORY_BOOK = "도서"

    CATEGORIES = [CATEGORY_ETC, CATEGORY_DRINK, CATEGORY_IT, CATEGORY_BOOK]

    def __init__(self, code, name, price, stock, category):
        if category not in Item.CATEGORIES:
            raise ValueError("잘못된 카테고리입니다.")

        self.code = code
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

    def decrease_stock(self, qty=1): # 서비스에서 직접 stock -= 1 안 함 → 객체지향
        # qty(quantity:수량) = 1은 1씩 재고 감소
        # qty=2는 재고2개 감소
        # qty 처리를 안하면 장바구니 리스트에 같은 상품이 여려개 들어감
        # 재고 계산이 꼬임 / 구매 금액 계산이 어려움 / db에 용이
        if self.stock < qty:
            return False
        self.stock -= qty
        return True

    def __str__(self):
        return f"{self.code} | {self.name} | {self.category} | {self.price}원 | 재고:{self.stock}"

    def to_line(self):
        return f"{self.code},{self.name},{self.price},{self.stock},{self.category}\n"

    @classmethod
    def from_line(cls, line):
        code, name, price, stock, category = line.strip().split(",")
        return cls(code, name, int(price), int(stock), category)
