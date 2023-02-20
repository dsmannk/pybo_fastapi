# FastAPI 서버 실행하기 (백엔드 서버)
# 파이참 터미널 projects/myapi 디렉터리에서 uvicorn main:app --reload 명령어 실행
# [파이참 터미널]
# (myapi) myapi % uvicorn main:app --reload
# Svelte 서버 실행하기 (프론트엔드 서버)
# VSCode 터미널 projects/myapi/frontend 디렉터리에서 npm run dev 명령어 실행
# [VSCode 터미널]
# frontend % npm run dev

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes import question, answer, user
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from core.config import settings

#from . import model
#from .database import engine
#MYSQL_URL = settings.DATABASE_URL

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",    # 또는 "http://localhost:5173"
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question.router)
app.include_router(answer.router)
app.include_router(user.router)


# app.add_middleware(DBSessionMiddleware, db_url=MYSQL_URL)

# @app.get("/hello")
# def hello():
#     return {"message": "안녕하세요 파이보"}


# @app.get("/user/test")
# async def user():
#     query = db.session.query(User)
#     return query.all()


# from db.models.answer import Answer
# from db.models.question import Question
# from datetime import datetime
# q = Question(subject='pybo가 무엇인가?', content='pybo에 대해 알고 싶습니다.', create_date=datetime.now())
# from db.session import SessionLocal
# db = SessionLocal()
# db.add(q)
# db.commit()

##################################################################################
# FRONT-END
# 화살표 함수 : https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Functions/Arrow_functions
# 자바스크립트 라이브러리인 moment를 사용하면 날짜를 보기 좋게 다듬을 수 있다. moment - https://momentjs.com/
# 스벨트 스토어 - https://svelte.dev/tutorial/writable-stores

# body에 설정한 qs.stringify(params)는 params 데이터를 'application/x-www-form-urlencoded' 형식에 맞게끔 변환하는 역할을 한다.
# qs.stringify 함수를 사용하기 위해서는 다음과 같이 qs 패키지를 먼저 설치해야 한다.
# [VSCode 터미널]
# frontend % npm install qs

# BACK-END
# 데이터를 조회하는 다양한 사용법은 SQLAlchemy공식 문서를 참조하자.
# SQLAlchemy 공식 문서: https://docs.sqlalchemy.org/en/14/orm/query.html
# https://docs.sqlalchemy.org/en/13/core/type_basics.html

# 제너레이터란? - https://wikidocs.net/134909

# contextmanager - https://docs.python.org/ko/3/library/contextlib.html

# 파이썬 타입 어노테이션 - https://wikidocs.net/134883
# Depends의 활용 예
# Depends는 매우 다양한 방법으로 활용할 수 있다. FastAPI의 다음 문서를 꼭 한번 읽어 보기를 추천한다.
# https://fastapi.tiangolo.com/tutorial/dependencies/

# Pydantic
# Pydantic은 FastAPI의 입출력 스펙을 정의하고 그 값을 검증하기 위해 사용하는 라이브러리이다. Pydantic은 FastAPI 설치시 함께 설치되기 때문에 따로 설치할 필요는 없다.
# Pydantic - https://pydantic-docs.helpmanual.io/
# EmailStr을 사용하기 위해서는 다음과 같이 email_validator를 먼저 설치해야 한다.
# (myapi) c:/projects/myapi> pip install "pydantic[email]"

# 비밀번호를 암호화 하여 저장하기 위해서는 passlib가 필요하다.
# passlib - https://passlib.readthedocs.io/en/stable/index.html

# OAuth2PasswordRequestForm과 jwt를 사용하기 위해서는 먼저 다음의 라이브러리를 설치해야 한다.
# pip install python-multipart
# pip install python-jose[cryptography]

# jwt(Json Web Token)를 사용하여 액세스 토큰을 생성한다.
# jwt란 Json 포맷을 이용하여 사용자에 대한 속성을 저장하는 Claim 기반의 Web Token이다.
# jwt - https://jwt.io/


# SECRET_KEY 생성하기
# 여러분의 SECRET_KEY는 위에 설정한 값과 다르게 설정해야 한다. 다음과 같은 방법으로 SECRET_KEY를 생성할 수 있다.

# openssl이 설치된 터미널을 사용할 수 있다면 다음과 같이 생성하자.

# $ openssl rand -hex 32
# 4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c
# 또는 다음과 같이 secrets 라이브러리를 사용할수도 있다.
# >>> import secrets
# >>> secrets.token_hex(32)
# '344a451d26d1968c0cd4ca12613e5f61b0f71dafced442c730edba55bb9035bc'

# 2023 02 18 작업 진행완료(2-05 질문 목록 화면 만들기)
# 3-07 회원가입 진행할 차례(https://wikidocs.net/176872)

