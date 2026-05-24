# cv_builder/urls.py
from django.urls import path
from .views import create_cv, register_view, login_view, logout_view
# cv_builder/urls.py
from .views import create_cv, register_view, login_view, logout_view, generate_pdf, all_cvs_view, cv_detail_view, delete_cv_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('builder/', create_cv, name='create_cv'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # ... existing paths ...
    path('download-pdf/', generate_pdf, name='generate_pdf'),
    path('all-cvs/', all_cvs_view, name='all_cvs'),
    path('cv/<int:pk>/', cv_detail_view, name='cv_detail'),
    path('cv/delete/<int:pk>/', delete_cv_view, name='delete_cv'),

    # ... your existing paths ...
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]