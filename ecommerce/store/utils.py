import json
from .models import *
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = [] 
    order = {'get_cart_total':0,'get_total_count':0,'shipping':False}
    
    for item in cart:
        try:
            product = Product.objects.get(id=item)
            quantity = cart[item]['quantity']
            order['get_total_count']+= quantity
            order['get_cart_total']+= product.price*quantity
            items.append({'product':product,'quantity': quantity,'get_total':order['get_cart_total']})
            if product.digital==False:
                order['shipping'] = True
        except:
            pass
    return {'items':items,'order':order}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        cart=cookieCart(request)
        order = cart['order']
        items = cart['items']
    return items,order
def guestOrder(request,data):
        name=data['form']['name']
        email=data['form']['email']
        items= cookieCart(request)['items']
        customer,created = Customer.objects.get_or_create(
            email=email,
        )
        customer.name=name
        customer.save()
        order = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )

        for item in items:
            product= Product.objects.get(id=item['product'].id)
            orderitem = OrderItem.objects.create(
                order=order[0],
                product=product,
                quantity = item['quantity']
            )
        return customer,order[0]