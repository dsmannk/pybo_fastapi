import contextlib
from db.session import SessionLocal

#@contextlib.contextmanager # 데이터베이스 세션의 생성과 반환을 자동화하기
def get_db():
    db = SessionLocal()
    try:
        yield db # DB 연결 성공한 경우, DB 세션 시작
    finally:
        db.close()
        # db 세션이 시작된 후, API 호출이 마무리되면 DB 세션을 닫아준다.