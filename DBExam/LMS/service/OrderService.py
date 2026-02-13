from LMS.common.session import Session


class OrderService:
    @staticmethod
    def create_order(member_id, item_id, quantity):
        conn = Session.get_connection()
        cursor = conn.cursor()

        try:
            # 1. 재고 확인 및 상품 가격 가져오기
            cursor.execute("SELECT price, stock FROM items WHERE id = %s FOR UPDATE", (item_id,))
            item = cursor.fetchone()

            if not item or item['stock'] < quantity:
                return False, "재고가 부족합니다."

            # 2. orders 테이블 삽입 (총 금액 계산: 가격 * 수량)
            total_price = item['price'] * quantity
            cursor.execute(
                "INSERT INTO orders (member_id, total_price) VALUES (%s, %s)",
                (member_id, total_price)
            )
            order_id = cursor.lastrowid

            # 3. order_items 테이블 삽입
            cursor.execute(
                "INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, item_id, quantity, item['price'])
            )

            # 4. 재고 차감 (매우 중요!)
            cursor.execute(
                "UPDATE items SET stock = stock - %s WHERE id = %s",
                (quantity, item_id)
            )

            # 모든 작업 성공 시 확정
            conn.commit()
            return True, "주문이 완료되었습니다."

        except Exception as e:
            conn.rollback()
            print(f"주문 에러: {e}")
            return False, "주문 처리 중 오류가 발생했습니다."
        finally:
            cursor.close()