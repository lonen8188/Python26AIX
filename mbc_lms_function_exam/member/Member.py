class Member:
    def __init__(self, uid, pw, name, role="user", active=True):
        self.id = uid
        self.pw = pw
        self.name = name
        self.role = role
        self.active = active

    # 파일 저장용 문자열 변환
    def to_line(self):
        return f"{self.id}|{self.pw}|{self.name}|{self.role}|{self.active}\n"

    # 파일 → 객체 변환 (클래스 메서드)
    @classmethod
    def from_line(cls, line):
        uid, pw, name, role, active = line.strip().split("|")
        return cls(uid, pw, name, role, active == "True")
