from django.db import models



# Create your models here.

class Register(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    Category_name = models.CharField(max_length=20)

    def __str__(self):
            return self.Category_name
    

class products(models.Model):
    Product_category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    Product_name = models.CharField(max_length=100)
    Product_price = models.BigIntegerField()
    Product_description = models.TextField()
    Product_stock = models.BigIntegerField()
    Product_image = models.ImageField(upload_to='product_image')

    
    def __str__(self):
        return self.Product_name

class Cart(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    product =  models.ForeignKey(products,on_delete=models.CASCADE)
    price = models.BigIntegerField()
    quantity = models.BigIntegerField()


class orders(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    product =  models.ForeignKey(products,on_delete=models.CASCADE)
    price = models.BigIntegerField()
    quantity = models.BigIntegerField()
    address = models.TextField()
    status = models.CharField(max_length=20, default ='pending')