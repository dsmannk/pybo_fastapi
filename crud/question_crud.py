from datetime import datetime

from db.models.question import Question
from db.models.answer import Answer
from db.models.user import User
from db.domain.question_schema import QuestionCreate, QuestionUpdate
from sqlalchemy.orm import Session


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    question_list = db.query(Question)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username) \
            .outerjoin(User, Answer.user_id == User.id).subquery()

        # sub_query.c.question_id에 사용한 c는 서브쿼리의 조회 항목을 의미한다
        # sub_query = SELECT answer.question_id, answer.content, "user".username
        # FROM answer LEFT OUTER JOIN "user" ON answer.user_id = "user".id

        # sub_query.c = ReadOnlyColumnCollection(anon_1.question_id, anon_1.content, anon_1.username)

        question_list = question_list \
            .outerjoin(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    )
        total = question_list.distinct().count()
        question_list = question_list.order_by(Question.create_date.desc()) \
            .offset(skip).limit(limit).distinct().all()

    else:
        _question_list = question_list.order_by(Question.create_date.desc())

        total = _question_list.count()
        question_list = _question_list.order_by(Question.create_date.desc()) \
            .offset(skip).limit(limit).all()

    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)


def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question


def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now(),
                           user=user)
    db.add(db_question)
    db.commit()


def update_question(db: Session, db_question: Question,
                    question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()


def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()


def vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    db.commit()