from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String


engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    account_status = Column(String, nullable=False)  # e.g., 'active', 'inactive', 'suspended'
    subscription_plan = Column(String, nullable=False)  # e.g., 'free', 'basic', 'premium', "enterprise"


class Faq(Base):
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(String, nullable=True)  # e.g., 'billing', 'technical', 'general'
    embedding = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<FAQ(question={self.question}, answer={self.answer}, category={self.category}, embedding={self.embedding})>"


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class DataconnectionUser:
    @classmethod
    async def user_name(cls, user_id: int) -> str:
        with get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                return user.name
            else:
                return "User not found"

    @classmethod
    async def account_status(cls, user_id: int) -> str:
        with get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                return user.account_status
            else:
                return "User not found"

    @classmethod
    async def subscription_plan(cls, user_id: int) -> str:
        with get_session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                return user.subscription_plan
            else:
                return "User not found"

class DataconnectionFaq:
    @classmethod
    async def get_faqs(cls):
        with get_session() as session:
            faqs = session.query(Faq).all()
            return [{"question": faq.question, "answer": faq.answer, "category": faq.category} for faq in faqs]
    
    @classmethod
    async def get_faq_by_category(cls, category: str):
        with get_session() as session:
            faqs = session.query(Faq).filter(Faq.category == category).all()
            return [{"question": faq.question, "answer": faq.answer} for faq in faqs]
    
    @classmethod
    async def get_faq_by_id(cls, faq_id: int):
        with get_session() as session:
            faq = session.query(Faq).filter(Faq.id == faq_id).first()
            if faq:
                return {"question": faq.question, "answer": faq.answer, "category": faq.category}
            else:
                return None
    
    @classmethod
    async def add_faq(cls, question: str, answer: str, category: str = None, embedding: list[float] = None):
        # embedding = await generate_embedding(f"{question}\n{answer}")
        with get_session() as session:
            new_faq = Faq(question=question, answer=answer, category=category, embedding=str(embedding) if embedding else None)
            session.add(new_faq)
            session.commit()
            return {"id": new_faq.id, "question": new_faq.question, "answer": new_faq.answer, "category": new_faq.category}

    @classmethod
    async def update_faq(cls, faq_id: int, question: str = None, answer: str = None, category: str = None):
        with get_session() as session:
            faq = session.query(Faq).filter(Faq.id == faq_id).first()
            if faq:
                if question:
                    faq.question = question
                if answer:
                    faq.answer = answer
                if category:
                    faq.category = category
                session.commit()
                session.refresh(faq)
                return {"id": faq.id, "question": faq.question, "answer": faq.answer, "category": faq.category}
            else:
                return None
    
    @classmethod
    async def delete_faq(cls, faq_id: int):
        with get_session() as session:
            faq = session.query(Faq).filter(Faq.id == faq_id).first()
            if faq:
                session.delete(faq)
                session.commit()
                return {"message": "FAQ deleted successfully"}
            else:
                return {"message": "FAQ not found"}

    @classmethod
    async def search_by_embedding(cls, query_embedding: list[float]):
        with get_session() as session:
            sql = """
            SELECT question, answer, category
            FROM faqs
            ORDER BY embedding <-> :embedding
            LIMIT 5
            """
            result = session.execute(sql, {"embedding": query_embedding})
            return [{"question": r["question"], "answer": r["answer"], "category": r["category"]} for r in result]
