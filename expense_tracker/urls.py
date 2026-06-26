from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='expense_home'),
    path('', views.login_view, name='login'),
    path("signup/",views.signup,name="signup"),

    path("delete/<int:id>/", views.delete_expense, name="delete_expense"),
    path("edit/<int:id>/", views.edit_expense, name="edit_expense"),

    path('logout/', views.logout_view, name='logout'),
]