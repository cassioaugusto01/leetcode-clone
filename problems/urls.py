from django.urls import path
from . import views

urlpatterns = [
    # Páginas principais
    path('', views.home, name='home'),
    path('problems/', views.problem_list, name='problem_list'),
    path('problem/<slug:slug>/', views.problem_detail, name='problem_detail'),
    
    # Autenticação
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Execução e submissão de código
    path('problem/<slug:slug>/run/', views.run_code, name='run_code'),
    path('problem/<slug:slug>/submit/', views.submit_code, name='submit_code'),
    
    # Perfil e submissões
    path('profile/', views.user_profile, name='profile'),
    path('submission/<int:submission_id>/', views.submission_detail, name='submission_detail'),
]

