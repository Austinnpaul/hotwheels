from django.shortcuts import render,redirect
from .models import Car, Wishlist,Cart,CartItem

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
# --
from django.shortcuts import redirect, render, get_object_or_404
from .models import Car

from django.shortcuts import get_object_or_404, redirect
from .models import *
from django.http import HttpResponseBadRequest
from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt


# from django.shortcuts import render

def about(request):
    """
    Renders the About page for the HotWheels E-Commerce site.
    """
    # Optional dynamic data
    team_members = [
        {"name": "Alice", "role": "Founder & Collector", "img": "https://randomuser.me/api/portraits/men/32.jpg"},
        {"name": "Bob", "role": "Marketing Lead", "img": "https://randomuser.me/api/portraits/women/44.jpg"},
        {"name": "Charlie", "role": "Product Manager", "img": "https://randomuser.me/api/portraits/men/56.jpg"},
        {"name": "Dana", "role": "Customer Support", "img": "https://randomuser.me/api/portraits/women/66.jpg"},
    ]

    context = {
        "page_title": "About Us - HotWheels E-Commerce",
        "team_members": team_members
    }
    return render(request, "about.html", context)


def logout_view(request):
    logout(request)  # This clears the session/cookies
    return redirect('userlogin')

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
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            user = User.objects.create_user(username=username,password=password1,email=email)
            user.save()
            return redirect(userlogin)
        else:
            print("password does't match")
            return redirect(userregister)
    return render(request, 'userregister.html')



def userlogin(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(request,username=username,password=password)
        print(user)
        

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect(user_page)
        else:
            return redirect(userlogin)

        messages.error(request, "Invalid credentials")

    return render(request, "userlogin.html")


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




def catalog(request):
    data=Car.objects.all()

    return render(request, 'catalog.html',{'data':data})



@login_required
def add_to_cart(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        car=car
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{car.name} quantity updated in your cart 🛒")
    else:
        messages.success(request, f"{car.name} added to your cart 🛒")

    # Redirect back to same page (catalog or product page)
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')  # Optional: redirect to login

    # Get the user's cart or None if it doesn't exist
    cart = Cart.objects.filter(user=request.user).first()
    items = []
    total = 0

    if cart:
        cart_items = cart.items.select_related('car').all()
        for item in cart_items:
            subtotal = item.car.price * item.quantity
            total += subtotal
            items.append({
                'id': item.id,
                'car': item.car,
                'quantity': item.quantity,
                'subtotal': subtotal
            })

    return render(request, 'cart.html', {'items': items, 'total': total})




def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    return redirect('cart')

def buynows(request):
    return render(request, 'buynow.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'userlist.html', {'users': users})

def user_page(request):
    data = Car.objects.all()
    return render(request, 'userpage.html', {'data': data})

# ---------------- WISHLIST ----------------

@login_required
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    # We look for a record that has BOTH this user and this car.
    # This prevents the "MultipleObjectsReturned" crash.
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        car=car
    )

    if created:
        messages.success(request, f"{car.name} added to your wishlist! 🏎️")
    else:
        messages.info(request, f"{car.name} is already in your wishlist.")

    return redirect(request.META.get('HTTP_REFERER', 'userpage'))

@login_required
def wishlist_view(request):
    # Fetch all wishlist entries for the current user
    # .select_related('car') makes the query faster by grabbing car details in one go
    items = Wishlist.objects.filter(user=request.user).select_related('car').order_by('-created_at')
    
    context = {
        'items': items,
    }
    return render(request, 'wishlist.html', context)  

@login_required
def remove_from_wishlist(request, car_id):
    # We find the specific entry for this user and this car
    item = Wishlist.objects.filter(user=request.user, car_id=car_id)
    
    if item.exists():
        item.delete()
        messages.warning(request, "Removed from wishlist.")
    
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))
def edit_car(request, id):
    car = get_object_or_404(Car, id=id)

    if request.method == "POST":
        car.name = request.POST.get('name')
        car.description = request.POST.get('description')
        car.price = request.POST.get('price')
        car.stock = request.POST.get('stock')

        # Update image only if a new one is uploaded
        if 'image' in request.FILES:
            car.image = request.FILES['image']

        car.save()
        return redirect('product_list')  # your product list page

    return render(request, 'edit.html', {'car': car})

def remove_wishlist(request, id):
    Wishlist.objects.filter(user=request.user, car_id=id).delete()
    messages.info(request, "Item removed from wishlist")
    return redirect('wishlist')



# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def buy_now(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = float(request.POST.get("amount")) * 100  # Razorpay expects paise

        # Create an order in Razorpay
        razorpay_order = client.order.create({
            "amount": int(amount),
            "currency": "INR",
            "payment_capture": 1  # auto capture
        })

        # Create Order in DB
        order = Order.objects.create(
            name=name,
            amount=amount/100,  # store in INR
            status=PaymentStatus.PENDING,
            provider_order_id=razorpay_order['id']
        )

        context = {
            "order": order,
            "razorpay_order_id": razorpay_order['id'],
            "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
            "amount": amount,
            "currency": "INR",
            "callback_url": "/paymenthandler/",
        }
        return render(request, "payment.html", context)

    return render(request, "buynow.html")


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id", "")
        razorpay_order_id = request.POST.get("razorpay_order_id", "")
        signature = request.POST.get("razorpay_signature", "")

        order = Order.objects.filter(provider_order_id=razorpay_order_id).first()
        if not order:
            return HttpResponseBadRequest("Order not found")

        # Verify signature
        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            # Payment success
            order.payment_id = payment_id
            order.signature_id = signature
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "payment_success.html", {"order": order})
        except:
            # Payment failed
            order.status = PaymentStatus.FAILED
            order.save()
            return render(request, "payment_failed.html", {"order": order})

    return HttpResponseBadRequest("Invalid request method")