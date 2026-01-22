# 비회원용 게시판을 만들어 보자.

# 프로젝트 목표
# c : 게시글 등록
# r : 게시글 전체 보기(리스트)
# r : 게시글 자세히 보기
# u : 게시글 수정
# d : 게시글 삭제

# 사용할 변수 리스트 (전역 변수 : 프로그램 전반적으로 사용가능)
run = True # while문 프로그램 구동중!!
board_no = [] # 중복되지 않는 유일한 값, not null
board_title = []  # 게시글의 제목
board_content = [] # 게시글의 내용
board_writer = []  # 글쓴이
board_password = [] # 게시글의 암호(수정,삭제)
board_hit = []      # 좋아요 !!!
board_visitcount = [] # 조회수!!!

# 주메뉴
menu = """
===================================
엠비씨 아카데미 비회원 게시판입니다.

1. 게시글 등록
2. 게시글 리스트 보기
3. 게시글 자세히 보기
4. 게시글 수정하기
5. 게시글 삭제하기
6. 게시판 프로그램 종료

"""

# 프로그램 실행문
while run:
    print(menu)
    # select는 while 문 안쪽에서만 활용되는 1회용 변수 : 지역변수
    select = input("1~6까지 입력하세요 : ")
    #        input은 키보드로 입력한 값을 문자열로 전달함
    if select == "1": # 키보드로 입력한 값이 1이면?
        print("게시글을 등록합니다!")
        # 게시글 등록용 코드 추가

        # 게시글의 번호는 프로세스가 자동처리
        # 키보드로 게시글을 받아 변수에 넣음
        title = input("제목 : ")
        content = input("내용 : ")
        writer = input("작성자 : ")
        password = input("암호 : ")

        # 넣은 정보를 확인한다.
        print(f"제목 : {title}, 내용 : {content}")
        print(f"작성자 : {writer}, 암호 : {password}")
        choose = input("저장하려면 y를 누르세요 : ")
        if choose == "y":
            board_title.append(title)
            board_content.append(content)
            board_writer.append(writer)
            board_password.append(password)

            # 제목의 리스트에서 인덱스를 추출하여 + 1한 값이 no
            # if title in board_title :
            #     idx = board_title.index(title)
            #     board_no.append(idx+1)

            # 제목을 이용해서 번호를 생성하면 중복제목 문제발생
            # board_no 리스트의 길이를 활용하여 해결
            no = len(board_no) + 1

            board_no.append(no)
            board_hit.append(0) # 좋아요
            board_visitcount.append(0) # 조회수

            print(f"{no}번의 게시글이 등록 되었습니다." )


    elif select == "2":
        print("[게시글 전체 목록 출력]")
        # 게시글 리스트 보기용 코드 추가

        print("------------------------------------------")
        print("번호\t 제목\t 작성자\t 조회수\t ")
        print("------------------------------------------")

        if len(board_no) == 0:
            print("등록된 게시물이 없습니다.")
            continue    # while문으로 돌아간다.

        for i in range(len(board_no)): # 게시글의 개수만큼 반복 ( 0~게시물수까지 인덱스 처리용)
            print(f"{board_no[i]}\t {board_title[i]}\t {board_writer[i]}\t {board_visitcount[i]}")
            #         번호               제목               작성자                조회수



    elif select == "3":
        print("[게시글 자세히 보기]")
        # 게시글 자세히 보기 코드 추가
        bno = int(input("게시글 번호 : "))

        if bno in board_no: # 등록된 게시물의 유무 확인
            print("게시물을 찾았습니다.")
            idx = board_no.index(bno) # 리스트에서 게시물의 인덱스 값을 찾아옴

            board_visitcount[idx] += 1 # 조회수 1 증가

            print("-----------------------------")
            print(f"번호 : {board_no[idx]}")
            print(f"제목 : {board_title[idx]}")
            print(f"내용 : {board_content[idx]}")
            print(f"작성자 : {board_writer[idx]}")
            print(f"조회수 : {board_visitcount[idx]}")
            print(f"좋아요 : {board_hit[idx]}")
            print("===================================")

            if input("좋아요 누르기(y) : ") == "y":
                board_hit[idx] += 1
                print("좋아요 +1")
            else :
                print("아쉽습니다. 다음에 더 좋은 게시글이 될겁니다.")

        else:
            print("해당번호에 게시글이 없습니다.")


    elif select == "4":
        print("[게시글 수정]")
        # 게시글 수정 코드 추가
        no = int(input("게시글 번호 : "))
        pw = input("암호 : ")

        if no in board_no:
            idx = board_no.index(no)

            if board_password[idx] == pw:
                board_title[idx] = input("새 제목 : ")
                board_content[idx] = input("새 내용 : ")
                print("게시글이 수정되었습니다.")
            else:
                print("암호가 틀렸습니다.")
        else:
            print("게시글 번호가 없습니다.")

    elif select == "5":
        print("[게시글 삭제]")
        # 게시글 삭제 코드 추가

        no = int(input("게시글 번호 : "))
        pw = input("암호 : ")

        if no in board_no:
            idx = board_no.index(no)

            if board_password[idx] == pw:
                board_no.pop(idx)
                board_title.pop(idx)
                board_content.pop(idx)
                board_writer.pop(idx)
                board_password.pop(idx)
                board_hit.pop(idx)
                board_visitcount.pop(idx)

                print("게시글이 삭제되었습니다.")
            else:
                print("암호가 틀렸습니다.")
        else:
            print("게시글 번호가 없습니다.")

    elif select == "6":
        print("[비회원게시판 프로그램을 종료합니다.")
        run = False

    else :
        # 1~6까지 잘못 입력된 값 처리용
        print("잘못 입력하셨습니다. ")
