# task_manager/accounts/api/views.py

from django.http import JsonResponse

def accounts_root_api(request):
    return JsonResponse({"accounts": []})

def profile_api(request):
    return JsonResponse({"accounts": []})