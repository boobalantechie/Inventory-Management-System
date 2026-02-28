from django.shortcuts import render ,redirect,get_object_or_404
from .models import Product,Category
from django.http  import HttpResponse # iv'e created it 
from .forms import ProductForm ,CategoryForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User

from django.core.paginator import Paginator

# Create your views here.

# def home(request):
#     return HttpResponse("hello boobalan")

# def home(request):
#     # products=Product.objects.all()
#     # return render(request,"home.html",{"products":products})

  # this is old manual form logic 

# def home(request):
#     if request.method=='POST':
#         name=request.POST.get("name")
#         price=request.POST.get("price")

#         Product.objects.create(name=name,price=price)

#         return redirect("home")
#     products=Product.objects.all()
#     return render(request,"home.html",{"products":products})

#--------------------------------------
# this is new automaticall form logic 
#-------------------------------------- 
@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_category = Category.objects.count()
    active_products = Product.objects.filter(status=True).count()
    inactive_products = Product.objects.filter(status=False).count()
    # print(Product)
    context={
        'total_products':total_products,
        'total_category':total_category,
        'active_products':active_products,
        'inactive_products':inactive_products
    }
    return render(request,'dashboard.html',context)



@login_required
def home(request):
    search_query=request.GET.get("search")
    products=Product.objects.all()
    print("searchs",search_query)
    if search_query:
        products=products.filter(name__icontains=search_query)

    #pagination
    paginator=Paginator(products,5)
    page_number=request.GET.get("page")
    products=paginator.get_page(page_number)

    category_form=CategoryForm()
    product_form=ProductForm()
    if request.method=="POST":
        # form=ProductForm(request.POST,request.FILES)


        if 'add_category' in request.POST:
            category_form=CategoryForm(request.POST)
            if category_form.is_valid():
                # category_form.save()
                new_category = category_form.save()
                product_form = ProductForm(initial={
                    "category": new_category.id
                })
        if 'add_product' in request.POST:
            product_form=ProductForm(request.POST)
            if product_form.is_valid():
                product_form.save()
                messages.success(request,"product addded successfully")
                return redirect("home")

            # if form.is_valid():
            #     form.save()
            #     messages.success(request,"product added successfully")
            #     return redirect("home")
    else:
        form=ProductForm()
    # Products=Product.objects.all()
    return render(request,"home.html",{"products":products,"form":product_form,"category_form":category_form})



@login_required
def delete_product(request,id):
    if not request.user.is_staff:
        messages.error(request,"you are not allowed")
    product=get_object_or_404(Product,id=id)
    product.delete()
    messages.success(request,"deleted successfully")
    return redirect("home")

@login_required 
def edit_product(request,id):

    product=get_object_or_404(Product,id=id)

    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES,instance=product)

        if form.is_valid():
            form.save()
            messages.success(request,"product updated successfully")
            return redirect('home')
        # product.name=request.POST.get("name")
        # product.price=request.POST.get("price")
        # product.save()
        # messages.success(request,"updated successfully")
    else:
        form=ProductForm(instance=product)

        # return redirect("home")
    return render(request,"edit.html",{"form":form})


def login_view(request):
    if request.method=="POST":
        print("POST DATA:", request.POST)
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)
        print(user)

        if  user is not None:
            login(request,user)
            messages.success(request,"login succesfull")
            return redirect("home")
        print(user)
    return render(request,"login.html")

def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request,"username already exists")
            return redirect("signup")
        if User.objects.filter(email=email).exists():
            messages.error(request,"email already exists")
            return redirect("signup")
        
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
    
        messages.success(request,"account created successfully")
        return redirect("login")

    return render(request,"signup.html")