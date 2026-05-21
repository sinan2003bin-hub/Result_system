from django.urls import path  # type: ignore[import]
from . import views


urlpatterns = [
    path('', views.home, name='core_home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('dashboard/edit/<int:id>/', views.edit_student, name='edit_student'),
]