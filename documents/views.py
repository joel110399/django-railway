from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@csrf_exempt 
def mi_vista1(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            context = {
                # "id_cedula": data['id_cedula'],
                # "nombres": data['nombres'],
                # "nacionalidad": data['nacionalidad'],
            }
            return render(request, '1.html', context)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Los datos no están en formato JSON'}, status=400)
@csrf_exempt
def mi_vista2(request):
     if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)

            context = {
                "id_cedula": data['id_cedula'],
                "nombres": data['nombres'],
                "nacionalidad": data['nacionalidad'],
            }
            return render(request, '2.html', context)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Los datos no están en formato JSON'}, status=400)
@csrf_exempt
def mi_vista4(request):
      if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)

            context = {
                "id_cedula": data['id_cedula'],
                "nombres": data['nombres'],
                "nacionalidad": data['nacionalidad'],
            }
            return render(request, '4.html', context)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Los datos no están en formato JSON'}, status=400)

@csrf_exempt
def mi_vista5(request):
      if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)

            context = {
                "id_cedula": data['id_cedula'],
                "nombres": data['nombres'],
                "nacionalidad": data['nacionalidad'],
            }
            return render(request, '5.html', context)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Los datos no están en formato JSON'}, status=400)
