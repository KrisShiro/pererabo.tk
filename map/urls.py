from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),

    # API layer
    # Places
    path('delete_place/<int:place_id>/', views.delete_place, name='delete_place'),
    path('add_place/', views.add_place, name='add_place'),
    path('edit_place/<int:place_id>/', views.edit_place, name='edit_place'),

    # Proposals
    path('add_proposal/', views.add_proposal, name='add_proposal'),
    path('approve_proposal/<int:proposal_id>/', views.approve_proposal, name='approve_proposal'),
    path('disapprove_proposal/<int:proposal_id>/', views.disapprove_proposal, name='disapprove_proposal'),
]

