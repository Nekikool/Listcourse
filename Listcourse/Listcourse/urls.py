from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'Listcourse.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^login/$','member.views.loginView', name='login'),
    url(r'^logout/$', 'member.views.logoutView', name="logout"),
    
    url(r'^liste/$','ingredient.views.listView', name="liste"),
    url(r'^addProductToList/$','ingredient.views.addProductToList', name='addProductToList'),
    url(r'^removeProductList/$','ingredient.views.removeProductList', name='removeProductList'),
    url(r'^createList/$','ingredient.views.createList', name='createList'),
    url(r'^liste/saveCurrentList/(?P<listId>[0-9]+)/$','ingredient.views.saveCurrentList', name='saveCurrentList'),

    url(r'^myLists/$','ingredient.views.myListsView', name='myLists'),
    url(r'^myLists/deleteList/(?P<listId>[0-9]+)/$','ingredient.views.deleteList', name='deleteList'),
    url(r'^myLists/changeList/(?P<listId>[0-9]+)/$','ingredient.views.changeList', name='changeList'),
    url(r'^myLists/fusionList/(?P<listId>[0-9]+)/$','ingredient.views.fusionList', name='fusionList'),
    


]
