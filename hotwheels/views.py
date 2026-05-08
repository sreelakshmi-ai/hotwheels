from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Product, Category

def home(request):
    
    featured = Product.objects.filter(is_featured=True)[:8]
    new_arrivals = Product.objects.filter(is_new_arrival=True)[:8]
    
    return render(request, 'home.html',{
      
        'featured': featured,
        'new_arrivals': new_arrivals,
        
    })

def about(request):
    return render(request, 'hotwheels/about.html')

def contact(request):
    return render(request, 'hotwheels/contact.html')

    from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, Order, OrderItem
from django.contrib import messages

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'product_list.html', {'products': products, 'categories': categories})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'hotwheels/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, 'Product added to cart')
    return redirect('cart')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('product_list')
    total = sum(item.total_price() for item in cart_items)
    # Order create cheyyunna logic ivide add cheyyam
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

    from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

    from django.shortcuts import get_object_or_404

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'hotwheels/product_detail.html', {'product': product})





from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Wishlist
from django.contrib.auth.decorators import login_required


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('product_list')


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('product_list')
    from django.shortcuts import render

def login_view(request):
    return render(request, 'login.html')


def cart_view(request):             
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    
    return render(request, 'hotwheels/cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    cart.pop(str(id), None)
    request.session['cart'] = cart
    return redirect('cart')

def checkout(request):
    request.session['cart'] = {}
    return render(request, 'hotwheels/checkout_success.html')

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})  
    product_id = str(product_id)
    
    if product_id in cart:
        cart[product_id] += 1   
    else:
        cart[product_id] = 1    
    
    request.session['cart'] = cart
    return redirect('cart')     

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        
        total = 0
        order = Order.objects.create(customer_name=name, customer_email=email, customer_phone=phone, total_amount=0)
        
        for product_id, qty in cart.items():
            product = Product.objects.get(id=product_id)
            subtotal = product.price * qty
            total += subtotal
            OrderItem.objects.create(order=order, product=product, qty=qty, price=product.price)
        
        order.total_amount = total
        order.save()
        request.session['cart'] = {}  # cart clear cheyyu
        return render(request, 'hotwheels/checkout_success.html', {'order': order})
    
    return render(request, 'hotwheels/checkout.html')


