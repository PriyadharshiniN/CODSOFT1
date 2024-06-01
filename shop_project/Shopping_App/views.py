from django.shortcuts import get_object_or_404, render,redirect
from django.http import  Http404, JsonResponse
from django.contrib import messages
from Shopping_App.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json
from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .form import PaymentForm, QuantityForm


def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"Shopping_App/index.html",{"products":products})
   
def register(request):
    return render(request,"Shopping_App/register.html")

def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"Shopping_App/collections.html",{"catagory":catagory})
 
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"Shopping_App/fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
 
 
 
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    total_amount = sum(item.total_cost for item in cart)
    return render(request,"Shopping_App/cart.html",{"cart":cart,"total_amount":total_amount})
  else:
    return redirect("/")
 
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
 
 
 
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
 
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")
 
 


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                email = user.email
                username = user.username
                
                send_mail(
                    'Login Notification',
                    f'Hi {username},\n\nYou have successfully logged in to your Phoenix Mart account.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                messages.success(request, "Logged in Successfully")
                return redirect("home")
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect("/login")
        return render(request, "Shopping_App/login.html")


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = user.email

            send_mail(
                'Registration Successful',
                f'Hi {username},\n\nYou have successfully registered an account with us.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Registration Success! You can log in now.")
            return redirect('/login')
    return render(request, "Shopping_App/register.html", {'form': form})

 
def collections(request):
  catagory=Catagory.objects.filter(status=0)
  return render(request,"Shopping_App/collections.html",{"catagory":catagory})
  
 
def collectionsview(request,name):
  if(Catagory.objects.filter(name=name,status=0)):
      products=Product.objects.filter(catagory__name=name)
      return render(request,"Shopping_App/products/index.html",{"products":products,"category_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')
 
 
def product_details(request,cname,pname):
  if(Catagory.objects.filter(name=cname,status=0)):
    if(Product.objects.filter(name=pname,status=0)):
      products=Product.objects.filter(name=pname,status=0).first()
      return render(request,"Shopping_App/products/product_details.html",{"products":products})
    else:
      messages.error(request,"No Such Produtct Found")
      return redirect('collections')
  else:
    messages.error(request,"No Such Catagory Found")
    return redirect('collections')

def payment(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cost = sum(item.total_cost for item in cart_items)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            for item in cart_items:
                OrderView.objects.create(
                    user=request.user,
                    product=item.product,
                    product_qty=item.product_qty
                )
            cart_items.delete()
            return redirect('Shopping_App/order_success')
    else:
        form = PaymentForm()
    return render(request, 'Shopping_App/payment.html', {'form': form, 'total_cost': total_cost})
  
@login_required  
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cost = sum(item.total_cost for item in cart_items)
    if request.method == 'POST':
        for item in cart_items:
            OrderView.objects.create(
                user=request.user,
                product=item.product,
                product_qty=item.product_qty
            )
        return redirect('order_success')
    return render(request, 'Shopping_App/place_order.html', {'cart_items': cart_items,'total_cost':total_cost})
  
  
@login_required
def order_success(request):
    return render(request, 'Shopping_App/order_success.html')

@login_required
def payment_success(request):
    return render(request, 'Shopping_App/payment_success.html')
  
  
  
@login_required
def buy_now(request):

    product_id = request.GET.get('id')
    quantity = request.GET.get('qty')
    product_name = request.GET.get('name')
    product = get_object_or_404(Product, pk=product_id)
    total_amount =int( product.selling_price) * int(quantity)
    
    if product_id and quantity and product_name and total_amount:
        return render(request,"Shopping_App/buy_now.html",{'product_id':product_id,'qty':quantity,'product_name':product_name,'total_amount':total_amount,'product':product})
    else:
        return HttpResponse("Missing parameters", status=400)
    
@login_required
def buy_payment(request, product_id, qty):
    product = get_object_or_404(Product, pk=product_id)
    total_amount = qty * product.selling_price
    return render(request, 'Shopping_App/buy_payment.html', {
        'product_name': product.name,
        'product_qty': qty,
        'total_amount': total_amount,
        'product_id': product_id,
        'product': product,
    })
       
@login_required
def cancel_order(request):
  if request.method == "POST":
    return render(request,'Shopping_App/order_history.html')