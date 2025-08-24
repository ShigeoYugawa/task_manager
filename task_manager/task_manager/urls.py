# task_manager/task_manager/urls.py

from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")), 
    path('tasks/', include('tasks.urls')),

    # トップページ
    path('', accounts_views.home_view, name='home'),   
]
