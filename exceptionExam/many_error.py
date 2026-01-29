# 예외가 이것저것 날꺼 같다.????
# try 문 안에서 여러개의 오류를 처리

try :
    4 / 0
    a = [1, 2]
    print(a[3])

# except ZeroDivisionError as e :
    #     print(e)
    # print("0으로 나눠지는 예외가 발생함!!!")

# except IndexError as e :
    #     print(e)
    # print("리스트 인덱스 범위 초과")

except (ZeroDivisionError, IndexError) as e :
    print(e)
    print("0으로 나눴거나 리스트의 범위 초과 예외발생!!")
    print("예외발생시 담당자에게 문의하세요 : 전번~ ")