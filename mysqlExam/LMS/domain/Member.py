class Member:
    def __init__(self, id, uid, pw, name, role="user", active=True):
        self.id = id  # DB의 PK
        self.uid = uid  # 아이디
        self.pw = pw  # 비밀번호
        self.name = name  # 이름
        self.role = role  # 권한
        self.active = active  # 활성화 여부

    @classmethod
    def from_db(cls, row: dict):
        """
        DictCursor로부터 전달받은 딕셔너리 데이터를 Member 객체로 변환합니다.
        """
        if not row:
            return None

        return cls(
            id=row.get('id'),
            uid=row.get('uid'),
            pw=row.get('password'),  # DB 컬럼명이 'password'인 경우
            name=row.get('name'),
            role=row.get('role'),
            active=bool(row.get('active'))
        )

    def is_admin(self):
        return self.role == "admin"

    def __str__(self):
        return f"{self.name}({self.uid}) [{self.role}]"