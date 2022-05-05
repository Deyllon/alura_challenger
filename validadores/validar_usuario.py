from email_validator import validate_email, EmailNotValidError
from usuarios.models import Usuarios
from django.contrib.auth.models import User



def validar_email(email):
    
    try:
        email = validate_email(email).email
        return True
    except EmailNotValidError:
        return False
    
def verifica_se_email_ja_existe(email):
    
    if User.objects.filter(email=email).exists():
        return True
    
    return False
