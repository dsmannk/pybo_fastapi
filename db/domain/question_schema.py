import datetime

from pydantic import BaseModel, validator

from db.domain.answer_schema import Answer
from db.domain.user_schema import User

# Pydantic은 API의 입출력 항목을 다음과 같이 정의하고 검증할수 있다.
#  - 입출력 항목의 갯수와 타입을 설정
#  - 입출력 항목의 필수값 체크
#  - 입출력 항목의 데이터 검증

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    # Answer 모델은 Question 모델과 answers라는 이름으로 연결되어 있다.
    # Answer 모델에 Queston 모델을 연결할 때 backref="answers" 속성을 지정했기 때문이다.
    # 따라서 Question 스키마에도 answers라는 이름의 속성을 사용해야 등록된 답변들이 정확하게 매핑된다.
    # 만약 answers 대신 다른 이름을 사용한다면 값이 채워지지 않을 것이다.
    answers: list[Answer] = []
    user: User | None
    modify_date: datetime.datetime | None = None
    voter: list[User] = []

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class QuestionList(BaseModel):
    # 질문 목록 API의 출력항목으로 질문 목록 데이터만 있었지만
    # total 항목을 추가해야 하기 때문에, 질문 목록 API의 응답으로
    # 사용할 스키마를 다음과 같이 새로 작성해야 한다.
    total: int = 0
    question_list: list[Question] = []


class QuestionUpdate(QuestionCreate):
    question_id: int


class QuestionDelete(BaseModel):
    question_id: int


class QuestionVote(BaseModel):
    question_id: int