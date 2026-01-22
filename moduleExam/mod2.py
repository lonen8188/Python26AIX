# 이번에는 클래스와 변수등을 포함하는 import

PI = 3.1415926 # 대문자로 변수를 만들면 상수(변하지 않는값)

class Math :  # Math 클래스
    def solv(self, r): # r 지름
        return PI * (r ** 2) # 원의 넓이를 구하는 공식
    # 원의 넓이 구하는 메서드 종료

def add(a, b): # 함수
    return a + b