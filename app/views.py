from django.db.models import Q
from django.http import JsonResponse
from unicodedata import category
from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import Customer, Product, Cart, OrderPlaced
from django.contrib.auth.forms import UserCreationForm, User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        airpods = Product.objects.filter(category='A')
        phonecases = Product.objects.filter(category='PC')
        menss = Product.objects.filter(category='M')
        women = Product.objects.filter(category='W')
        maskss = Product.objects.filter(category='MA')
        return render(request, 'app/home.html', 
        {'airpods':airpods,'phonecases':phonecases,'menss':menss,'women':women,'maskss':maskss})


class ProductDetailView(View):
    def get(self,request,pk):
        product1 = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product1.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product1':product1, 'item_already_in_cart':item_already_in_cart})

# def product_detail(request):
#     return render(request, 'app/productdetail.html')

@login_required()
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required()
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.selling_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)



def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)



@login_required()
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required()
def profile(request):
 return render(request, 'app/profile.html')


@login_required()
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})



@login_required()
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op})

def masks(request, data=None):
    if data == None:
        maskss = Product.objects.filter(category='MA')
    elif data == 'Marvel' or data == 'DC' or data == 'Disney' or data == 'Friends':
        maskss = Product.objects.filter(category='MA').filter(brand=data)
    return render(request, 'app/masks.html',{'maskss':maskss})


def mens(request, data=None):
    if data == None:
        mens = Product.objects.filter(category='M')
    elif data == 'Marvel' or data == 'DC' or data == 'Harry_Potter' or data == 'Star_Wars' or data == 'X-Men':
        mens = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/mens.html', {'mens':mens})



def womens(request, data=None):
    if data == None:
        wom = Product.objects.filter(category='W')
    elif data == 'Harry_Potter' or data == 'Power_Puff_Girls' or data == 'TJ' or data == 'Garfield' or data == 'DC' or data == 'Lion_King' or data == 'Minions':
        wom = Product.objects.filter(category='W').filter(brand=data)
    return render(request, 'app/womens.html', {'wom':wom})




def phonecase(request,data=None):
    if data == None:
        phonecases = Product.objects.filter(category='PC')
    elif data == 'Marvel' or data == 'DC' or data == 'Disney' or data == 'Lion_King':
        phonecases = Product.objects.filter(category='PC').filter(brand=data)
    return render(request, 'app/phonecase.html',{'phonecases':phonecases})

# def login(request):
#  return render(request, 'app/login.html')

def airpod(request, data=None):
    if data == None:
        air = Product.objects.filter(category='A')
    elif data == 'Marvel' or data == 'DC' or data == 'Disney' or data == 'Lion_King':
        air = Product.objects.filter(category='A').filter(brand=data)
        return render(request, 'app/airpod.html',{'air':air})

@login_required()
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'totalamount':totalamount, 'add':add, 'cart_items':cart_items})

# def signup(request):
    # return render(request, 'app/signup.html')

@login_required()
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/signup.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!!, Registered Successfully.')
            form.save()
        return render(request, 'app/signup.html', {'form':form})

@method_decorator(login_required(), name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form,'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name, locality=locality, city=city,state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Nice, Profile Updated Successfully!!!')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})