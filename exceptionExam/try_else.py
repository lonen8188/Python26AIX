# try-else : try문 수행 중
# 오류가 발생하면 except절을 처리하고
# 오류가 발생하지 않으면 else 절이 수행

try :
    age = int(input("나이를 입력하세요!!!"))

except : # except에 클래스를 넣지 않으면 모든 예외!!!
    print("숫자만 입력하세요!!!")

else : # 예외발생하지 않으면 처리되는 문장
    if age <= 18 :
        print("귀하는 미성년자 입니다.")
    else:
        print("환영합니다.")