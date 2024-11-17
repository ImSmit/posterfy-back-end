from django.http import JsonResponse


def index():
    return JsonResponse({"message": "Hello World"})
