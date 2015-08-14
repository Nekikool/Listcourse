#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from ingredient.models import Category, SubCategory, Product, List, ProductInList
from ingredient.forms import AddProductToListForm,CreateListForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import json
from django.core import serializers

############## Page d'accueil ##############

def home(request):
	categories = Category.objects.all()
	sousCategories = SubCategory.objects.all()
	

	return render(request, 'ingredient/home.html', locals())

##########################################	

############## Page List ##############

def listView(request):
	
    ingredients = Product.objects.all()
    form = CreateListForm()
    if request.user.is_authenticated():
        if List.objects.filter(user=request.user).filter(used=True).exists():
            myList = List.objects.filter(user=request.user).filter(used=True)[0]
            myProduct = ProductInList.objects.filter(listUser = myList)
	return render(request, 'ingredient/listView.html',locals())

# Création d'une liste
def createList(request):
    if request.method == 'POST':
        form = CreateListForm(request.POST)
        if form.is_valid():
            #Si on avait une liste en cours, on la set en inutilisé
            if List.objects.filter(pk=request.session.get('currentList',-1)).exists():
                oldList = List.objects.get(pk=request.session.get('currentList'))
                oldList.used = 0
                oldList.save()
            currentList = form.save(commit=False)
            currentList.user = request.user
            currentList.save()
            messages.success(request, request.session.get('currentList'))
            request.session['currentList'] = currentList.id
        else:
            messages.warning(request, 'Une erreur s\'est produite')

    return redirect(reverse(listView))

# Ajout d'un produit à sa liste
def addProductToList(request):

    currentList = None
    response_dict = {}        
    if request.user.is_authenticated() and List.objects.filter(user=request.user).filter(used=True).exists():
        currentList = List.objects.filter(user=request.user).filter(used=True)[0];
    

        if request.POST.has_key('productId'):
            productId = request.POST['productId']
            quantity= request.POST['quantity']
            try:
                 
                if ProductInList.objects.filter(product__id=productId).filter(listUser=currentList).exists():
                    productList= ProductInList.objects.filter(product__id=productId).filter(listUser=currentList)[0]
                    productList.quantity = int(quantity)+int(productList.quantity)
                    productList.save() 
                    response_dict.update({'state':'success','productId': productId,'quantity':quantity})  
                else:
                    product = Product.objects.get(pk = productId) 
                    ProductInList.objects.create(product=product, quantity=quantity, listUser=currentList)             
                    response_dict.update({'state':'success','productId': productId,'quantity':quantity, 'name':product.name, 'category':product.subCategory.category.name,'subCategory':product.subCategory.name})  
                                                                                
            except:
                response_dict= {'state':'error','errorMessage':'Une erreur s\'est produite'}
            

    else:
        response_dict.update({'state':'error','errorMessage': 'Vous devez créer une liste'})  
    return HttpResponse(json.dumps(response_dict), content_type='application/json')

# Delete product from list

def removeProductList(request):
    currentList = None
    response_dict = {}        
    if request.user.is_authenticated() and List.objects.filter(user=request.user).filter(used=True).exists():
        currentList = List.objects.filter(user=request.user).filter(used=True)[0];

        if request.GET['productId']:
            productId = request.GET['productId']
            try:
                if ProductInList.objects.filter(product__id=productId).filter(listUser=currentList).exists():
                    ProductInList.objects.filter(product__id=productId).filter(listUser=currentList).delete()
                    response_dict.update({'state':'success','productId': productId})
                else:
                    response_dict= {'state':'error','errorMessage':'Une erreur s\'est produite'}
            except:
                response_dict= {'state':'error','errorMessage':'Une erreur s\'est produite'}
        else:
            response_dict.update({'state':'error','errorMessage': 'VUne erreur s\'est produite'})  
    return HttpResponse(json.dumps(response_dict), content_type='application/json')


#######################################################

############## Page MyList ##############

def myListsView(request):

    if request.user.is_authenticated() and  List.objects.filter(user=request.user).exists():
        myLists = List.objects.filter(user=request.user).order_by('date')
        productInlist = []
        for myList in myLists:
            if ProductInList.objects.filter(listUser=myList).exists():
                productInlist.append(ProductInList.objects.filter(listUser=myList))

    return render(request, 'ingredient/myLists.html', locals())