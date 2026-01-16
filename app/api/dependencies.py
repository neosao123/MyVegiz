from app.db.session import SessionLocal
# Gives DB session to routes

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
