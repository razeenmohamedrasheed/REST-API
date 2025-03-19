from db import engine,Base
from model.users import User


Base.metadata.create_all(bind=engine)