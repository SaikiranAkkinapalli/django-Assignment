from django.urls import path
from . import views
urlpatterns = [
    path('',views.home),
    path('addType',views.addFoodType),
    path('addItem',views.addItem),
    path('addTable',views.addTable),
    path('addmanager',views.addManager),
    path('customer',views.customer),
    path('verifyTableAvailability',views.tableAvailability),
    path('order',views.orderrecieve),
    path('checkout',views.checkout),
    path('signup',views.signup),
    path('logout',views.loggingout),
]