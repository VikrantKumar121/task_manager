from .models import User
import bcrypt

def authenticate(email,password):
    email=email
    password=password
    try:
        user = User.objects.get(email=email)
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        else:
            return None
    except:
        return None


