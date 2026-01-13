from django.shortcuts import render,redirect
from .models import Car, Wishlist

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render



def index(request):
    data=Car.objects.all()
    return render(request, 'index.html',{'data':data})
def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        

        if(username=='admin'and password=='admin@123'):
            return redirect('adminlist')


        # If credentials are correct and user is staff, log them in
       
    return render(request,"adminlogin.html")

def adminlist(request):
    return render (request,"dashboard.html")



def userregister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Password check
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('userregister')

        # Username exists check (IMPORTANT)
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('userregister')

        # Email exists check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('userregister')

        # Create user ONLY if all checks pass
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'userregister.html')



def userlogin(request):
    return render (request,"userlogin.html")



def addproduct(request):
    if request.method == "POST":
        Car.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price'],
            stock=request.POST['stock'],
            image=request.FILES['image']
        )
        return redirect('adminlist')

    return render(request, 'addproduct.html')

def product_list(request):
    cars = Car.objects.all()
    return render(request, 'productlist.html', {'cars': cars})

def delete_car(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == "POST":
        car.delete()
    return redirect('product_list')

def userregister(request):
    return render(request, 'userregister.html')


def catalog(request):
    data=Car.objects.all()

    return render(request, 'catalog.html',{'data':data})

from django.shortcuts import redirect, render, get_object_or_404
from .models import Car

def add_to_cart(request, car_id):
    cart = request.session.get('cart', {})

    if str(car_id) in cart:
        cart[str(car_id)] += 1
    else:
        cart[str(car_id)] = 1

    request.session['cart'] = cart
    return redirect('catalog')


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for car_id, quantity in cart.items():
        car = Car.objects.get(id=car_id)
        subtotal = car.price * quantity
        total += subtotal
        items.append({
            'car': car,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {'items': items, 'total': total})


 
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        car=car
    )

    return redirect('catalog')

def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related('car')
    return render(request, 'wishlist.html', {'items': items})

# def remove_from_wishlist(request, car_id):
#     Wishlist.objects.filter(user=request.user, car_id=car_id).delete()
#     return redirect('wishlist')