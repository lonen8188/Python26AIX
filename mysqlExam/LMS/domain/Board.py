class Board:
    def __init__(self, id, title, content, member_id, active=True, writer_name=None, writer_uid=None):
        self.id = id  # DB의 PK
        self.title = title
        self.content = content
        self.member_id = member_id  # 작성자의 고유 번호(FK)
        self.active = active  # 삭제 여부 (TINYINT 1/0)

        # JOIN을 통해 가져올 추가 정보들 (선택 사항)
        self.writer_name = writer_name
        self.writer_uid = writer_uid

    @classmethod
    def from_db(cls, row: dict):
        if not row: return None
        return cls(
            id=row.get('id'),
            title=row.get('title'),
            content=row.get('content'),
            member_id=row.get('member_id'),
            active=bool(row.get('active')),
            # JOIN 쿼리 시 사용할 이름과 아이디
            writer_name=row.get('name'),
            writer_uid=row.get('uid')
        )

    def __str__(self):
        # 목록 출력 시 보여줄 형식
        writer = self.writer_name if self.writer_name else f"ID:{self.member_id}"
        return f"{self.id:<4} | {self.title:<20} | {writer:<10}"