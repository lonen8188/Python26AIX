class Score:

    def __init__(self, uid, kor, eng, math):
        self.uid = uid
        self.kor = kor
        self.eng = eng
        self.math = math

    @property
    def total(self): # 변수처럼 사용하기 s.total
        return self.kor + self.eng + self.math

    @property
    def avg(self): # 변수처럼 사용하기 s.avg
        return round(self.total / 3, 2)

    # 성적 등급 자동 계산
    @property
    def grade(self): # 변수처럼 사용하기 s.grade
        if self.avg >= 90:
            return "A"
        elif self.avg >= 80:
            return "B"
        elif self.avg >= 70:
            return "C"
        else:
            return "F"

    def to_line(self):
        return f"{self.uid}|{self.kor}|{self.eng}|{self.math}\n"

    @classmethod
    def from_line(cls, line):
        uid, kor, eng, math = line.strip().split("|")
        return cls(uid, int(kor), int(eng), int(math))