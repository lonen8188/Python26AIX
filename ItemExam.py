# ===============================
# 상품 CRUD 프로그램
# ===============================

run = True

# 전역 변수 (상품 DB 역할)
item_names = ["노트북", "모니터"]
unit_prices = [1200000, 400000]
quantity = [40, 25]
product_info = ["AI용 삼성노트북", "LG 24인치 LED"]
category = ["가전", "잡화"]


# -------------------------------
# C : 새 상품 등록
# -------------------------------
def new_item():
    print("\n[ 새 상품 등록 ]")

    name = input("상품명 : ")
    price = int(input("단가 : "))
    qty = int(input("수량 : "))
    info = input("상품 설명 : ")

    item_add_menu()
    cat_num = input("카테고리 선택 : ")

    if cat_num == "1":
        cat = "교재"
    elif cat_num == "2":
        cat = "잡화"
    elif cat_num == "3":
        cat = "음식"
    elif cat_num == "4":
        cat = "패션"
    else:
        print("잘못된 카테고리 선택")
        return

    item_names.append(name)
    unit_prices.append(price)
    quantity.append(qty)
    product_info.append(info)
    category.append(cat)

    print("상품 등록 완료!")


# -------------------------------
# R : 전체 상품 목록
# -------------------------------
def item_list():
    print("\n[ 상품 리스트 ]")
    print("번호 | 상품명 | 가격 | 수량 | 카테고리")
    print("-" * 40)

    for i in range(len(item_names)):
        print(f"{i} | {item_names[i]} | {unit_prices[i]} | {quantity[i]} | {category[i]}")


# -------------------------------
# R : 상품 상세 보기
# -------------------------------
def item_view():
    item_list()
    idx = int(input("\n상세 조회할 상품 번호 : "))

    if 0 <= idx < len(item_names):
        print("\n[ 상품 상세 정보 ]")
        print("상품명 :", item_names[idx])
        print("가격 :", unit_prices[idx])
        print("수량 :", quantity[idx])
        print("카테고리 :", category[idx])
        print("설명 :", product_info[idx])
    else:
        print("존재하지 않는 상품입니다.")


# -------------------------------
# U : 상품 수정
# -------------------------------
def item_update():
    item_list()
    idx = int(input("\n수정할 상품 번호 : "))

    if 0 <= idx < len(item_names):
        print("※ 수정하지 않으려면 Enter")

        name = input(f"상품명({item_names[idx]}) : ")
        price = input(f"가격({unit_prices[idx]}) : ")
        qty = input(f"수량({quantity[idx]}) : ")
        info = input(f"설명({product_info[idx]}) : ")

        if name:
            item_names[idx] = name
        if price:
            unit_prices[idx] = int(price)
        if qty:
            quantity[idx] = int(qty)
        if info:
            product_info[idx] = info

        print("상품 수정 완료!")
    else:
        print("존재하지 않는 상품입니다.")


# -------------------------------
# D : 상품 품절 처리
# -------------------------------
def item_delete():
    item_list()
    idx = int(input("\n품절 처리할 상품 번호 : "))

    if 0 <= idx < len(item_names):
        quantity[idx] = 0
        print(f"[{item_names[idx]}] 상품이 품절 처리되었습니다.")
    else:
        print("존재하지 않는 상품입니다.")


# -------------------------------
# 메뉴 출력
# -------------------------------
def main_menu():
    print("""
=================================
엠비씨 아카데미 쇼핑몰

1. 상품등록
2. 상품리스트
3. 상품자세히보기
4. 상품수정하기
5. 상품품절처리

9. 프로그램 종료
=================================
""")


def item_add_menu():
    print("""
==== 상품 카테고리 ====
1. 교재
2. 잡화
3. 음식
4. 패션
""")


# ===============================
# 프로그램 실행
# ===============================
while run:
    main_menu()
    select = input("메뉴 선택 : ")

    if select == "1":
        new_item()
    elif select == "2":
        item_list()
    elif select == "3":
        item_view()
    elif select == "4":
        item_update()
    elif select == "5":
        item_delete()
    elif select == "9":
        print("프로그램 종료")
        run = False
    else:
        print("잘못된 입력입니다.")
