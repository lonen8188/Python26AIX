from datetime import datetime

class Order:
    def __init__(self, user_id, item_code, item_name, qty, price, status="PAID"):
        self.user_id = user_id
        self.item_code = item_code
        self.item_name = item_name
        self.qty = qty
        self.price = price
        self.status = status  # PAID / CANCELED / REFUNDED
        #                      결제완료 / 취소됨 / 환불됨

    def to_line(self):
        return f"{self.user_id}|{self.item_code}|{self.item_name}|{self.qty}|{self.price}|{self.status}\n"

    @classmethod
    def from_line(cls, line):
        u, c, n, q, p, s = line.strip().split("|")
        return cls(u, c, n, int(q), int(p), s)

    def __str__(self):
        return f"{self.item_name} x{self.qty} ({self.status})"