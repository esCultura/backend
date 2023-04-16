from django.http import JsonResponse
from subprocess import run


def refresh_script(request):
    run(['python', 'manage.py', 'runscript', 'refresh'], check=True)
    return JsonResponse({'message': 'Script refresh executed successfully'})
