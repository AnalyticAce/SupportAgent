from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    account_status = Column(String, nullable=False)  # e.g., 'active', 'inactive', 'suspended'
    subscription_plan = Column(String, nullable=False)  # e.g., 'free', 'basic', 'premium', "enterprise"