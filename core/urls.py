
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from cv_builder.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cv_builder.urls')),
    path('', home_view, name='home'),
    # Add this to redirect the homepage to your CV builder
    path('', lambda request: redirect('create_cv')),
]
