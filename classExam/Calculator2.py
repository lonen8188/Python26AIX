# 클래스는 대부분 파일명을 대문자로 만드는 것이 관례이다.
# 클래스는 인스턴스를 목적으로 만듬.

class Calculator: # 파일명과 클래스명도 대문자로 시작!
    # : (콜론)으로 끝나기 때문에 들여쓰기가 중요함

    # 내부에 함수(메서드)를 생성한다.
    def __init__(self):
        # 초기화 메서드
        # 클래스 선언시 기본적으로 실행되는 문법
        self.result = 0  # 클래스가 생성되면서 변수를 만듬

    def add(self, num):
        self.result += num # result = result + num
        return self.result

    def sub(self, num):
        self.result -= num # result = result - num
        return self.result

    def mul(self, num):
        self.result *= num # result = result * num
        return self.result

    def div(self, num):
        self.result /= num # result = result / num
        return self.result
# class 선언 종료

cal1 = Calculator()
# 변수에 객체를 연결
cal2 = Calculator()
# 클래스를 사용하려면 변수에 연결(스택과 힙영역이 연결)
# 이때 사용하는 주소가 self
# 객체(인스턴스) 생성과 변수 연결(self) 끝

# 객체.메서드(값) self로 연결된 주소의 객체를 찾아서
# .add(5) 실행한다. -> 메서드 실행후 결과를 받음
kkwresult = cal1.add(5)
print(kkwresult)

ksbresult = cal2.add(7)
print(ksbresult)

print(cal1.sub(10))
print(cal2.mul(9))
print(cal2.div(9))



