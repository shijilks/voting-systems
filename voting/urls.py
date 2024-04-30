from django.urls import path 
from . import views 



urlpatterns = [
     path("", views.index, name="index"),
     path("vote/<str:slug>", views.detail, name="detail"),
     path("result/<str:slug>", views.result, name="result"),
     path("result", views.result, name="result"),
     path("signin", views.signin, name= "signin"),
     path('signup/', views.signup, name="signup"),
     path('logout/', views.signout, name="logout"),
     path('edit/<int:item_id>/', views.edit_item, name='edit_item'),  # URL for editing category item
     path('delete/<int:item_id>/', views.delete_item, name='delete_item'), 
     path('update/<int:item_id>/', views.update_item, name='update_item'),

      
]