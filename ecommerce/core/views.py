from django.shortcuts import render,redirect
from core.forms import *
from django.contrib import messages
from core.models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import CategoryForm
from .models import Category

from .models import Contact

from django.core.mail import send_mail

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


# import os
# from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# from django.contrib.staticfiles import finders

import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_SECRET))

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request,'core/index.html',{'products':products})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print('true')
            form.save()
            print('data added successfully')
            messages.success(request,'product added successfully')
            return redirect('/')
        else:
            print("not working")
            messages.info(request,"product is not added,Try Again")
    else:
        form = ProductForm()
    return render(request,'core/add_product.html',{'form':form})

def product_desc(request,pk):
    #get a perticular product of id=pk
    product=Product.objects.get(pk=pk)
    return render(request,'core/product_desc.html',{'product':product})

def add_to_cart(request,pk):
    product=Product.objects.get(pk=pk)
    #create an order item
    order_item,created=Orderitem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )
    #get query set of order object of perticuar user
    
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk= pk).exists():
            order_item.quantity+=1
            order_item.save()
            messages.info(request,"added quantity item")
            return redirect("product_desc",pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request,"item added to cart")
            return redirect("product_desc",pk=pk)
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"item added to cart")
        return redirect("product_desc",pk=pk)
    
    
    

def orderlist(request):
    if Order.objects.filter(user=request.user,ordered=False).exists():
        order=Order.objects.get(user=request.user,ordered=False)
        return render(request,'core/orderlist.html',{'order':order})
    return render(request,'core/orderlist.html',{'message':'your cart is empty'})
        
    

def add_item(request,pk):
    product=Product.objects.get(pk=pk)
    #create an order item
    order_item,created=Orderitem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )
    #get query set of order object of perticuar user
    
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk= pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity+=1
                order_item.save()
                messages.info(request,"Added quantity item")
                return redirect("orderlist")
            else:
                message.info(request,'sorry! Product is out of stock')
                return redirect('orderlist')
            
        else:
            order.items.add(order_item)
            messages.info(request,"item added to cart")
            return redirect("product_desc",pk=pk)
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"item added to cart")
        return redirect("product_desc",pk=pk)
    
def remove_item(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item=Orderitem.objects.filter(
                product=item,
                user=request.user,
                ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request,'Item Quantity Was Updated')
            return redirect("orderlist")
        else:
            messages.info(request,'This Item Is Not In Your Cart')
            
            return redirect("orderlist")
    else:
        messages.info(request,'You Do Not Have Any Order')
        return redirect("orderlist")

# def checkout_page(request):
#     if CheckoutAddress.objects.filter(user=request.user).exists():
#         return render(request,'core/checkout_address.html',{'payment_allow':"allow"})
#     if request.method =='POST':
#         form=CheckoutForm(request.POST)
#         if form.is_valid():
#             street_address=form.cleaned_data.get('street_address')
#             apartment_address=form.cleaned_data.get('apartment_address')
#             country=form.cleaned_data.get('country')
#             zip_code=form.cleaned_data.get('zip_code')
                
                
#             checkout_address= CheckoutAddress(
#             user=request.user,
#             street_address=street_address,
#             apartment_address=apartment_address,
#             country=country,
#             zip_code=zip_code,
#             )
#             checkout_address.save()
#             print('it should render the summary page')
#             return render(request,'core/checkout_address.html',{'payment_allow':"allow"})
#         else:
#             messages.warning(request,'failed checkout')
#             return redirect('checkout_page')
#     else:
#         form=CheckoutForm()
#         return render(request,'core/checkout_address.html',{'form':form})    

def checkout_page(request):
    if CheckoutAddress.objects.filter(user=request.user).exists():
        return render(request,'core/checkout_address.html',{'payment_allow':"allow"})
    if request.method =='POST':
        form=CheckoutForm(request.POST)
        if form.is_valid():
            street_address=form.cleaned_data.get('street_address')
            apartment_address=form.cleaned_data.get('apartment_address')
            country=form.cleaned_data.get('country')
            zip_code=form.cleaned_data.get('zip_code')
                
                
            checkout_address= CheckoutAddress(
            user=request.user,
            street_address=street_address,
            apartment_address=apartment_address,
            country=country,
            zip_code=zip_code,
            )
            checkout_address.save()
            print('it should render the summary page')
            return render(request,'core/checkout_address.html',{'payment_allow':"allow"})
        else:
            messages.warning(request,'failed checkout')
            return redirect('checkout_page')
    else:
        form=CheckoutForm()
        return render(request,'core/checkout_address.html',{'form':form})
    
def payment(request):
    try:
        order=Order.objects.get(user=request.user,ordered=False)
        address=CheckoutAddress.objects.get(user=request.user)
        order_amount=order.get_total_price()
        order_currency="INR"
        order_receipt=order.order_id
        notes={
            "street_address":address.street_address,
            "apartment_address":address.apartment_address,
            "country":address.country,
            "zip_code":address.zip_code,
            
        }
        razorpay_order=razorpay_client.order.create(
            dict(
                amount=order_amount * 100,
                currency=order_currency,
                receipt=order_receipt,
                notes=notes,
                payment_capture="0",
            )
        )
        print(razorpay_order["id"])
        order.razorpay_order_id = razorpay_order["id"]
        order.save()
        print("it should render the summary page")
        return render(request,"core/paymentsummaryrazorpay.html",{
            "order": order,
            "order_id": razorpay_order["id"],
            "orderId": order.order_id,
            "final_price": order_amount,
            "razorpay_merchant_id": settings.RAZORPAY_ID,
            
        },)
    except Order.DoesNotExist:
        print("order not found")
        return HttpResponse("404 Error")
@csrf_exempt  
def handlerequest(request):
    if request.method =="POST":
        try:
            payment_id=request.POST.get('razorpay_payment_id','')
            order_id=request.POST.get('razorpay_order_id','')
            signature=request.POST.get('razorpay_signature','')
            print(payment_id,order_id,signature)
            params_dict={
                'razorpay_order_id':order_id,
                'razorpay_payment_id':payment_id,
                'razorpay_signature':signature,

            }
            try:
                order_db=Order.objects.get(razorpay_order_id=order_id)
                print("order found")
            except:
                print('order not found')
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id= payment_id
            order_db.razorpay_signature= signature
            order_db.save()
            print("working......")
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not  None:
                print("working final fine......")
                amount=order_db.get_total_price()
                amount=amount * 100
                payment_status=razorpay_client.payment.capture(payment_id,amount)
                if payment_status is not None:
                    print(payment_status)
                    order_db.ordered=True
                    order_db.save()
                    for item in order_db.items.all():
                        item.product.product_available_count -= item.quantity
                        item.product.save()
                    print("payment Success")
                    checkout_address=CheckoutAddress.objects.get(user=request.user)
                    request.session[
                        "order_complete"
                    ] = "your order is successfully placed,you will receive your order within 5-7 day "
                    # request.session["order_id"]=order_id
                    # request.session["payment_status"]=payment_status
                    return render(request,"core/invoice.html",{'order':order_db,'payment_status':payment_status,'checkout_address':checkout_address})
                    # return redirect("render_pdf_view")
                else:
                    print("payment failed")
                    order_db.ordered=False
                    order_db.save()
                    request.session[
                        "order_failed"
                    ]="unfortunately your order could not be placed ,try again !"
                    return redirect("/")
            else:
                order_db.ordered=False
                order_db.save()
                return render(request,"core/paymentfailed.html")
        except:
            return HttpResponse("Error occured")

def invoice(request):
    
    return render(request,"core/invoice.html")

# def render_pdf_view(request):
#     order_id=request.session["order_id"]
#     order_db=Order.objects.get(razorpay_order_id=order_id)
#     checkout_address=CheckoutAddress.objects.get(user=request.user)
#     amount=order_db.get_total_price()
#     amount=amount * 100
#     payment_id=order_db.razorpay_payment_id
#     payment_status=request.session["payment_status"]
#     template_path = 'core/invoice.html'
#     context = {
#         'order':order_db,'payment_status':payment_status,'checkout_address':checkout_address
#     }
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response)
#     # if error then show some funny view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response

def contact_view(request):
    contacts = Contact.objects.all()
    for c in contacts:
        print(c.id)
    return render(request, 'core/seeadmin.html', {'contacts': contacts})
# def contact_list(request):
#     contacts = Contact.objects.all()
#     return render(request, 'core/seeadmin.html', {'contacts': contacts})


def sentmsg(request, id):
    if request.method == 'POST':
        user_email = request.user.email
        print(user_email)# Get the current user's email
        contact = get_object_or_404(Contact, id=id)  # Retrieve contact object using its id
        recipient_email = contact.email
        print(recipient_email)# Get recipient's email from the contact object
        message = request.POST.get('message')  # Get the message from the form

        # Send email
        send_mail(
            'Subject of the email',  # Subject of the email
            message,  # Message content
            user_email,  # Sender's email address
            [recipient_email],  # Recipient's email address(es)
            fail_silently=False,  # Set to True to suppress exceptions
        )
        
        return HttpResponse('Message sent successfully!')

        # Optionally, you can add additional logic here, such as redirecting the user
        # to a different page after sending the email
    else:
        # Handle the case where the request method is not POST
        return render(request, 'core/sentmsg.html')
def add_category(request):
    if request.method == 'POST':
        form =CategoryForm(request.POST)
        if form.is_valid():
            print('true')
            form.save()
            print('data added successfully')
            messages.success(request,'product category added successfully')
            return redirect('/')
        # else:
        #     print("not working")
        #     messages.info(request,"category is not added,Try Again")
    else:
        form =CategoryForm()
        return render(request,'core/add_category.html',{'form':form})
# else:
    #     form =CategoryForm()
    return render(request,'core/index.html',{'form':form})
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format')
            return render(request, 'core/contact.html')

        # Validate other fields as needed (e.g., checking if they are not empty)

        # Create Contact object if all validations pass
        try:
            contact = Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
        except Exception as e:
            messages.error(request, f'Error creating contact: {str(e)}')
            return render(request, 'core/contact.html')

        messages.success(request, 'Your message has been sent. Thank you!')
        return redirect('/')
    else:
        return render(request, 'core/contact.html')
    
    
    
def productview(request):
    products = Product.objects.all()
    for c in products:
        print(c.id)
    return render(request, 'core/deleteproduct.html', {'products': products})

def deletepro(request,product_id):
    product=Product.objects.get(id=product_id)
    product.delete()
    print("product is deleted")
    return redirect("productview")

def update_product(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    print(product.img.url)
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=ProductForm(instance=product)
    return render(request,'core/update.html',{'form':form,'image':product.img.url})
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'core/orderview.html', {'orders': orders})

def order_li(request):
    # Assuming you have a foreign key 'user' in your Order model
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'core/ordercus.html', {'user_orders': user_orders})
    
                
            
            