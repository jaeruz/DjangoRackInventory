from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('register',views.register, name='register'),

    path('adminPanel',views.adminPanel, name='adminPanel'),
    path('adminRack',views.adminRack, name='adminRack'),
    path('racks',views.racks, name='racks'),
    path('addRack',views.addRack, name='addRack'),
    path('rackAddItem',views.rackAddItem, name='rackAddItem'),

    path('userPanel',views.userPanel, name='userPanel'),

    path('inventory',views.inventory, name='inventory'),
    path('addItem',views.addItem, name='addItem'),
    path('editItem',views.editItem, name='editItem'),
    path('deleteItem',views.deleteItem, name='deleteItem'),


]
