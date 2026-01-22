# 회원에 대한 CRUD 객체용 클래스

class Member:

    # member = Member("id","pw","name","role")
    def __init__(self, uid, pw, name, role="user", active=True):
        # 객체가 생성될때 초기값 처리함
        self.uid = uid      # 아이디
        self.pw = pw        # 비밀번호
        self.name = name    # 이름
        self.role = role    # 권한 (admin / manager / user)
        self.active = active # 활성화여부(True / False)

    def __str__(self): # print(member) 처리되는용 (테스트용)
        status = "활성" if self.active else "비활성"
        return f"{self.uid} | {self.name} | {self.role} | {status}"

    def to_line(self):
        # 파일 저장용 (직렬화) : 메모리에 있는 객체를 메모장으로 저장할 문자열로 변환
        return f"{self.uid}|{self.pw}|{self.name}|{self.role}|{self.active}"
        # kkw|1111|김기원|admin|True
        # lhj|5678|임효정|manager|True
        # ljj|8888|이재정|user|True

    @staticmethod # 객체가 아니라 문자열 처리!!! -> session.py에 @classmethod 처리함
    def from_line(line: str):
        # 저장된 문자열을 1줄씩 객체화(Member) 시킴
        uid, pw, name, role, active = line.strip().split("|")
        # kkw|1111|김기원|admin|True
        return Member(
            uid=uid,
            pw=pw,
            name=name,
            role=role,
            active=(active == "True")
        ) # def __init__(self, uid, pw, name, role="user", active=True)

    # 권한 처리용 메서드
    def is_admin(self):
        return self.role == "admin" # 지금 객체가 admin???

    def is_manager(self):
        return self.role == "manager" # 지금 객체가 manager???