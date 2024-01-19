from django.urls import path
from accounts import views
import allauth.account.views as ahv

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
    path('signup/', views.SignupView.as_view(), name='account_signup'),

    path('password_reset/', views.ResetPassword.as_view(), name='reset_password'),
    path('password_reset_done/', views.ResetPasswordSent.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.ResetPasswordConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', views.ResetPasswordComplete.as_view(), name='password_reset_complete'),

]