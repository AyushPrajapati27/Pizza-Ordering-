from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings


# Create your views here.
def home(request):
    pizza = Pizza.objects.all()
    context = {'pizza':pizza}

    return render(request,'home.html',context)

def login_page(request):
 if request.method == 'POST':
    try:
        username=request.POST.get('username')
        password=request.POST.get('password')

        user_obj=User.objects.filter(username=username)
        if not user_obj.exists():
            messages.warning(request,'User not found')
            return redirect('/login/')
        
        user_obj = authenticate(username=username,password=password)
        
        if user_obj:
           login(request,user_obj)
           return redirect('/')
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('/login/')
        
    
        messages.success(request,'Account Created Successfully')


        return redirect('/login/')
    
    except Exception as e:
        messages.error(request,'Something Went Wrong')
        return redirect('/register/')

 return render(request,'login.html')

def register_page(request):
   if request.method == 'POST':
    try:
        username=request.POST.get('username')
        password=request.POST.get('password')

        user_obj=User.objects.filter(username=username)
        if user_obj.exists():
            messages.warning(request,'Username already exists')
            return redirect('/register/')
        
        user_obj = User.objects.create_user(username=username)
        user_obj.set_password(password)
        user_obj.save()
        
    
        messages.success(request,'Account Created Successfully')


        return redirect('/login/')
    
    except Exception as e:
        messages.warning(request,'Something Went Wrong')
        return redirect('/register/')

   return render(request,'register.html')

@login_required(login_url='/login/')
def add_cart(request,pizza_uid):
    user = request.user
    pizza_obj = Pizza.objects.get(uuid = pizza_uid)
    cart , _ = Cart.objects.get_or_create(user=user,is_paid=False)
    messages.success(request,f"{pizza_obj.pizza_name} add to your cart")
    cart_items=CartItem.objects.create(
       cart=cart,
       pizza=pizza_obj,
    )
    return redirect('/')

@login_required(login_url='/login/')
def cart(request):
    cart_obj, _ = Cart.objects.get_or_create(is_paid=False, user=request.user)
    cart_items = cart_obj.cart_items.all()
    discount = 0
    applied_coupon = None

    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code", "").strip()
        if coupon_code:
            discount, valid, applied_coupon = cart_obj.apply_coupon(coupon_code)
            if valid:
                cart_obj.discount_amount = discount
                cart_obj.applied_coupon = applied_coupon
                cart_obj.save()
                messages.success(request, f"Coupon {applied_coupon} applied! Discount ₹{discount}")
            else:
                messages.error(request, f"Invalid coupon code: {coupon_code}")

    total = cart_obj.get_cart_total()
    final_total = total - discount

    context = {
        'cart': cart_obj,
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total,
        'applied_coupon': applied_coupon
    }
    return render(request, 'cart.html', context)


@login_required(login_url='/login/')
def remove_cart_items(request,cart_item_uid):
   try:
       CartItem.objects.get(uuid=cart_item_uid).delete()
       return redirect('/cart/')
   except Exception as e:
      print(e)

@login_required(login_url='/login/')
def orders(request):
   orders=Cart.objects.filter(is_paid=True,user=request.user)
   context={'orders':orders}
   return render(request,'orders.html',context)

@login_required(login_url='/login/')
def success(request,uuid):
      try:
         cart = Cart.objects.get(user=request.user,uuid=uuid, is_paid=False)
         cart.is_paid = True
         cart.save()
         messages.success(request,"Your Order has been places successfully!")
         return redirect('/orders/')
      except Exception as e:
         messages.warning(request,"Something went wrong!")
         return redirect('/cart/')

def user_logout(request):
   logout(request)
   return redirect('/')

def pizza_list(request):
   query = request.GET.get('q')

   if query:
      pizzas= Pizza.objects.filter(pizza_name__icontains=query)
   else:
      pizzas = Pizza.objects.all()
   return render(request,"home.html",{"pizza":pizzas})
      

def add_to_wishlist(request,pizza_name):
   pizza = get_object_or_404(Pizza,pizza_name=pizza_name)
   Wishlist.objects.get_or_create(user=request.user,pizza=pizza)
   messages.success(request,f"{pizza.pizza_name} has been Successfully added to your wishlist")
   return redirect("wishlist")

def remove_from_wishlist(request,pizza_name):
   pizza = get_object_or_404(Pizza,pizza_name=pizza_name)
   Wishlist.objects.filter(user=request.user,pizza=pizza).delete()
   return redirect("wishlist")

def wishlist(request):
   items = Wishlist.objects.filter(user=request.user)
   return render(request,"wishlist.html",{"items" :items})







