# 로그인 상태 관리 클래스
# 현재 로그인한 회원(Member 객체)을 보관
# 전역변수 대신 객체로 돌려씀
# 로그인, 로그아웃, 로그인여부, 관리자인지....

# 이곳은 객체가 돌아다녀야 됨 -> @classmethod 처리 필수

class Session:
    # def __init__(self) 필요없음!!
    # cls로 Member를 활용하기 때문에

    login_member = None # 현재 로그인한 객체
    # 로그인을 했으면 login_member = Member()
    # 로그아웃 했으면 login_member = None

    cart = []  # 장바구니 (Item 객체 저장)

    @classmethod # cls와 세트로 구현
    def login(cls, member): # Session.login(member)
        # 로그인을 성공하면 @staticmethod로 만든 객체를 클래스로 변환
        cls.login_member = member
        cls.cart = []  # 로그인 시 장바구니 초기화

    @classmethod
    def logout(cls):    # Session.logout()
        cls.login_member = None
        cls.cart = []

    @classmethod
    def is_login(cls):
        # 로그인 상태인지???
        return cls.login_member is not None
        # cls : Member객체       None 아니면 True

    @classmethod
    def is_admin(cls):
        # 현재 admin 인지 ???
        return cls.is_login() and cls.login_member.is_admin()
        #           True      and       Member().is_admin()
        #                                    True
        #                     and는 둘다 True = True 처리함

    @classmethod
    def is_manager(cls):
        # 현재 admin 인지 ???
        return cls.is_login() and cls.login_member.is_manager()
        #           True      and       Member().is_admin()
        #                                    True
        #                     and는 둘다 True = True 처리함