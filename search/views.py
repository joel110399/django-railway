from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from supabase_client import get_supabase_client
from utils.cedula_validation import cedula_validation
import xmltodict
import json
import requests

supabase = get_supabase_client()

@csrf_exempt
def search_users(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        type = data['type']
        user = data['user']
        searches = user['user_metadata']['searches']
        searches_performed = user['user_metadata']['searchesPerformed']
        results = []

        print(searches_performed, searches)

        # if searches_performed >= searches:
        #     return JsonResponse({"error": "Alcanzaste el limite de busqueas asignados a tu plan."}, safe=False, status=401)
        
        supabase.table('historico-busqueda').insert({"nombres": data['value'], "user-id": user['id']}).execute()


        if type == "No específico":
            pass
        elif type == "Individuo":
            value = data['value']

            if cedula_validation(value):
                print(11111111111111111)
                print(value[0:3])
                url = f'https://dataportal.jce.gob.do/idcons/IndividualDataHandler.aspx?ServiceID=16ae7f8b-a09d-4956-a167-d5d0807218ba&ID1={value[0:3]}&ID2={value[3:10]}&ID3={value[10:]}'
                response = requests.get(url)

                xml_data = response.text
                json_data = xmltodict.parse(xml_data)
                print("Received data in JSON format:", json_data)

                table_criteria_map = {
                    'cedulados': "id_cedula",
                }

                for table, criteria in table_criteria_map.items():
                    response = supabase.table(table).select('*').eq(criteria, value).execute()

                    if response.data:  # Check if there's any data in the response
                        for item in response.data:
                            item['nombres'] = item['nombre_completo']
                        results.extend(response.data)  # Agregar los resultados a la lista


                if "root" in json_data:  # Check if there's any data in the response
                    print(2222222222222222)
                    print(json_data["root"])

                    res = supabase.table('junta').insert({"nombres": json_data['root']['nombres'], "apellido1": json_data['root']['apellido1'], "apellido2": json_data['root']['apellido2']}).execute()
                    print(res.data)
                    
                    results.extend(res.data)  # Agregar los resultados a la lista
            else:
                print(2222222222222222)
                # Definir un diccionario que mapee el nombre de la tabla con el criterio de búsqueda correspondiente
                table_criteria_map = {
                    'cedulados': "nombre_completo",
                    'DB2PEP': "Nombres",
                    'DB212ERPEP': "Nombres PEP",
                }

                for table, criteria in table_criteria_map.items():
                    print(table, criteria)
                    response = supabase.table(table).select('*').text_search(criteria, value).execute()

                    if response.data:  # Check if there's any data in the response
                        for item in response.data:
                            item['nombres'] = item[criteria]
                        results.extend(response.data)  # Agregar los resultados a la lista

        elif type == "Empresa":
            pass
        elif type == "Pasaporte":
            pass

        if results:  # Si hay resultados, retornarlos

            supabase.table('reports').insert({"type": 'MATCH', "user-id": user['id'], "data": results, "value": value}).execute()

            return JsonResponse(results, safe=False, status=200)
        else:  # Si no hay resultados, retornar una respuesta vacía
            return JsonResponse([], safe=False, status=200)


@csrf_exempt
def get_history(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['user']

        response = supabase.table("historico-busqueda").select('*').eq("user-id", user['id']).execute()

        return JsonResponse(response.data, safe=False, status=200)

@csrf_exempt
def get_children(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['user']

        response = supabase.auth.admin.list_users()

        return JsonResponse(response.data, safe=False, status=200)


@csrf_exempt
def register_client(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['user']

        print(data)

        response = supabase.table('client-list').insert({"nombres": data['value']['nombres'], "user-id": user['id']}).execute()

        print(response)
        
        return HttpResponse(status=200)
    
    
@csrf_exempt
def create_child_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['user']
        data = data['data']
        children = user['user_metadata']['children']
        children_limit = user['user_metadata']['children_limit']

        if len(children) >= children_limit:
            return JsonResponse({"error": "Alcanzaste el limite de hijos asignados a tu plan."}, safe=False, status=401)

        try:
            res = supabase.auth.sign_up({'email': data['correo'], 'password': data['contrasena'],  
                'options': {
                    'data': {
                        'name': data['nombre'],
                        'role': 'child',
                        'parent': user['id'],
                        'document_id': data['documento'],
                        # depastamento
                        # cargo
                        'type': 'individual',
                        'plan': user['user_metadata']['plan'],
                        'status': 'inactive',
                        'searches': 0,
                        'searches_performed': 0,
                        'searches_available': 0,
                    }
                }
            })
            
            response = {
                'id': res.user.id,
                'name': data['nombre'],
                'email': res.user.email,
                'role': 'child',
                'parent': user['id'],
                'document_id': data['documento'],
                'type': 'individual',
                'plan': user['user_metadata']['plan'],
                'status': 'inactive',
                'searches': 0,
                'searches_performed': 0,
                'searches_available': 0,
            
            }
            return JsonResponse({'data': response}, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": "Error al crear el usuario"}, safe=False, status=401)
