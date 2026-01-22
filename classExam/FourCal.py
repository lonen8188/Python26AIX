# 클래스용도로 파일을 생성하면 대문자로 시작!!!

class FourCal:
    # pass # 아무동작 안하고 넘어감

    # 변수 선언부 __init__
    def __init__(self):
        self.first = 0
        self.second = 0
        # 이것은 취약한 코드임!!!

    # 메서드 선언부

    # 세터와 게터를 이용해 구현함!
    def setdata(self, first, second):
    # a.first와 a.second를 직접 가서 처리가 가능
    # 하지만 검증해서 같을 처리하는 것도 필요함
    # 데이터를 넣는 메서드를 세터라고 한다.

        if first <= 0 :
            self.first = 0
        else :
            self.first = first

        if second <= 0 :
            self.second = 0
        else:
            self.second = second

    def add(self):
        result = self.first + self.second
        return result

    def div(self):
        result = self.first / self.second
        # 나누는 값이 0이면 컴퓨터는 오류를 발생시킴
        return result

a = FourCal()
# a.first = 100 # 객체 변수에 바로 입력이됨
# a.second = 200
# print(a.self)
a.setdata(-10,10)
result1 = a.add()
print(f"-10+10을 : add()메서드 실행결과 : {result1}")

print(a.first) # 객체 변수에 바로 출력
print(a.second)
# 위 방법은 개발자들이 취약한 코드라고 판단함!!

# a변수에 FourCal()클래스를 연결한다.
print(type(a))
# <class '__main__.FourCal'>
# __main__ -> 모듈의 이름을 담고 있는 파이썬 내장변수
# 최상위 코드가 실행되는 환경의 이름 (주 실행코드임)
# 건물에는 무조건 1층 입구가 있듯이 프로그램 실행은 main으로 판단

class MoreFourCal(FourCal):
    #             부모객체 (+ , - , *, / )
    # 부모객체의 모든 기능을 사용하면서 추가 메서드를 만듬
    def pow(self):
        result = self.first ** self.second
        #           부모에 추가 메서드 (제곱처리)
        return result

    def div(self): # 부모와 같은 메서드 명!!!
        if self.second == 0:
            # 나누는 뒷값이 0이면 나눌필요도 없이 0을 리턴
            return 0
        else:
            return self.first / self.second

c = MoreFourCal()
c.add()  # 부모의 메서드 활용
c.pow()  # 자식의 메서드 활용


# 메서드 오버라이딩 (부모가 만든 메서드를 튜닝할때)
# d = FourCal()
# d.setdata(8,0)
# result = d.div()
# print(result)

e = MoreFourCal()
e.setdata(9,0)
result = e.div() # 부모에서 개선된 자식 div()를 실행함
print(result)

# 클래스 변수(필드) : __init__ 나 일반 메서드에 바깥쪽 변수

class Family :
    lastname = "김"

    # 이곳은 메서드들.....

print(Family.lastname)

a = Family()
b = Family()
a.lastname = "최"
print(a.lastname)
print(b.lastname)

