import pymysql # pip install pymysql


# DB와 연결이 설정되면, "cursor()" 메소드를 사용하여 커서 객체를 만들어 SQL 쿼리문을 실행할 수 있습니다.
# cursor = db.cursor()

# sql = """
# CREATE TABLE products (
# 	product_id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     price DECIMAL(10, 2) NOT NULL,
#     quantity INT DEFAULT 0
#  )
#  """
#
#  cursor.execute(sql) # SQL 쿼리문 실행
#  db.commit() # DB 변경사항 반영

# product_data = [
#     ('Product A', 19.99, 10),
#     ('Product B', 29.99, 20),
#     ('Product C', 39.99, 30)
# ]
#
# insert_sql = "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)"
# for product in product_data:
# 	cursor.execute(insert_sql, product)
#
# db.commit()

# cursor.execute("SELECT * FROM products")
# rows = cursor.fetchall() 모든행을 가져온다.
# for row in rows:
# 	print(row)

# cursor.execute("SELECT * FROM products")
# row = cursor.fetchone() 하나의 행을 가져온다.
# while row is not None:
# 	print(row)
#     row = cursor.fetchone()

# cursor.execute("SELECT * FROM products")
# rows = cursor.fetchmany(2) size만큼 행을 가져온다.
# while rows:
# 	for row in rows:
#     	print(row)
#     rows = cursor.fetchmany(2)


class Session:
    # 현재 로그인된 Member 객체를 저장 (None이면 로그아웃 상태)
    login_member = None
    cart = []

    @staticmethod
    def get_connection():
        return pymysql.connect(
            host='localhost',
            user='mbc',
            password='1234', # 본인의 비밀번호로 변경
            db='lms',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
            # dict 타입으로 처리함
        )

    @classmethod
    def login(cls, member):
        cls.login_member = member
        cls.cart = []  # 로그인 시 장바구니 비우기

    @classmethod
    def logout(cls):
        cls.login_member = None
        cls.cart = []

    @classmethod
    def is_login(cls):
        return cls.login_member is not None

    # 추가: 권한 체크 메서드 (서비스 계층에서 사용됨)
    @classmethod
    def is_admin(cls):
        return cls.is_login() and cls.login_member.role == "admin"

    @classmethod
    def is_manager(cls):
        # 매니저이거나 어드민이면 참 (보통 어드민이 매니저 권한을 포함함)
        return cls.is_login() and cls.login_member.role in ("manager", "admin")

