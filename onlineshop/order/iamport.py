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

    if access_res["code"] == 0:
        return access_res["response"]["access_token"]
    else:
        return None


# 2. 결제 정보 전달
def payments_prepare(order_id, amount, *args, **kwargs):
    access_token = get_token()
    if access_token:
        access_data = {"merchant_uid": order_id, "amount": amount}
        url = "https://api.iamport.kr/payments/prepare"
        headers = {"Authorization": access_token}
        req = requests.post(url, data=access_data, headers=headers)
        res = req.json()

        if res["code"] != 0:
            raise ValueError("API 통신 오류")
    else:
        raise ValueError("Token Error")


# 3. 결제 완료 및 확인
def find_transaction(order_id, *args, **kwargs):
    access_token = get_token()
    if access_token:
        url = "https://api.iamport.kr/payments/find/" + order_id
        headers = {"Authorization": access_token}
        req = requests.post(url, headers=headers)
        res = req.json()

        if res["code"] == 0:
            res = res["response"]
            context = {
                "imp_id": res["imp_uid"],
                "merchant_order_id": res["merchant_uid"],
                "amount": res["amount"],
                "status": res["status"],
                "type": res["pay_method"],
                "receipt_url": res["receipt_url"],
            }
            return context
        else:
            return None
    else:
        raise ValueError("Token Error")
