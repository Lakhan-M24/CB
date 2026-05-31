from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_loan, name='add_loan'),
    path('edit/<int:pk>/', views.edit_loan, name='edit_loan'),
    path('delete/<int:pk>/', views.delete_loan, name='delete_loan'),
    path('pending/', views.pending_summary, name='pending_summary'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/delete/<int:uid>/', views.delete_user, name='delete_user'),
]
