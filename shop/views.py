from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category,Product

def home_page(request):
    return render(request,"home_page.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            username = username,
            password = password
        )

        if user:
            login(request,user)
            return redirect("/")
        else:
            messages.error(request,"Username yoki parol noto'g'ri !")
            return redirect("/login/")

    return render(request,"login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
    
        #Guard_clause
        if password1 != password2:
            messages.error(request,"Parol1 bilan Parol2 bir xil emas !")
            return redirect(register_page)
           

        user_exists = User.objects.filter(username = username).exists()

        if user_exists:
            messages.error(request,"Bu username allaqachon olingan !")
            return redirect(register_page)
            
        new_user = User.objects.create(
            username = username,
        ) 

        new_user.set_password(raw_password = password2)

        new_user.save()

        return redirect(login_page)
    
    return render(request, "register.html")

def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        descrition = request.POST.get('descrition')
        image = request.FILES.get('image')
        is_available = request.POST.get('is_available') == 'on'

        try:
            category_obj = Category.objects.get(id=category_id)
        
            Product.objects.create(
                name=name,
                price=price,
                category=category_obj,
                descrition=descrition,
                image=image,
                is_available=is_available,
                owner = request.user,
            )
            messages.success(request, "Mahsulot muvaffaqiyatli qo'shildi!")
            return redirect('product_list')
            
        except Category.DoesNotExist:
            messages.error(request, "Xato: Bunday kategoriya mavjud emas!")
            return redirect('add_product')

    categories = Category.objects.all()
    category = {
        "categories":categories
    }
    return render(request, "add_product.html", category)

def product_list(request):
    products = Product.objects.all()
    product = {
        "products":products
    }
    return render(request, "products.html",product)

def delete_product(request,product_id):
    product = Product.objects.get(id = product_id)
    product.delete()
    return redirect(product_list)


def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if product.owner != request.user:
        messages.error(request, "Sizda tahrirlash huquqi yo'q!")
        return redirect('product_list')

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        category_id = request.POST.get('category')
        product.category = Category.objects.get(id=category_id)
        product.descrition = request.POST.get('descrition')
        product.is_available = request.POST.get('is_available') == 'on'
        
        new_image = request.FILES.get('image')
        if new_image:
            product.image = new_image
            
        product.save()
        messages.success(request, "Mahsulot yangilandi!")
        return redirect('product_list')

    categories = Category.objects.all()
    return render(request, 'edit_product.html', {
        'product': product,
        'categories': categories
    })
    