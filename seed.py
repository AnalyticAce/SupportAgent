from models import User
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

def seed_database():
    session = SessionLocal()
    
    if not session.query(User).first():
        users = [
            User(user_id=1, name="Alice", email="alice@gmail.com", account_status="active", subscription_plan="premium"),
            User(user_id=2, name="Bob", email="bob@gmail.com", account_status="active", subscription_plan="basic"),
            User(user_id=3, name="Shalom", email="shalom@gmail.com", account_status="inactive", subscription_plan="enterprise")
        ]
        session.add_all(users)
        session.commit()
        print('Database seeded successfully.')
    else:
        print('Database already seeded.')
    
    session.close()


if __name__ == "__main__":
    seed_database()