from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Páginas principais
    path('', views.home, name='home'),
    
    # URLs novas (challenge)
    path('challenges/', views.challenge_list, name='challenge_list'),
    path('challenge/<slug:slug>/', views.challenge_detail, name='challenge_detail'),
    path('challenge/<slug:slug>/run/', views.run_code, name='run_code'),
    path('challenge/<slug:slug>/submit/', views.submit_code, name='submit_code'),
    
    # URLs antigas (problem) - Redirects para compatibilidade
    path('problems/', RedirectView.as_view(pattern_name='challenge_list', permanent=True)),
    path('problem/<slug:slug>/', RedirectView.as_view(pattern_name='challenge_detail', permanent=True)),
    path('problem/<slug:slug>/run/', views.run_code),  # Mantém funcionalidade
    path('problem/<slug:slug>/submit/', views.submit_code),  # Mantém funcionalidade
    
    # Alias para compatibilidade
    path('problem-list/', views.problem_list, name='problem_list'),
    path('problem-detail/<slug:slug>/', views.problem_detail, name='problem_detail'),
    
    # Autenticação
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Perfil e submissões
    path('profile/', views.user_profile, name='profile'),
    path('submission/<int:submission_id>/', views.submission_detail, name='submission_detail'),
]

