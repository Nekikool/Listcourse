from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'Listcourse.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accueil/$', 'ingredient.views.home', name="accueil"),
    url(r'^liste/$','ingredient.views.listView', name="liste"),
    url(r'^login/$','member.views.loginView', name='login'),
    url(r'^logout/$', 'member.views.logoutView', name="logout"),
    url(r'^addProductToList/$','ingredient.views.addProductToList', name='addProductToList'),
    url(r'^removeProductList/$','ingredient.views.removeProductList', name='removeProductList'),
    url(r'^createList/$','ingredient.views.createList', name='createList'),
    url(r'^myLists/$','ingredient.views.myListsView', name='myLists'),
    url(r'^saveCurrentList/(?P<listId>[0-9]+)/$','ingredient.views.saveCurrentList', name='saveCurrentList'),


]
