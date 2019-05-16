from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),

    # API layer
    path('delete_place/<int:place_id>/', views.delete_place, name='delete_place'),
    path('add_place/', views.add_place, name='add_place'),
]

