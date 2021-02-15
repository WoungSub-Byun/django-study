import requests

from django.conf import settings

# 1. iamport로부터 access_token 받아오기
def get_token():
    access_data = {
        "imp_key": settings.IAMPORT_KEY,
        "imp_secret": settings.IAMPORT_SECRET,
    }

    url = "https://api.iamport.kr/users/getToken"

    req = requests.post(url, data=access_data)
    access_res = req.json()

    if access_res["code"] is 0:
        return access_res["response"]["access_token"]
    else:
        return None
