from cryptography.fernet import Fernet
from django.conf import settings


def encrypt_message(message):
    fernet = Fernet(settings.FERNET_KEY.encode())
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message.decode()


def decrypt_message(encrypted_message):
    fernet = Fernet(settings.FERNET_KEY.encode())
    decrypted_message = fernet.decrypt(encrypted_message.encode())
    return decrypted_message.decode()

def get_message_content(message):
    if message.is_encrypted:
        return decrypt_message(message.content)
    return message.content