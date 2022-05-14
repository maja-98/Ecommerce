from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from .models import *
import json
from datetime import datetime
from .utils import *
from django.db.models import Q

def debug(*args):
    print('\n')
    print(args)
    print('\n')
# Create your views here.
def store(request):
    q= request.GET.get('q') if request.GET.get('q')!=None else ''
    products = Product.objects.filter(
        Q(name__icontains=q)
    )
    items,order=cartData(request)
    context = {'products':products,'Order':order}
    
    return render(request,'store/store.html',context)

def checkout(request):
    items,order=cartData(request)

    context = {'items':items,'Order':order}
    return render(request,'store/checkout.html',context)

def cart(request):
    items,order=cartData(request)

    context = {'items':items,'Order':order}
    return render(request,'store/cart.html',context)

def productView(request,id):
    items,order=cartData(request)
    id=int(id.lstrip('0'))
    product=Product.objects.get(id=id)
    context = {'product':product,'Order':order}
    
    return render(request,'store/product-view.html',context)
def myOrders(request):
    items,order=cartData(request)
    if request.user.is_authenticated:
        
        orders = Order.objects.filter(customer=request.user.customer,complete=True).order_by('-date_ordered')
        orderitem_queryset=[[order,order.orderitem_set.all()] for order in orders ]
        # orderitems = [orderitem for val in orderitem_queryset for orderitem in val]
        
        context={'orderDict':orderitem_queryset,'Order':order}
        return render(request,'store/my-orders.html',context)
    else:
        return HttpResponse('please log in to view Order history')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId,action)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order , product=product)
    if action=='add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    
    orderItem.save()
    if orderItem.quantity==0:
        orderItem.delete()
    return JsonResponse('Item Was Added',safe=False)

def processOrder(request):
    data = json.loads(request.body)
    transaction_id = round(datetime.now().timestamp()) 
    if request.user.is_authenticated:
        
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)

        

    else:
        customer,order = guestOrder(request,data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if round(float(total),2)== float(order.get_cart_total):
        
        order.complete = True
        order.date_ordered = datetime.now()
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )
    
    return JsonResponse('Payment submitted..', safe=False)