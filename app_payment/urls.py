from django.urls import path
from .views import *

urlpatterns = [
    path('', Card, name='index'),
    path('checkout/', Checkout, name='checkout'),
    path('status', Status, name='status'),
]