from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector


engine = create_engine(settings.database_url)
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
    embedding = Column(Vector(1536), nullable=True)  # OpenAI embeddings are 1536 dimensions
    
    def __repr__(self):
        return f"<FAQ(question={self.question}, answer={self.answer}, category={self.category})>"


def ensure_tables_exist():
    """
    Ensure all database tables exist. Create them if they don't.
    This function is called automatically when getting a database session.
    """
    try:
        # Check if pgvector extension is available
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM pg_extension WHERE extname = 'vector'"))
            if not result.fetchone():
                print("Warning: pgvector extension not found. Vector operations may not work.")
        
        # Create all tables defined in the models
        Base.metadata.create_all(bind=engine)
        print("Database tables ensured successfully.")
    except Exception as e:
        print(f"Warning: Could not create tables: {e}")
        # Don't raise the exception to avoid breaking the application
        # Just log it for debugging purposes

@contextmanager
def get_session():
    # Ensure tables exist before any database operation
    ensure_tables_exist()
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
        with get_session() as session:
            new_faq = Faq(question=question, answer=answer, category=category, embedding=embedding)
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
    async def search_by_embedding(cls, query_embedding: list[float], limit: int = 5):
        """
        Search FAQs using vector similarity with pgvector extension
        """
        with get_session() as session:
            # Convert list to string format for PostgreSQL vector casting
            embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
            
            # Use pgvector's cosine distance for similarity search
            # Note: Using string formatting here since SQLAlchemy has issues with vector type casting
            sql = text(f"""
            SELECT question, answer, category, embedding <-> '{embedding_str}'::vector as distance
            FROM faqs
            WHERE embedding IS NOT NULL
            ORDER BY embedding <-> '{embedding_str}'::vector
            LIMIT :limit
            """)
            result = session.execute(sql, {"limit": limit})
            return [{"question": r[0], "answer": r[1], "category": r[2], "distance": r[3]} for r in result]
