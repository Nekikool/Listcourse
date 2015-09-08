#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from ingredient.models import Category, SubCategory, Product, List, ProductInList
from ingredient.forms import AddProductToListForm,CreateListForm,AddCustomProductForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import json
from django.core import serializers

############## Useful function ##############

#Get current List
def getCurrentList(request):
    myList = None
    if List.objects.filter(user=request.user).filter(used=True).exists():
        myList = List.objects.filter(user=request.user).filter(used=True)[0]
	
	return myList

##########################################	

############## Page List ##############

def listView(request):
	
    ingredients = Product.objects.all()
    form = CreateListForm()
    productForm = AddCustomProductForm()
    if request.user.is_authenticated():
        myList = getCurrentList(request)
        if myList is not None:
            myProduct = ProductInList.objects.filter(listUser = myList)
	return render(request, 'ingredient/listView.html',locals())

# Création d'une liste
def createList(request):
    if request.method == 'POST':
        form = CreateListForm(request.POST)
        if form.is_valid():
            #Si on avait une liste en cours, on la set en inutilisé
            oldList = getCurrentList(request)
            if oldList is not None:
                oldList.used = False
                oldList.save()
            currentList = form.save(commit=False)
            currentList.user = request.user
            currentList.save()
            messages.success(request, "Votre liste a bien été créée")
        else:
            messages.warning(request, 'Une erreur s\'est produite')

    return redirect(reverse(listView))


#save current list
def saveCurrentList(request, listId):
    myList = getCurrentList(request)
    if myList is not None:
        if int(listId) == int(myList.id):
            myList.used = False
            myList.save()
            messages.success(request, "Votre liste a bien été sauvegardée")
        else:
            messages.warning(request, "Une erreur est survenue")   
    else:
            messages.warning(request, "Une erreur est survenue")   
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


# Add a custom product in the main list and in the user's current list
def addCustomProduct(request):
    if request.method == 'POST':
        form = AddCustomProductForm(request.POST)
        if form.is_valid():
            try:
                product = form.save()
                product.perso = True
                product.user=request.user
                product.save()
                currentList = getCurrentList(request)
                if currentList is not None:
                    ProductInList.objects.create(product=product, quantity=1, listUser=currentList)
                messages.success(request, "Votre produit a bien été ajouté")
            except:
                messages.warning(request, 'Une erreur s\'est produite')
        else:
            messages.warning(request, 'Une erreur s\'est produite')
    return redirect(reverse(listView)) 


def deleteCustomProduct(request,productId):
    if request.user.is_authenticated() and Product.objects.filter(perso=True).filter(user=request.user).filter(id=productId).exists():
        try:
            Product.objects.filter(perso=True).filter(user=request.user).filter(id=productId)[0].delete()
            messages.success(request, "Votre produit a bien été supprimé")
        except:
            messages.warning(request, "Une erreur s\'est produite")
    else:
        messages.warning(request, 'Une erreur s\'est produite')
    return redirect(reverse(listView))

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

#Remove the select lsit
def deleteList(request, listId):
    if request.user.is_authenticated() and List.objects.filter(user=request.user).filter(id=listId).exists():
        try:
            List.objects.get(user=request.user, id=listId).delete()
            messages.success(request, "La liste a bien été supprimée")
        except:
            messages.warning(request, 'Une erreur s\'est produite')
    else:
        messages.warning(request, 'Une erreur s\'est produite')
    return redirect(reverse(myListsView)) 

#Change the current list
def changeList(request, listId):
    if List.objects.filter(user=request.user).filter(id=listId).exists():
        try:
            oldList = getCurrentList(request)
            if oldList is not None:
                oldList.used = False
                oldList.save()
            newList = List.objects.filter(user=request.user).filter(id=listId)[0]
            newList.used = True
            newList.save()

            messages.success(request, "Votre liste actuelle est : "+newList.name)
        except:
            messages.warning(request, 'Une erreur s\'est produite')
    else:
        messages.warning(request, 'Une erreur s\'est produite')
    return redirect(reverse(myListsView)) 


#add products of the given list in the current list
def fusionList(request, listId):
    if List.objects.filter(user=request.user).filter(id=listId).exists():
        currentList = getCurrentList(request)
        if currentList is not None and ProductInList.objects.filter(listUser_id=listId).exists():
            try:
                productsList = ProductInList.objects.filter(listUser_id=listId)
                for productList in productsList:
                    if ProductInList.objects.filter(listUser=currentList.id).filter(product=productList.product).exists():
                        currentProductList = ProductInList.objects.filter(listUser=currentList.id).filter(product=productList.product)[0]
                        currentProductList.quantity = int(productList.quantity) + int(currentProductList.quantity)
                        currentProductList.save()
                    else:
                        ProductInList.objects.create(product=productList.product, quantity=productList.quantity, listUser=currentList)
                messages.success(request, "La liste a bien été fusionnée")
            except:
                messages.warning(request, 'Une erreur s\'est produite')
        else:
            messages.warning(request, 'Une erreur s\'est produite')

    else:
        messages.warning(request, "Cette liste ne vous appartient pas")

    return redirect(reverse(myListsView)) 