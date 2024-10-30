
from fastapi import Depends, status


from .core.database import engine, Sessionlocal

def get_db():
    db = Sessionlocal()
    try: 
        yield db
    finally:
        db.close()


