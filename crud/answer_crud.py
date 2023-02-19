from datetime import datetime

from sqlalchemy.orm import Session

from db.domain.answer_schema import AnswerCreate, AnswerUpdate
from db.models.answer import Answer
from db.models.question import Question
from db.models.user import User

def create_answer(db: Session, question: Question, answer_create: AnswerCreate, user: User):
    db_answer = Answer(question=question,
                      content=answer_create.content,
                      create_date=datetime.now(),
                      user=user)
    db.add(db_answer)
    db.commit()


def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)


def update_answer(db: Session, db_answer: Answer,
                  answer_update: AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit()


def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()