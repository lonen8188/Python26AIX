# Member.py는 각 회원에 자료를 담당한다.
# 웹프로그래밍에 백엔드에는 데이터베이스와 결합하는데
# MemberDTO, MemberVO라는 이름으로 사용된다.
# DTO(Data Transfer Object, 데이터 전송 객체)
# VO(Value Object, 값 그 자체)

# 회원 각각의 자료를 리스트가 아닌 변수에 담에 제공하려 함

class Member: # 클래스는 무조건! 대문자로 시작하세요!!!
    def __init__(self, uid, pw, name, role="user", active=True):
        self.id = uid           # id
        self.pw = pw            # password
        self.name = name        # 이름
        self.role = role        # 권한
        self.active = active    #활성화 유무

    # 사용법 member = Member()  -> 객체를 생성하여 변수에 연결
    # 이름 : member.id
    # 암호 : member.pw

    # 파일 저장용 문자열 변환
    def to_line(self):
        return f"{self.id}|{self.pw}|{self.name}|{self.role}|{self.active}\n"

    # 사용법 member = Member()
    # member.to_line() -> kkw|1234|김기원|admin|True엔터
    # 메모장에 객체 기록용!

    # 파일에서 불러온 내용 객체처리
    @classmethod # 객체(self)가 아니라 클래스 자체를(cls)를 다루는 메서드 정의
    def from_line(cls, line): # line : 메모장의 1줄 문자열
        uid, pw, name, role, active = line.strip().split("|")
        #           변수들에 넣음  <-  1줄 문자열에 엔터를 지우고 |로 잘라서

        return cls(uid, pw, name, role, active == "True")

    # 사용법 : m = Member(uid, pw, name, role, active) -> 권장하지 않음(바로 넣음)
    #         self를 사용하는 방법(객체 변수)

    # 권장법 : m = Member.from_line(line) -> 객체생성 책임을 클래스가 담당
    #         cls를 사용하는 방법 (클래스변수)

    # 면접시 물어보는 내용!!!
    # 직렬화, 역직렬화
    # 직렬화(Serialization) : 객체 -> 저장 가능한 형태
    #       member.to_line()

    # 역직렬화(Deserialization) : 저장된데이터 -> 객체 (@classmethod)
    #      Member.from_line(line)
