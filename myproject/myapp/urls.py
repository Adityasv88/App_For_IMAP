from django.urls import path
from . import views  # import views so we can use them in urls.

urlpatterns = [

    path('my-view/', views.my_view, name='my-view'),

]
