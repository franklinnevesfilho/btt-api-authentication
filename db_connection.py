from sqlmodel import create_engine, Session, SQLModel

db_name = "test_db"
db_url = f"mysql+pymysql://root:@localhost:3306/{db_name}"
engine = None

def create_db_and_tables():
    global engine
    engine = create_engine(db_url)
    SQLModel.metadata.create_all(engine)

def get_session():
    if engine is None:
        create_db_and_tables()
    return Session(engine)