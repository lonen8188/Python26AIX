#  최상위폴더.현재폴더.모듈(파일명)   클래스
from LMS.service import MemberService, ScoreService, BoardService, ItemService
from LMS.common.Session import Session

def main():
    # 프로그램 시작 시 데이터 로드
    MemberService.load()

    run = True
    while run:
        print("""
==========================
 MBC 아카데미 관리 시스템
==========================
1. 회원가입  2. 로그인 3. 로그아웃
4. 회원관리 (관리자)  
5. 게시판  6. 성적관리 7. 상품몰
9. 종료
""")
        member = Session.login_member
        if member is None :
            print("현재 로그인상태가 아닙니다.")
        else:
            print(f"{member.name}님 환영합니다. ")

        sel = input(">>> ")
        if sel == "1": MemberService.signup()
        elif sel == "2": MemberService.login()
        elif sel == "3": MemberService.logout()
        elif sel == "4": MemberService.admin_menu()
        elif sel == "5": BoardService.run()
        elif sel == "6": ScoreService.run()
        elif sel == "7": ItemService.run()
        elif sel == "9":
            print("프로그램 종료")
            run = False

if __name__ == "__main__": # 프로그램 시작!!!
    main()