from .cart import Cart

# context processor : 모든 템플릿을 해석할 때 항상 처리해야하는 정보가 있을 때 담당하는 기능
# 설정의 템플릿 옵션 설정에 추가
def cart(request):
    cart = Cart(request)
    return {"cart": cart}
