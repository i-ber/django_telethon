from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from django_telethon.models import App, ClientSession, LoginStatus
from bot.models import NewDialogs

def _get_data(request):
    if 'application/json' in request.META.get('CONTENT_TYPE', ''):
        data = request.body.decode('utf-8')
        data = json.loads(data)
    else:
        data = request.POST
    return data

# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def new_dialog_view(request):
    try:
        data = _get_data(request)
        phone_number = data.get('phone_number', None)
        client_session_name = data.get('session_name', None)

        if not App.objects.all().exists():
            return JsonResponse({'error': 'No app found'}, status=400)
        if not phone_number or not client_session_name:
            return JsonResponse({'error': 'Missing phone number or client session name'}, status=400)
        try:
            client_session = ClientSession.objects.get(name=client_session_name)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Client session does not exists'}, status=400)

        if client_session.login_status != LoginStatus.LOGIN_DONE:
            return JsonResponse({'error': 'Client session is not in login done status'}, status=400)

        if NewDialogs.objects.filter(phone_number=phone_number, client_session=client_session).exists():
            return JsonResponse({'error': 'Dialog already exist'}, status=400)

        login = NewDialogs.objects.create(client_session=client_session,
                                          phone_number=phone_number,
                                          have_to_start=True)

        return JsonResponse(
            {"message": "Dialog added in queue successfully", "status": "success", "login_id": login.id},
            status=200
        )
    except (KeyError, json.JSONDecodeError) as e:
        return JsonResponse({"message": "Invalid data provided", "status": "error"}, status=400)

