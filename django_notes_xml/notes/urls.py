from django.urls import path

from .views import CreateNote, DetailNote

urlpatterns = [
    path('', CreateNote.as_view(), name='index'),
    path('note/<uuid:uuid>', DetailNote.as_view(), name='note'),
]
