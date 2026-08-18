import sys

sys.path.insert(0, '.')

from fastapi.testclient import TestClient
from backend.database import SessionLocal, Base, engine
from backend.models import User, StudentProfile
from backend.main import app

Base.metadata.create_all(bind=engine)
db = SessionLocal()
db.query(StudentProfile).delete()
db.query(User).delete()
db.commit()
db.close()

client = TestClient(app)
print('register', client.post('/register', json={'full_name': 'Old Name', 'email': 'old@example.com', 'password': 'password123'}).status_code)
login = client.post('/login', json={'email': 'old@example.com', 'password': 'password123'})
print('login', login.status_code)
token = login.json()['access_token']
profile = client.put('/profile', json={'full_name': 'New Name', 'email': 'new@example.com'}, headers={'Authorization': 'Bearer ' + token})
print('profile', profile.status_code)
print(profile.json())

db = SessionLocal()
user = db.query(User).filter(User.email == 'new@example.com').first()
print('new user exists', user is not None)
print('saved full_name', user.full_name if user else None)
old = db.query(User).filter(User.email == 'old@example.com').first()
print('old user exists', old is not None)
db.close()

print('login updated', client.post('/login', json={'email': 'new@example.com', 'password': 'password123'}).status_code)
print('empty email', client.put('/profile', json={'full_name': 'Bad', 'email': '   '}, headers={'Authorization': 'Bearer ' + token}).status_code)
print('duplicate register', client.post('/register', json={'full_name': 'Other', 'email': 'new@example.com', 'password': 'pass1234'}).status_code)
