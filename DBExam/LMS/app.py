# pip install flask
from flask import Flask, render_template, request, redirect, url_for, session
from LMS.common.session import Session
from LMS.domain.Board import Board
from LMS.domain.Score import Score

app = Flask(__name__)

import os

UPLOAD_FOLDER = 'uploads/'
# 폴더가 없으면 자동 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 최대 업로드 용량 제한 (예: 16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 1. 게시판 목록 조회
@app.route('/board')
def board_list():
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 작성자 이름을 함께 가져오기 위해 JOIN 사용
            sql = """
                SELECT b.*, m.name as writer_name 
                FROM boards b 
                JOIN members m ON b.member_id = m.id 
                ORDER BY b.id DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            boards = [Board.from_db(row) for row in rows]
            return render_template('board_list.html', boards=boards)
    finally:
        conn.close()

# 2. 게시글 상세 보기
@app.route('/board/view/<int:board_id>')
def board_view(board_id):
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # JOIN을 통해 작성자 정보(name, uid)를 함께 조회
            sql = """
                SELECT b.*, m.name as writer_name, m.uid as writer_uid
                FROM boards b
                JOIN members m ON b.member_id = m.id
                WHERE b.id = %s
            """
            cursor.execute(sql, (board_id,))
            row = cursor.fetchone()

            if not row:
                return "<script>alert('존재하지 않는 게시글입니다.'); history.back();</script>"

            # Board 객체로 변환 (앞서 작성한 Board.py의 from_db 활용)
            board = Board.from_db(row)

            return render_template('board_view.html', board=board)
    finally:
        conn.close()

@app.route('/board/write', methods=['GET', 'POST'])
def board_write():
    # 1. 사용자가 '글쓰기' 버튼을 눌러서 들어왔을 때 (화면 보여주기)
    if request.method == 'GET':
        # 로그인 체크 (로그인 안 했으면 글 못 쓰게)
        if 'user_id' not in session:
            return '<script>alert("로그인 후 이용 가능합니다."); location.href="/login";</script>'
        return render_template('board_write.html')

    # 2. 사용자가 '등록하기' 버튼을 눌러서 데이터를 보냈을 때 (DB 저장)
    elif request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        # 세션에 저장된 로그인 유저의 id (member_id)
        member_id = session.get('user_id')

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 기억하신 테이블 구조(member_id, title, content)에 맞게 INSERT
                sql = "INSERT INTO boards (member_id, title, content) VALUES (%s, %s, %s)"
                cursor.execute(sql, (member_id, title, content))
                conn.commit()
            return redirect(url_for('board_list')) # 저장 후 목록으로 이동
        except Exception as e:
            print(f"글쓰기 에러: {e}")
            return "저장 중 에러가 발생했습니다."
        finally:
            conn.close()


@app.route('/board/edit/<int:board_id>', methods=['GET', 'POST'])
def board_edit(board_id):
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 화면 보여주기 (기존 데이터 로드)
            if request.method == 'GET':
                sql = "SELECT * FROM boards WHERE id = %s"
                cursor.execute(sql, (board_id,))
                row = cursor.fetchone()

                if not row:
                    return "<script>alert('존재하지 않는 게시글입니다.'); history.back();</script>"

                # 본인 확인 로직 (필요시 추가)
                if row['member_id'] != session.get('user_id'):
                    return "<script>alert('수정 권한이 없습니다.'); history.back();</script>"

                board = Board.from_db(row)
                return render_template('board_edit.html', board=board)

            # 2. 실제 DB 업데이트 처리
            elif request.method == 'POST':
                title = request.form.get('title')
                content = request.form.get('content')

                sql = "UPDATE boards SET title=%s, content=%s WHERE id=%s"
                cursor.execute(sql, (title, content, board_id))
                conn.commit()

                return redirect(url_for('board_view', board_id=board_id))
    finally:
        conn.close()


@app.route('/board/delete/<int:board_id>')
def board_delete(board_id):
    # 로그인 여부 확인 (필요시)
    # if 'user_id' not in session:
    #     return '<script>alert("로그인 후 이용 가능합니다."); location.href="/login";</script>'

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 본인 확인 로직을 추가하고 싶다면 WHERE member_id = %s 를 추가하세요.
            sql = "DELETE FROM boards WHERE id = %s"  # 저장된 테이블명 boards 사용
            cursor.execute(sql, (board_id,))
            conn.commit()

            if cursor.rowcount > 0:
                print(f"게시글 {board_id}번 삭제 성공")
            else:
                return "<script>alert('삭제할 게시글이 없거나 권한이 없습니다.'); history.back();</script>"

        return redirect(url_for('board_list'))
    except Exception as e:
        print(f"삭제 에러: {e}")
        return "삭제 중 오류가 발생했습니다."
    finally:
        conn.close()


# 세션을 사용하기 위해 보안키 설정 (아무 문자열이나 입력)
app.secret_key = 'your_secret_key_here'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    uid = request.form.get('uid')
    upw = request.form.get('upw')

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 회원 정보 조회
            sql = "SELECT id, name, uid, role  FROM members WHERE uid = %s AND password = %s"
            cursor.execute(sql, (uid, upw))
            user = cursor.fetchone()

            if user:
                # 2. 로그인 성공: 세션에 사용자 정보 저장
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_uid'] = user['uid']

                # 이제 DB에서 'role'을 가져왔으니 에러 없이 잘 들어갈 겁니다.
                session['user_role'] = user['role']

                return redirect(url_for('index'))
            else:
                return "<script>alert('아이디 또는 비밀번호가 틀렸습니다.'); history.back();</script>"
    finally:
        conn.close()


@app.route('/logout')
def logout():
    session.clear()  # 세션 비우기
    return redirect(url_for('login'))


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')

    uid = request.form.get('uid')
    password = request.form.get('password')  # 컬럼명 password에 맞춤
    name = request.form.get('name')

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 아이디 중복 확인
            cursor.execute("SELECT id FROM members WHERE uid = %s", (uid,))
            if cursor.fetchone():
                return "<script>alert('이미 존재하는 아이디입니다.'); history.back();</script>"

            # 회원 정보 저장 (role, active는 기본값이 들어감)
            sql = "INSERT INTO members (uid, password, name) VALUES (%s, %s, %s)"
            cursor.execute(sql, (uid, password, name))
            conn.commit()

            return "<script>alert('회원가입이 완료되었습니다!'); location.href='/login';</script>"
    except Exception as e:
        print(f"회원가입 에러: {e}")
        return "가입 중 오류가 발생했습니다."
    finally:
        conn.close()


@app.route('/member/edit', methods=['GET', 'POST'])
def member_edit():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'GET':
                # 기존 정보 불러오기
                cursor.execute("SELECT * FROM members WHERE id = %s", (session['user_id'],))
                user_info = cursor.fetchone()
                return render_template('member_edit.html', user=user_info)

            # POST 요청: 정보 업데이트
            new_name = request.form.get('name')
            new_pw = request.form.get('password')

            if new_pw:  # 비밀번호 입력 시에만 변경
                sql = "UPDATE members SET name = %s, password = %s WHERE id = %s"
                cursor.execute(sql, (new_name, new_pw, session['user_id']))
            else:  # 이름만 변경
                sql = "UPDATE members SET name = %s WHERE id = %s"
                cursor.execute(sql, (new_name, session['user_id']))

            conn.commit()
            session['user_name'] = new_name  # 세션 이름 정보도 갱신
            return "<script>alert('정보가 수정되었습니다.'); location.href='/mypage';</script>"
    finally:
        conn.close()


# @app.route('/score/members')
# def score_member_list():
#     # 관리자나 매니저만 접근 가능
#     if session.get('user_role') not in ('admin', 'manager'):
#         return "<script>alert('권한이 없습니다.'); history.back();</script>"
#
#     conn = Session.get_connection()
#     try:
#         with conn.cursor() as cursor:
#             # 일반 유저(student)들만 조회
#             sql = "SELECT id, uid, name FROM members WHERE role = 'user' AND active = 1"
#             cursor.execute(sql)
#             students = cursor.fetchall()
#             return render_template('score_member_list.html', students=students)
#     finally:
#         conn.close()

@app.route('/score/members')
def score_members():
    if session.get('user_role') not in ('admin', 'manager'):
        return "<script>alert('권한이 없습니다.'); history.back();</script>"

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # LEFT JOIN을 통해 성적이 있으면 s.id가 숫자로, 없으면 NULL로 나옵니다.
            sql = """
                SELECT m.id, m.uid, m.name, s.id AS score_id 
                FROM members m
                LEFT JOIN scores s ON m.id = s.member_id
                WHERE m.role = 'user'
                ORDER BY m.name ASC
            """
            cursor.execute(sql)
            members = cursor.fetchall()
            return render_template('score_member_list.html', members=members)
    finally:
        conn.close()

# @app.route('/score/add')
# def score_add():
#     # 관리자/매니저 권한 체크
#     if session.get('user_role') not in ('admin', 'manager'):
#         return "<script>alert('권한이 없습니다.'); history.back();</script>"
#
#     # URL 파라미터(?uid=abc&name=홍길동) 받기
#     target_uid = request.args.get('uid')
#     target_name = request.args.get('name')
#
#     return render_template('score_form.html', target_uid=target_uid, target_name=target_name)


@app.route('/score/add')
def score_add():
    if session.get('user_role') not in ('admin', 'manager'):
        return "<script>alert('권한이 없습니다.'); history.back();</script>"

    target_uid = request.args.get('uid')
    target_name = request.args.get('name')

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 대상 학생의 id 찾기
            cursor.execute("SELECT id FROM members WHERE uid = %s", (target_uid,))
            student = cursor.fetchone()

            # 2. 기존 성적이 있는지 조회
            existing_score = None
            if student:
                cursor.execute("SELECT * FROM scores WHERE member_id = %s", (student['id'],))
                row = cursor.fetchone()
                if row:
                    # 기존에 만든 Score.from_db 활용
                    existing_score = Score.from_db(row)

            return render_template('score_form.html',
                                   target_uid=target_uid,
                                   target_name=target_name,
                                   score=existing_score)  # score 객체 전달
    finally:
        conn.close()

@app.route('/score/save', methods=['POST'])
def score_save():
    if session.get('user_role') not in ('admin', 'manager'):
        return "권한 오류", 403

    # 폼 데이터 수집
    target_uid = request.form.get('target_uid')
    kor = int(request.form.get('korean', 0))
    eng = int(request.form.get('english', 0))
    math = int(request.form.get('math', 0))

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 대상 학생의 id(PK) 가져오기
            cursor.execute("SELECT id FROM members WHERE uid = %s", (target_uid,))
            student = cursor.fetchone()
            if not student:
                return "<script>alert('존재하지 않는 학생입니다.'); history.back();</script>"

            # 2. Score 객체 생성 (계산 프로퍼티 활용)
            temp_score = Score(member_id=student['id'], kor=kor, eng=eng, math=math)

            # 3. 기존 데이터가 있는지 확인 (ScoreService 로직 이식)
            cursor.execute("SELECT id FROM scores WHERE member_id = %s", (student['id'],))
            is_exist = cursor.fetchone()

            if is_exist:
                # UPDATE 실행
                sql = """
                    UPDATE scores SET korean=%s, english=%s, math=%s, 
                                      total=%s, average=%s, grade=%s
                    WHERE member_id = %s
                """
                cursor.execute(sql, (temp_score.kor, temp_score.eng, temp_score.math,
                                     temp_score.total, temp_score.avg, temp_score.grade,
                                     student['id']))
            else:
                # INSERT 실행
                sql = """
                    INSERT INTO scores (member_id, korean, english, math, total, average, grade)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (student['id'], temp_score.kor, temp_score.eng, temp_score.math,
                                     temp_score.total, temp_score.avg, temp_score.grade))

            conn.commit()
            return f"<script>alert('{target_uid} 학생 성적 저장 완료!'); location.href='/score/list';</script>"
    finally:
        conn.close()


@app.route('/score/list')
def score_list():
    # 1. 권한 체크 (관리자나 매니저만 볼 수 있게 설정)
    if session.get('user_role') not in ('admin', 'manager'):
        return "<script>alert('권한이 없습니다.'); history.back();</script>"

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 2. JOIN을 사용하여 학생 이름(name)과 성적 데이터를 함께 조회
            # 성적이 없는 학생은 제외하고, 성적이 있는 학생들만 총점 순으로 정렬
            sql = """
                SELECT m.name, m.uid, s.* FROM scores s
                JOIN members m ON s.member_id = m.id
                ORDER BY s.total DESC
            """
            cursor.execute(sql)
            datas = cursor.fetchall()

            # 3. DB에서 가져온 딕셔너리 리스트를 Score 객체 리스트로 변환
            score_objects = []
            for data in datas:
                # Score 클래스에 정의하신 from_db 활용
                s = Score.from_db(data)
                # 객체에 없는 이름(name) 정보는 수동으로 살짝 넣어주기
                s.name = data['name']
                s.uid = data['uid']
                score_objects.append(s)

            return render_template('score_list.html', scores=score_objects)
    finally:
        conn.close()

@app.route('/score/my')
def score_my():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 내 ID로만 조회
            sql = "SELECT * FROM scores WHERE member_id = %s"
            cursor.execute(sql, (session['user_id'],))
            row = cursor.fetchone()

            # Score 객체로 변환 (from_db 활용)
            score = Score.from_db(row) if row else None

            return render_template('score_my.html', score=score)
    finally:
        conn.close()


@app.route('/mypage')
def mypage():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 내 상세 정보 조회
            cursor.execute("SELECT * FROM members WHERE id = %s", (session['user_id'],))
            user_info = cursor.fetchone()

            # 2. 내가 쓴 게시글 개수 조회 (작성하신 boards 테이블 활용)
            cursor.execute("SELECT COUNT(*) as board_count FROM boards WHERE member_id = %s", (session['user_id'],))
            board_count = cursor.fetchone()['board_count']

            return render_template('mypage.html', user=user_info, board_count=board_count)
    finally:
        conn.close()


@app.route('/board/my')
def board_my_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 내가 작성한 글만 최신순으로 조회
            sql = "SELECT * FROM boards WHERE member_id = %s ORDER BY created_at DESC"
            cursor.execute(sql, (session['user_id'],))
            my_posts = cursor.fetchall()

            return render_template('board_my_list.html', posts=my_posts)
    finally:
        conn.close()

@app.route('/')
def index():
    return render_template('main.html')

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)