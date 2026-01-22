# 클래스는 주로 같은 내용에 변수 및 메서드를 모아서 처리하는 용도
# 인스턴스 : 객체를 복제해서 같은 변수나 메서드를 찍어내는 효과
# LMS 프로그램을 지금 처럼 콘솔에 출력하면 1인용인데
# 클래스로 구현하면 여려명이 접근해서 사용할 수 도 있다. -> FLASK, fastAPI(웹서버)

# 변수 선언시 글로벌 영역에 선언하면 : session -> 값를 공유
# 클래스가 아닌 일반 사항으로 처리하면 1명이 로그인하면
# 다른사람이 접속할 때 이미 로그인한 상태가 됨

result = 0    # result는 결과값이라는 영문
result2 = 0

def add(num) :  # 함수 만듬 -> num을 받음
    global result   # 전역변수를 가져와 0값을 가지고 있음
    result += num   # result = rusult + num
    return result   # 결과를 내보냄
# add()함수 만듬 끝

def add2(num) :
    global result2
    result2 += num
    return result2

print(add(5))
print(add2(9))
print(add(2))
print(add2(4))
# 글로벌 영역에 있는 result, result2를 공유함!!
# 단점은 혼자 프로그램을 사용하지 않으면???
# 여러명이 add()함수를 사용하려면 여려명만큼 함수와 변수를 생성