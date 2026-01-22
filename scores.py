# 성적 처리용 프로그램을 개발해보자!!!!

# CREATE : 성적입력
# READ : 성적보기
# UPDATE : 성적수정
# DELETE : 성적삭제

# 필요한 변수는??
sns = [] # 학번
names = [] # 이름
kors = [] # 국어점수
engs = [] # 영어점수
mats = []  # 수학점수
tots = [] # 총점 빈 배열
avgs = [] # 평균 빈 배열
grades = [] # 학점 빈 배열

menu = """
======================
엠비씨아카데미성적처리

1. 성적입력
2. 성적보기
3. 성적수정
4. 성적삭제
5. 프로그램종료


"""

run = True # 프로그램 실행중!!!

while run: # run변수가 False 처리 될때까지 반복
    # : 아래는 들여쓰기 4칸 정도 처리
    # 들여쓰기를 진행하면 하위 실행문 이다!!!
    print(menu) # 콘솔창에 메뉴를 출력
    select = input("(1~5)값 입력 : ") # select 변수에 숫자를 넣는다.
    #               키보드로 입력받는 곳 앞쪽에 출력 메시지

    if select == "1":  # 키보드로 입력한 숫자가 1이면?
        print("학생 성적을 입력합니다.") # 1일때 처리되는 부분

        sn = input("학번을 입력하세요 : ")
        name = input("이름을 입력하세요 : ")
        kor = int(input("국어점수 : "))
        eng = int(input("영어점수 : "))
        mat = int(input("수학점수 : "))  # 키보드를 이용한 점수 입력
        #     키보드로 입력한 숫자는 문자로 인식됨으로 int()로 감싸 계산용으로 변경


        print("입력한 정보를 확인합니다.")
        # print(" 학번 : " + sn)
        # print(" 이름 : " + name)
        # print(" 국어 : " + kor)
        # print(" 영어 : " + eng)
        # print(" 수학 : " + mat) # 키보드로 입력한 점수 확인용
        # print에서 문자와 숫자가 같이 출력되려면 str()으로 숫자를 문자로 변경 해야 한다.
        # 그러나 f 포멧팅은 {} 안에 변수가 숫자든 문자든 상관없이 출력 해준다.
        print(f"학번 : {sn}, 이름 : {name}, 국어 : {kor}, 영어 : {eng} , 수학 : {mat} " )

        if input("저장하려면 y : ") == "y" : # 저장시 y 입력
            sns.append(sn)
            names.append(name)
            kors.append(kor)
            engs.append(eng)
            mats.append(mat) # 변수뒤에 s는 배열(리스트)라고 생각
                             # 변수.append() 리스트 뒤에 값이 추가됨
            tot = kor + eng + mat
            tots.append(tot) # 입력후 저장시 총점 계산하여 넣음
            avgs.append(tot / 3)   # 입력후 저장시 평균 계산하여 넣음
            # 미션 평균이 : 90이상이면 A ,  80이상이면 B , 70이상이면 C , 나머지 F


            print("저장완료!!!")

        else:
            print("저장되지 않았습니다.")
            print("처음부터 다시 입력하세요!!")



    elif select == "2": # 키보드로 입력한 숫자가 2이면?
        print("학생들의 성적을 출력합니다.") # 2일때 처리되는 부분
        print("====================================")
        print("[성적목록]")

        for i in range(len(sns)): # 리스트의 처음부터 끝까지 반복용
            #          len(sns) -> sns 리스트의 길이를 가져옴 -> 5(기본값)
            #    range(5) -> 0 ~ 5까지 증가
            # i in 5 -> i값에 0 반복 1 반복 2 반복 3 반복 4 반복 5 끝!
            # 결론 : i 값이 인덱스로 사용함

            # tots[i] = kors[i] + engs[i] + mats[i]
            # avgs[i] = tots[i] / 3
            # 오류발생으로 주석처리 -> 이유는 ? index out of range
            # 비어 있는 리스트는 주소가 없다.!!!!
            # 해결방법 : .append()를 사용한다.
            tots.append(kors[i] + engs[i] + mats[i])
            avgs.append(tots[i] / 3)

            # grades는 미션!!!
            print("------------------------------------------------------------")
            print("학번 : " + sns[i] + " 이름 : " + names[i])
            print("국어 : " + str(kors[i]) + " 영어 : " + str(engs[i]) + " 수학 : " + str(mats[i]))
            print("총점 : " + str(tots[i]) + " 평균 : " + str(avgs[i]))
            print("------------------------------------------------------------")



    elif select == "3": # 키보드로 입력한 숫자가 3이면?
        print("학생 성적을 수정합니다.")  # 3일때 처리되는 부분
        # 등록된 학생의 점수를 가져온다.
        # 학번을 이용하여 학생을 찾는다.
        sn = input("수정할 학번 : ")

        if sn in sns : # sns 학번이 들어있는 리스트 in 안에 있는지 확인
            print("학번이 있습니다.")
            idx = sns.index(sn) # 찾은 학번의 주소를 가져옴
            print(f"이름 : {names[idx]} , 국어 : {kors[idx]}, 영어 : {engs[idx]}, 수학 : {mats[idx]}")

            # 등록된 학생의 점수를 수정한다.
            kors[idx] = int(input(" 수정할 국어 점수 : "))
            engs[idx] = int(input(" 수정할 영어 점수 : "))
            mats[idx] = int(input(" 수정할 수학 점수 : "))

            # 미션 수정된 값을 기준으로 총점과  평균과 등급을 다시 등록한다.

        else :
            print("학번이 없습니다. ")
            print("처음으로 돌아 갑니다.")



    elif select == "4": # 키보드로 입력한 숫자가 4이면?
        print("학생 성적을 삭제합니다.")
        sn = input("삭제할 학번 : ")

        if sn in sns:
            idx = sns.index(sn)
            print(f"{names[idx]} 학생의 정보를 삭제합니다.")

            if input("정말 삭제할까요? (y) : ") == "y":
                sns.pop(idx)
                names.pop(idx)
                kors.pop(idx)
                engs.pop(idx)
                mats.pop(idx)
                tots.pop(idx)
                avgs.pop(idx)
                print("삭제 완료!")
        else:
            print("해당 학번이 없습니다.")

    elif select == "5": # 키보드로 입력한 숫자가 5이면?
        print("프로그램을 종료합니다.")
        run = False # while문을 종료하여 프로그램이 꺼진다.

    else: # 1~5까지 값 이외의 문자가 들어오면 처리용
        print("1~5값만 허용합니다.")

