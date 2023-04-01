from itertools import product
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from Product_App.models import Product



from Product_App.forms import ReserveForm

from .models import History, Order, Reservation, Restaurent

# Create your views here.

def index(request):
    restaurent = Restaurent.objects.all()
    return render(request,'Product_App/index.html', {'values':restaurent})


def reservation(request,id):
    queryset = Restaurent.objects.filter(pk=id)
    restaurent = get_object_or_404(queryset, pk=id)

    #Getting specific restaurent seat capacity
    for seat in queryset:
        restaurent_seat=seat.total_seat

   #Passes into the ReserveForm to make error
    form = ReserveForm(restaurent_seat=restaurent_seat)

    if request.method == 'POST':
            form = ReserveForm(restaurent_seat = restaurent_seat,data=request.POST)
            if form.is_valid():
                reserved = form.save(commit=False)
                reserved.user = request.user
                reserved.restaurents = restaurent
                reserved.save()
                messages.success(request, "Request for reservation successfull. Wait Please!")
                return HttpResponseRedirect(reverse('Product_App:index'))
                
    return render(request, 'Product_App/reservation.html', {'form':form, 'restaurent':queryset})

def ur_reserve(request):
    table = Reservation.objects.filter(user=request.user)
    return render(request, 'Product_App/your_reserve.html', {'table':table})

def orders(request):
    if request.method == 'POST':
        extra_charge = request.POST.get('service')
        rest_id = request.POST.get('rest_id')

        cart = request.session.get('cart')
        sum = 0
        for key_1, value_1 in cart.items():
            val = value_1['restaurent_id']
            val = value_1['restaurent_id']
            price = value_1['price']
            
            if int(val) == int(rest_id):
                sum = sum+int(price)

        for key, value in cart.items():
            val = value['restaurent_id']
            total = int(value['quantity'])*int(value['price'])


            if int(val) == int(rest_id):
                if extra_charge == 'waiter':
                    order = Order(
                        image = value['image'],
                        product_name= value['name'],
                        product_id= value['product_id'],
                        user = request.user,
                        price = value['price'],
                        quantity = value['quantity'],
                        total = total+10,
                    )
                    order.save()
                elif extra_charge == 'self':
                    order = Order(
                        image = value['image'],
                        product_name= value['name'],
                        product_id= value['product_id'],
                        user = request.user,
                        price = value['price'],
                        quantity = value['quantity'],
                        total = total,
                    )
                    order.save()

                #Order
                orders = Order.objects.last()

                history = History(
                    order = orders,
                    user = request.user,
                    product_id= value['product_id'],
                    restaurent_id = value['restaurent_id'],
                )
                history.save()
        request.session['cart'] = {}
        messages.success(request, "Order Placed Successfully")
        return redirect('Product_App:index')


    print(extra_charge, rest_id, sum)
    
    return render(request, 'Product_App/orders.html')

def menu_list(request, id):
    queryset = Restaurent.objects.filter(pk=id)
    restaurent = get_object_or_404(queryset, pk=id)
    table = Product.objects.filter(restaurents=restaurent)
    reserve_check = Reservation.objects.filter(restaurents=restaurent)
    
    for check in reserve_check:
        status = check.status
        user = check.user

    return render(request, 'Product_App/menus.html', {'table':table, 'status':status, 'user':user})



@login_required(login_url="/account/login")
def cart_add(request, id):
    cart = Cart(request)
   
    queryset = Product.objects.filter(pk=id)
    product = get_object_or_404(queryset, pk=id)
    restaurent = product.restaurents.id

    cart.add(product=product, restaurent = restaurent)
    return redirect("Product_App:menus", id=restaurent)


@login_required(login_url="/users/login")
def item_clear(request, id):

    cart = Cart(request)
    queryset = Product.objects.filter(pk=id)
    product = get_object_or_404(queryset, pk=id)
    restaurent = product.restaurents.id
    cart.remove(product)

    return redirect("Product_App:cart_detail", id=restaurent)


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    queryset = Product.objects.filter(pk=id)
    product = get_object_or_404(queryset, pk=id)
    restaurent = product.restaurents.id

    cart.add(product=product, restaurent = restaurent)
    return redirect("Product_App:cart_detail",id=restaurent)


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    queryset = Product.objects.filter(pk=id)
    product = get_object_or_404(queryset, pk=id)
    restaurent = product.restaurents.id
    cart.decrement(product=product, restaurent=restaurent)
    return redirect("Product_App:cart_detail", id=restaurent)


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("Product_App:cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request, id):
    queryset = Product.objects.filter(pk=id)
    product = get_object_or_404(queryset, pk=id)
    restaurents = product.restaurents.id
    print(restaurents)
    restaurent = Restaurent.objects.filter(pk=id)

    return render(request, 'Product_App/cart/cart_detail.html', {'restaurent':restaurent})