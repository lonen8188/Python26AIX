import os
import uuid
from LMS.common.session import Session
from datetime import datetime


class PostService:

    # 파일게시물 저장
    @staticmethod
    def save_post(member_id, title, content, file=None, upload_folder='uploads/'):
        """게시글과 첨부파일을 동시에 저장 (트랜잭션 처리)"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 게시글(posts) 먼저 저장
                sql_post = "INSERT INTO posts (member_id, title, content) VALUES (%s, %s, %s)"
                cursor.execute(sql_post, (member_id, title, content))

                # 방금 인서트된 게시글의 ID(PK) 가져오기
                post_id = cursor.lastrowid

                # 2. 파일이 있다면 처리
                if file and file.filename != '':
                    origin_name = file.filename
                    # 확장자 추출 및 중복 방지용 이름 생성
                    ext = origin_name.rsplit('.', 1)[1].lower()
                    save_name = f"{uuid.uuid4().hex}.{ext}"
                    file_path = os.path.join(upload_folder, save_name)

                    # 서버 폴더에 실제 파일 저장
                    file.save(file_path)

                    # DB에 파일 정보(attachments) 저장
                    sql_file = """
                        INSERT INTO attachments (post_id, origin_name, save_name, file_path, file_size)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    # f.seek(0, 2) 등으로 사이즈를 구할 수 있으나 간단히 0 처리 또는 생략 가능
                    cursor.execute(sql_file, (post_id, origin_name, save_name, file_path, 0))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving post: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    # 파일게시물 목록
    @staticmethod
    def get_posts():
        """작성자 이름과 함께 게시글 목록 조회"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT p.*, m.name as writer_name 
                    FROM posts p
                    JOIN members m ON p.member_id = m.id
                    ORDER BY p.created_at DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            conn.close()

    # 파일게시물 자세히보기
    @staticmethod
    def get_post_detail(post_id):
        """게시글 상세 정보와 첨부파일 정보를 함께 조회"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 조회수 증가
                cursor.execute("UPDATE posts SET view_count = view_count + 1 WHERE id = %s", (post_id,))

                # 2. 게시글 정보 조회 (작성자 이름 포함)
                sql_post = """
                        SELECT p.*, m.name as writer_name 
                        FROM posts p
                        JOIN members m ON p.member_id = m.id
                        WHERE p.id = %s
                    """
                cursor.execute(sql_post, (post_id,))
                post = cursor.fetchone()

                # 3. 첨부파일 정보 조회
                cursor.execute("SELECT * FROM attachments WHERE post_id = %s", (post_id,))
                files = cursor.fetchall()

                conn.commit()
                return post, files
        finally:
            conn.close()