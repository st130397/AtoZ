import re
import uuid
import secrets
from content.models import CustomUser
from django.contrib.auth import authenticate, login
from content.serializers import BlogSer, UserSer


class Authentication:

    def __init__(self):
        self.__token_details = {}

    def validate_login(self, request):
        try:
            json_data = request.data
            username = json_data.get('username', '')
            password = json_data.get('passkey', '')
            user = None
            if username and password:
                models = CustomUser.objects.all()
                serilz = UserSer(models, many=True)
                for item in serilz.data:
                    if item.get('username', '') == username and item.get('passkey', '') == password:
                        item.pop('passkey')
                        user = item
                        break
        except Exception as e:
            print(e)
            raise Exception
        return user

    def generate_token(self, user_details):
        token = None
        try:
            if user_details:
                token = str(uuid.uuid1())
                self.__token_details[token] = user_details
        except Exception as e:
            print("Error generating token:", e)
        return token

    def authenticate_user(self, username, role):
        #optimize
        try:
            models = CustomUser.objects.all()
            serilz = UserSer(models, many=True)
            usr_len = len(serilz.data)
            if usr_len > 0:
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return False

    def authenticate_token(self, token):
        res = None
        try:
            if token:
                user_details = self.__token_details.get(token)
                if user_details:
                    res = user_details
        except Exception as e:
            print(e)
        return res

    def validate_email(self, email):
        res = None
        if email:
            res = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)
        return res

    def validate_password(self, passkey):
        res = None
        if passkey:
            res1 = re.findall(r"[A-Z]", passkey)
            res2 = re.findall(r"[a-z]", passkey)
            if res1 and res2:
                res = True
        return res

    def logout(self, token):
        res = None
        try:
            if token:
                user_details = self.__token_details.get(token)
                if user_details:
                    res = self.__token_details.pop(token)
        except Exception as e:
            print(e)
        return res
