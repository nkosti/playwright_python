import random
import string
import uuid

from cryptography.fernet import Fernet


class Utilities:

    @staticmethod
    def generate_email():
        random_string = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        return f'test.user{random_string}@auto.com'

    @staticmethod
    def get_random_text(text: str, length: int = 20) -> str:
        return text + str(uuid.uuid4().hex[:length])

    @staticmethod
    def get_test_number(request):
        return [
            marker.name for marker in request.node.own_markers if "TEST" in marker.name
        ][0]

    @staticmethod
    def decrypt_text(text):
        f = Fernet("tesdfjlksdflkansflas=")
        decrypted_text = f.decrypt(text)
        return decrypted_text.decode("utf-8")
