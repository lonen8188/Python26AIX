# 회원관리 curd를 사용자 지정 함수로 만들어 보자.
# c : 회원가입
# r : 회원리스트 관리자인경우 회원암호 변경, 블랙리스트로생성, 권한 부여
# r : 로그인 id와 pw를 활용하여 로그인 상태 유지 session
# u : 회원정보 수정
# d : 회원탈퇴, 회원비활성화

# 프로그램에서 사용될 변수들
# 전역변수(global) -> py 파일 안에서 전체적으로 사용되는 변수
# 지역변수(local) -> while, if, for, def안에서 사용되는 변수
run = True # while 에서 전체적으로 사용되는 변수(프로그램 구동)
session = None # 로그인상태 저장용 -> 로그인한 사용자의 리스트 인덱스 기억용

# 프로그램에서 사용될 리스트 들 (더미 데이터)
# sns = [1, 2, 3] # 회원번호 들 회원삭제및 추가시 번호가 흔들릴 수 있음(인덱스만!)
ids = ["kkw", "lhj", "ljj"] # 로그인 아이디 들
pws = ["1234", "5678", "8888"] # 암호 들
names = ["김기원","임효정","이재정"]  # 사용자 명
roles = ["admin","manager","user"]  # 사용자 권한 (admin, manager, user)
active = [True,True,True] # 회원사용중, 탈퇴, 중지, 블랙리스트 등...
# 차후에는 파일처리로 변환 할 예정

# 프로그램에서 사용될 함수들
def member_add():
    # 회원가입용 함수
    print("member_add 함수로 진입합니다.")
    # 회원가입에 필요한 기능을 넣음
    new_id = input("아이디 : ") # 키보드로 아이디를 넣음

    # 이미 아이디가 존재하면 다른 아이디로 넣게 유도
    if new_id in ids: # ids ids리스트에서 찾아 있는지 확인
        # True 일때
        print("이미 존재하는 아이디 입니다. ")
        return # if문 종료

    else : # False ids에 입력된 id가 없을 때 (중복없다)
        new_pw = input("비밀번호 : ")
        new_name = input("이름 : ")
        member_add_menu() # 회원권한 메뉴 출력

        role_set = input("권한 선택 : ")
        if role_set == "1" :
            new_role = "admin"
        elif role_set == "2" :
            new_role = "manager"
        else :
            new_role = "user"

        print(f"""
입력된 정보를 확인하세요!!!
이름 : {new_name}  암호 : {new_pw}
아이디 : {new_id}  권한 : {new_role}""")

        # print("저장하려면 y : ")
        save_select = input("저장하려면 y : ")
        if save_select == "y" :
            print("저장을 시작합니다.")
            ids.append(new_id)  # .append()리스트 뒤에 추가
            pws.append(new_pw)
            names.append(new_name)
            roles.append(new_role)
            active.append(True)  # 저장 완료
            print("저장 완료됨!!!")

            # 차후에 로그인 함수를 추가 해봄
        else :
            print("회원가입이 되지 않았습니다.")

    print("member_add 함수를 종료합니다.")
# 회원가입용 함수 종료

def member_login() :
    # 가입된 회원을 확인하여 로그인 처리 후 session 변수에 인덱스를 넣음
    print("member_login 함수로 진입합니다.")
    # 로그인에 필요한 기능을 넣음

    global session  # 맨 위에 전역변수로 지정한 내용 활용

    if session is not None : # session에 이미 값이 있으면??
    # is not None 싱글톤이라는 객체가 있는지 비교하는 용
    # if session != None -> 숫자 비교형 이퀄이나는 값으로 사용

        # True
        print("이미 로그인 한 상태입니다.")
        print(f"로그인한 사용자는 {names[session]} 님 입니다.")
        return # 되돌아 간다.
    else :
        # False
        user_id = input("로그인 ID : " )
        user_pw = input("비밀번호 : ")

        if user_id in ids : # 키보드로 받은 id를 ids 리스트에 있는지??
            # True 있으면
            idx = ids.index(user_id) # id에 해당하는 주소를 idx에 넣음

            if not active[idx] : # 회원 활성화 상태인지?
                # False
                print("비활성화/차단된 계정입니다.")
                return
            else:
                # True
                # 암호를 비교한다.
                if user_pw == pws[idx] : # 키보드로 넣은 암호와 리스트의 주소 암호 일치
                    # id도 같고 활성화 상태이고 암호가 같다~!
                    session = idx # 로그인 상태로 완성!!!
                    # 글로벌 영역에 세션값(로그인 사용자의 주소)이 있는 상태가 됨

                    print(f"{names[session]}님 환영합니다.")
                    print(f"{roles[idx]}권한을 가지고 있습니다.")
                else :
                    print("비밀번호가 다릅니다.")

        else :
            # False 없으면
            print("존재하지 않는 아이디!!!!")




    print("member_login 함수를 종료합니다.")
# 회원로그인용 함수 종료

def member_admin() :
    # 관리자가 로그인 했을 경우 할수 있는 기능을 작성
    print("member_admin 함수로 진입합니다.")
    # 다른 사용자 암호 변경 코드

    # 블랙리스트로 변환 -> active를 False

    # 권한 부여 -> 사용자의 권한roles를 변경 (manage <-> user)

    print("member_admin 함수로 종료합니다.")
# 관리자가 사용자 변경사항 함수 종료

def member_logout() :
    # 회원 로그아웃으로 상태 변경 -> session 값을 None으로 변경
    print("member_logout 함수로 진입합니다.")
    # 로그인 상태인지를 확인하고 session을 None으로 변경

    print("member_logout 함수를 종료합니다.")
# 로그아웃 함수를 종료

def member_modify():
    # 회원 정보 수정
    print("member_modify 함수로 진입합니다.")
    # 로그인 상태인지를 확인하고 자산의 정보를 확인하고 수정한다.

    print("member_modify 함수를 종료합니다.")
# 회원정보 수정 종료

def member_delete():
    # 회원 탈퇴 또는 회원 유휴등 처리
    print("member_delete 함수로 진입합니다.")
    # 로그인 상태인지를 확인하고 탈퇴는 pop, 유휴(active=False)

    print("member_delete 함수를 종료합니다.")
# 회원탈퇴 종료

# --------------------- 기능에 대한 함수 생성 끝----------------

def main_menu() :
    print(f"""
    ==== 엠비씨아카데미 회원관리 프로그램입니다======
    1. 회원가입    2. 로그인     3. 로그아웃
    4. 회원정보수정      5. 회원탈퇴
    9. 프로그램 종료
    """)
# 메인메뉴용 함수 종료

def member_add_menu() : # 회원가입에서 사용할 메뉴
    print(f"""
    ----- 회원권한을 확인하세요.---------
    1. 관리자    2. 팀장    3. 일반사용자 
    """)

# ------------------ 메뉴 함수 끝 ------------------

# 프로그램 시작!!!!
while run : # 메인 프로그램 실행 코드
    main_menu() # 위에서 만든 메인 메뉴함수를 실행
    select = input(">>>") # 키보드로 메뉴 선택
    if select == "1" : # 회원가입 코드
        member_add()   # 회원가입용 함수 호출

    elif select == "2" : # 로그인 메뉴 선택
        member_login() # 로그인용 함수 호출

    elif select == "3" : # 로그아웃 메뉴 선택
        member_logout() # 로그아웃 함수 호출

    elif select == "4" : # 회원정보 수정 선택
        member_modify()  # 회원정보 수정 함수 호출

    elif select == "5" : # 회원탈퇴 선택
        member_delete()     # 회원정보 삭제 함수 호출

    elif select == "9" : # 프로그램 종료 선택
         run = False

    else:
        print("잘못 입력하셨습니다.")
# while문 종료