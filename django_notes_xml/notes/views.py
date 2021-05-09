import json
import uuid
from xmlrpc.client import ServerProxy, Fault

from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from notes.forms import CreateNoteForm


class CreateNote(View):
    def get(self, request):
        form = CreateNoteForm(initial={'key': 'value'})
        return render(request, 'notes/add_notes.html', {'form': form})

    def post(self, request, *args, **kwargs):
        data = json.load(request)
        try:
            server = ServerProxy('http://localhost:8001/notes')
            result = server.add(data['note'])
        except Fault as e:
            return HttpResponseBadRequest(e.faultString)
        except ConnectionRefusedError as e:
            return HttpResponseServerError(f'XMLRPC {e.strerror}')
        if not result:
            return HttpResponseBadRequest(request)
        return JsonResponse(
            {'uuid': result, 'link': request.build_absolute_uri(reverse('note', args=[result]))})


class DetailNote(View):
    def get(self, request, uuid):
        try:
            server = ServerProxy('http://localhost:8001/notes')
            note = server.get(str(uuid))
        except Fault as e:
            return HttpResponseBadRequest(e.faultString)
        except ConnectionRefusedError as e:
            return HttpResponseServerError(render(request, 'notes/500.html', {'error': e.strerror}))
        if not note:
            return HttpResponseNotFound(render(request, 'notes/404.html'))
        return render(request, 'notes/view_notes.html', {'note': note})
