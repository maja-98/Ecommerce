
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True, blank=True ) 
    feature1= models.CharField(max_length=200,null=True,blank=True)
    feature2= models.CharField(max_length=200, null=True,blank=True)
    feature3= models.CharField(max_length=200, null=True,blank=True)
    feature4= models.CharField(max_length=200, null=True,blank=True)
    description= models.TextField(max_length=1000, null=True,blank=True)
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
            
        except:
            url= '/images/placeholder.png'
        return url 
    
    @property
    def productId(self):
        return str(self.id).rjust(5,'0')
            

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete= models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(default=datetime.now())
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null = True)
    
    def __str__(self):
        return str(self.transaction_id)
    
    @property
    def shipping(self):
        for item in self.orderitem_set.all():
           if item.product.digital==False:
               return True
        return False
    
    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        return sum([item.get_total for item in order_items])
    
    @property
    def get_total_count(self):
        order_items = self.orderitem_set.all()
        return sum([item.quantity for item in order_items])
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(default=datetime.now())
    @property
    def get_total(self):
        return self.product.price * self.quantity  
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete= models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200 , null=False)
    city = models.CharField(max_length=200 , null=False)
    state = models.CharField(max_length=200 , null=False)
    zipcode = models.CharField(max_length=200 , null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address