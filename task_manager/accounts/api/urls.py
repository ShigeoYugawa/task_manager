# task_manager/accounts/api/urls.py

from django.urls import path
from . import views

app_name = "accounts_api"

urlpatterns = [
    path("", views.accounts_root_api, name="root"),
    path("profile/", views.profile_api, name="profile"),
]
