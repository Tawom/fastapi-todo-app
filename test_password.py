from app.database import SessionLocal
from app.models import User
from app.auth import verify_password, get_password_hash
import bcrypt

db = SessionLocal()
user = db.query(User).filter(User.username == 'testuser').first()

print('='*50)
print('PASSWORD VERIFICATION TEST')
print('='*50)

if user:
    print(f'\nTesting user: {user.username}')
    print(f'Stored hash: {user.hashed_password}')

    # Test common passwords
    test_passwords = ['testpass123', 'password123', 'admin123', 'test123', 'password']

    print('\nTesting passwords:')
    print('-'*30)
    for pwd in test_passwords:
        result = verify_password(pwd, user.hashed_password)
        print(f'  "{pwd}": {result}')

    # Direct bcrypt verification
    print('\nDirect bcrypt verification:')
    print('-'*30)
    for pwd in test_passwords:
        direct_result = bcrypt.checkpw(
            pwd.encode('utf-8'),
            user.hashed_password.encode('utf-8')
        )
        print(f'  "{pwd}": {direct_result}')

else:
    print('User not found')

db.close()