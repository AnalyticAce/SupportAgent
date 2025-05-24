import asyncio
from app.database import SessionLocal, engine, Base, User, Faq
from app.agent import generate_embedding

Base.metadata.create_all(bind=engine)

async def seed_database():
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
    elif not session.query(Faq).first():
        faqs = [
            Faq(id=1, 
            question="How do I reset my password?", 
            answer="You can reset your password by going to the settings page and clicking on 'Reset Password'.", 
            category="general",
            embedding=str(await generate_embedding("How do I reset my password? You can reset your password by going to the settings page and clicking on 'Reset Password'."))),
            Faq(id=2, 
            question="What is the refund policy?", 
            answer="We offer a 30-day money-back guarantee for all subscription plans.", 
            category="billing",
            embedding=str(await generate_embedding("What is the refund policy? We offer a 30-day money-back guarantee for all subscription plans."))),
            Faq(id=3, 
            question="How do I upgrade my subscription?", 
            answer="You can upgrade your subscription from the billing section in your account settings.", 
            category="billing",
            embedding=str(await generate_embedding("How do I upgrade my subscription? You can upgrade your subscription from the billing section in your account settings."))),
            Faq(id=4, 
            question="What should I do if I encounter a technical issue?", 
            answer="Please contact our support team via email or through the support portal.", 
            category="technical",
            embedding=str(await generate_embedding("What should I do if I encounter a technical issue? Please contact our support team via email or through the support portal.")))
        ]
        session.add_all(faqs)
        session.commit()
        print('FAQs seeded successfully.')
    else:
        print('Database already seeded.')
    
    session.close()


if __name__ == "__main__":
    asyncio.run(seed_database())