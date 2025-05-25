import asyncio
import asyncio
from app.database import SessionLocal, engine, Base, User, Faq
from app.agent import generate_embedding

async def seed_database():
    session = SessionLocal()
    
    try:
        # Clear existing data and seed users
        print("Clearing existing data...")
        session.query(Faq).delete()
        session.query(User).delete()
        session.commit()
        
        users = [
            User(user_id=1, name="Alice", email="alice@gmail.com", account_status="active", subscription_plan="premium"),
            User(user_id=2, name="Bob", email="bob@gmail.com", account_status="active", subscription_plan="basic"),
            User(user_id=3, name="Shalom", email="shalom@gmail.com", account_status="inactive", subscription_plan="enterprise")
        ]
        session.add_all(users)
        session.commit()
        print('Users seeded successfully.')
        
        # Seed FAQs with embeddings
        print("Generating embeddings for FAQs...")
        
        faq_data = [
            {
                "question": "How do I reset my password?",
                "answer": "You can reset your password by going to the settings page and clicking on 'Reset Password'.",
                "category": "general"
            },
            {
                "question": "What is the refund policy?",
                "answer": "We offer a 30-day money-back guarantee for all subscription plans.",
                "category": "billing"
            },
            {
                "question": "How do I upgrade my subscription?",
                "answer": "You can upgrade your subscription from the billing section in your account settings.",
                "category": "billing"
            },
            {
                "question": "What should I do if I encounter a technical issue?",
                "answer": "Please contact our support team via email or through the support portal.",
                "category": "technical"
            },
            {
                "question": "How do I cancel my subscription?",
                "answer": "You can cancel your subscription at any time from your account settings under the billing section.",
                "category": "billing"
            },
            {
                "question": "What features are included in the premium plan?",
                "answer": "The premium plan includes advanced analytics, priority support, custom integrations, and increased API limits.",
                "category": "billing"
            },
            {
                "question": "Can I use the service on multiple devices?",
                "answer": "Yes, your account can be accessed from multiple devices simultaneously as long as you're logged in with the same credentials.",
                "category": "general"
            },
            {
                "question": "How do I integrate the service with third-party tools?",
                "answer": "Go to the Integrations section in your dashboard to connect with supported tools like Slack, Zapier, and Google Workspace.",
                "category": "technical"
            },
            {
                "question": "Is there a free trial available?",
                "answer": "Yes, we offer a 14-day free trial with access to all premium features. No credit card required.",
                "category": "billing"
            },
            {
                "question": "How often is my data backed up?",
                "answer": "We back up all customer data daily to secure, redundant storage systems.",
                "category": "technical"
            },
            {
                "question": "Can I customize user roles and permissions?",
                "answer": "Yes, team admins can define custom roles and permissions in the Team Management settings.",
                "category": "general"
            },
            {
                "question": "What happens to my data after I cancel my subscription?",
                "answer": "Your data will remain accessible for 30 days after cancellation. After that, it will be permanently deleted from our servers.",
                "category": "billing"
            }
        ]
        
        faqs = []
        for faq_item in faq_data:
            # Generate embedding for the combined question and answer
            text_for_embedding = f"{faq_item['question']} {faq_item['answer']}"
            embedding = await generate_embedding(text_for_embedding)
            
            faq = Faq(
                question=faq_item['question'],
                answer=faq_item['answer'],
                category=faq_item['category'],
                embedding=embedding
            )
            faqs.append(faq)
        
        session.add_all(faqs)
        session.commit()
        print('FAQs seeded successfully with embeddings.')
            
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    asyncio.run(seed_database())