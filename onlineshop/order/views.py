from django.shortcuts import render, get_object_or_404

from .models import *
from cart.cart import Cart
from .forms import *

# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.get_discount_total()
                order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
                cart.clear()
                return render(request, "order/created.html", {"order": order})
    else:
        form = OrderCreateForm()
    return render(request, "order/create.html", {"cart": cart, "form": form})
