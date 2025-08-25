from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
import uuid

class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class PizzaCategory(BaseModel):
    category_name = models.CharField(max_length=100)

class Pizza(BaseModel):
    category = models.ForeignKey(PizzaCategory,on_delete=models.CASCADE,related_name='pizzas')
    pizza_name = models.CharField(max_length=100)
    pizza_price = models.IntegerField(default=100)
    images = models.ImageField(upload_to='pizzas/')


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,related_name="carts")
    is_paid=models.BooleanField(default=False)
    discount_amount = models.FloatField(default=0)
    applied_coupon = models.CharField(max_length=50, blank=True, null=True)

    def get_cart_total(self):
     total = CartItem.objects.filter(cart=self).aggregate(Sum('pizza__pizza_price'))['pizza__pizza_price__sum']
     return total if total is not None else 0
    
    def apply_coupon(self,coupon_code):
        coupons={
            "PIZZA10": 10,   
            "PIZZA20": 20, 
            "WELCOME50": 50
        }
        total_price = self.get_cart_total()
        code = coupon_code.upper()
        if code in coupons:
            discount = total_price*(coupons[code]/100)
            self.discount_amount = discount
            self.applied_coupon = code
            self.final_total = total_price - discount
            self.save()
            return discount, True, code
        else:
            return 0,False, code


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    pizza = models.ForeignKey(Pizza,on_delete=models.CASCADE)


class Wishlist(BaseModel):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="wishlist")
    pizza = models.ForeignKey(Pizza,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user','pizza')

    def __str__(self):
        return f"{self.user.username}-{self.pizza.pizza_name}"