from django.shortcuts import render,redirect
from .models import *
import re
from django.core.paginator import Paginator



def index(request):
    all_products = products.objects.all()[:4]
    return render(request, 'index.html', {
        'all_products': all_products
    })


def register(request):
    try:
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            password = request.POST.get("password")

            # Check empty fields
            if not name or not phone or not email or not password:
                return render(request, "register.html", {
                    "error": "All fields are required."
                })

            # Phone validation
            phone_pattern = r'^[6-9]\d{9}$'
            if not re.match(phone_pattern, phone):
                return render(request, "register.html", {
                    "error": "Enter a valid 10-digit mobile number."
                })

            # Email validation
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
            if not re.match(email_pattern, email):
                return render(request, "register.html", {
                    "error": "Enter a valid email address."
                })

            # Password validation
            password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
            if not re.match(password_pattern, password):
                return render(request, "register.html", {
                    "error": "Password must be at least 8 characters and include an uppercase letter, lowercase letter, number, and special character."
                })

            # Save data
            Register.objects.create(
                name=name,
                phone=phone,
                email=email,
                password=password
            )

            return render(request, "register.html", {
                "message": "User registered successfully."
            })

        return render(request, "register.html")

    except Exception as e:
        return render(request, "register.html", {
            "error": str(e)
        })
  


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        Adminemail= 'admin@gmail.com'
        Adminpass ='1234'

        if email == Adminemail and password == Adminpass:
            request.session['admin'] = True

            return redirect('adnhome')

            # return render(request,'admin.html',{'message':'Admin login sucessfull'})

        try:
            user = Register.objects.get(email=email, password=password)

            request.session['cid'] = email

            return redirect("index")

        except Register.DoesNotExist:
         
         return render(request, "login.html", {"error": "Invalid email or password" })
    else:
     return render(request, "login.html")
    



def adnhome(request):

    if 'admin' not in request.session:
        return redirect('login')

    alluser = Register.objects.count()
    allproducts = products.objects.count()
    total_orders = orders.objects.count()

    revenue = 0

    all_order_data = orders.objects.all()

    for order in all_order_data:
        revenue += order.price

    return render(request, 'admin.html', {
        'alluser': alluser,
        'allproducts': allproducts,
        'total_orders': total_orders,
        'revenue': revenue,
    })

def logout(request):
    if "cid" in request.session:
        request.session.flush()
        return redirect("index")

    elif "admin" in request.session:
        request.session.flush()
        return redirect("index")

    return redirect("login")
 

     
def profile(request):
    if "cid" in request.session:
        userdata = request.session["cid"]
        user = Register.objects.get(email=userdata)

        return render(request, "profile.html", {
            "user": user
        })

    return render(request, "login.html")




def admin_view_customer(request):
    if "admin" in request.session:

        all_customer = Register.objects.all()

        paginator = Paginator(all_customer, 5)   
        print(all_customer)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "view_customer.html", { "all_customer": page_obj})

    else:
        return render(request,'login.html')
    


def open_addproduct(request):
    all_category = Category.objects.all()  
    return render(request, "add_products.html", {"all_category": all_category})







def add_product(request):

    if "admin" not in request.session:
        return render(request, "login.html")

    all_category = Category.objects.all()

    if request.method == "POST":

        category = request.POST.get("category")
        name = request.POST.get("pname")
        price = request.POST.get("pprice")
        description = request.POST.get("pdesc")
        stock = request.POST.get("pstock")
        image = request.FILES.get("pimage")

        context = {
            "all_category": all_category
        }

        # Empty validation
        if not category or not name or not price or not description or not stock or not image:
            context["error"] = "Please fill all fields."
            return render(request, "add_products.html", context)
        

        try:
            category_obj = Category.objects.get(id=category)
            

            products.objects.create(
             Product_category=category_obj,
             Product_name=name,
             Product_price=price,
             Product_description=description,
             Product_stock=stock,
             Product_image=image
)
            context = {
            "all_category": all_category,
            "message": "Product Added Successfully"
}


            return render(request, "add_products.html", context)

        except Exception as e:
            print(e)
            context["error"] = str(e)
            return render(request, "add_products.html", context)

    return render(request, "add_products.html", {
        "all_category": all_category
    })









def view_products(request):
    if "admin" in request.session:

        all_products = products.objects.all()

        paginator = Paginator(all_products, 5)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)

        return render(request, "view_products.html", {
            "all_products": page_obj
        })
    
    return render(request,'login.html')    



def view_customer_products(request):

    all_products = products.objects.all()

    paginator = Paginator(all_products, 10)   
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return render(request, "view_customer_products.html", {
        "all_products": page_obj
    })









# def category(request):
#     if 'admin' in request.session:
#         if request.method == 'POST':
#             c_name=request.POST.get('category_name')
#             data = Category.objects.create(
#                 Category_name = c_name
#             )
#         all_categories = Category.objects.all()
#         paginator = Paginator(all_categories, 10)   
#         page = request.GET.get("page")
#         page_obj = paginator.get_page(page)

#         return render(request, 'category.html', { 'all_categories': page_obj })

#     return render(request,'login.html', { "message": "Unauthorized access" })


def category(request):
    if 'admin' not in request.session:
        return render(request, 'login.html')

    edit_category = None

    if request.GET.get("edit"):
        edit_category = Category.objects.get(id=request.GET.get("edit"))

    if request.method == "POST":
        cat_id = request.POST.get("id")
        name = request.POST.get("category_name")

        if cat_id:
            category = Category.objects.get(id=cat_id)
            category.Category_name = name
            category.save()
        else:
            Category.objects.create(Category_name=name)

        return redirect("category")

    all_categories = Category.objects.all()

    return render(request, "category.html", {
        "all_categories": all_categories,
        "all_category": all_categories,      
        "edit_category": edit_category
    })


def delete_category(request, id):
    if 'admin' not in request.session:
        return render(request, 'login.html', {"message": "Unauthorized Access"})

    category = Category.objects.get(id=id)
    category.delete()

    return redirect("category")


def edit_category(request,id):
    if 'admin' not in request.session:
        return render(request, 'login.html', {"message": "Unauthorized Access"})

    category = Category.objects.get(id=id)

    if request.method == "POST":
        category.Category_name = request.POST.get("category_name")
        category.save()
        return redirect("category")

    return render(request, "category.html", {
    "category": category,
    "all_categories": Category.objects.all()
})





def add_to_cart(request,product_id):
    if 'cid' in request.session:
        userdata=request.session['cid']

        user = Register.objects.get(email = userdata)

        product = products.objects.get(id = product_id)

        price_first = product.Product_price
        quantity = 1

        if product.Product_stock <=0:
               return redirect("view_customer_products")
        
        if Cart.objects.filter(user=user , product=product).exists():
            cart_item=Cart.objects.get(user=user , product= product)
            cart_item.quantity += 1

            price = product.Product_price * cart_item.quantity
            cart_item.price = price

            cart_item.save()
        else: 

         Cart.objects.create(
            user = user,
            product = product,
            price = price_first,
            quantity = quantity
        )
    print("Saved Successfully")
   
    return redirect("view_customer_products") 





def view_cart(request):
    if 'cid' not in request.session:
        return redirect('login')
    
    userdata=request.session['cid']
    
    user = Register.objects.get(email = userdata)

    cart_items = Cart.objects.filter(user=user)

    total = 0
    for item in cart_items:
        total += item.price

    return render(request, "view_cart.html", {
        "cart_items": cart_items,
         "total": total,
    })



def increase_quantity(request, id):
    cart_item = Cart.objects.get(id=id)

    if cart_item.quantity < cart_item.product.Product_stock:
        cart_item.quantity += 1
        cart_item.price = cart_item.product.Product_price * cart_item.quantity
        cart_item.save()

    return redirect('view_cart')




def decrease_quantity(request, id):
    cart_item = Cart.objects.get(id=id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.price = cart_item.product.Product_price * cart_item.quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')


def checkout(request):
      if 'cid' not in request.session:
            return redirect('login')
        
      userdata=request.session['cid'] 
      user = Register.objects.get(email = userdata)
      cart_items = Cart.objects.filter(user=user)

      total = 0
      for item in cart_items:
       total += item.price

      return render(request, "checkout.html", {
        "cart_items": cart_items,
        "user": user,
         "total": total,
        
    })

     



def placeorder(request): 

    if 'cid' not in request.session:
                return redirect('login')

    if request.method =='POST':

        user_email =request.session['cid'] 
        user = Register.objects.get(email = user_email)

        address = request.POST.get("address")
        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:
          
          orders.objects.create(
              user=user,
              product=item.product,
              price=item.price,
              quantity=item.quantity,
              address = address
          )
            
          item.product.Product_stock -= item.quantity
          item.product.save()


        cart_items.delete()

        return redirect('order_success')
    return redirect("checkout")





def view_orders(request):
    if 'cid' not in request.session:
        return redirect('login')

    user_email = request.session['cid']
    user = Register.objects.get(email=user_email)

    all_orders = orders.objects.filter(user=user)

    return render(request, "view_orders.html", {
        "all_orders": all_orders
    })




def order_success(request):
    return render(request, "order_success.html", {
        "message": "Order Placed Successfully!"
    })



# def view_orders(request):

#     if 'cid' not in request.session:
#         return redirect('login')

#     user = Register.objects.get(email=request.session['cid'])

#     order_list = orders.objects.filter(user=user)

#     return render(request, 'view_orders.html', {
#         'orders': order_list
#     })




def admin_orders(request):

    if 'admin' not in request.session:
        return redirect('login')

    order_data = orders.objects.all()

    return render(request, 'admin_orders.html', {
        'orders': order_data
    })


def update_order_status(request, id, status):

    if 'admin' not in request.session:
        return redirect('login')

    try:
        data = orders.objects.get(id=id)
        data.status = status
        data.save()
    except orders.DoesNotExist:
        pass

    return redirect('admin_orders')