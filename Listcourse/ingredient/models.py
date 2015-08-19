from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(null=True)

class SubCategory(models.Model):
	name = models.CharField(max_length=100)
	category = models.ForeignKey(Category, primary_key=False) 
	description = models.TextField(null=True)
	

class Product(models.Model):
   name = models.CharField(max_length=100)
   description = models.TextField(null=True)
   subCategory = models.ForeignKey(SubCategory, primary_key=False)
   perso = models.BooleanField(default=True)
   user = models.ForeignKey(User, null=True)

class List(models.Model):
	name = models.CharField(max_length=255, null=True)
	user = models.ForeignKey(User, primary_key=False)
	used = models.BooleanField(default=True)
	date = models.DateField(auto_now_add=True)     

class ProductInList(models.Model):
	product = models.ForeignKey(Product)
	quantity = models.IntegerField(default=1)
	listUser = models.ForeignKey(List)
	
	class Meta:
		unique_together = (('product', 'listUser'),)