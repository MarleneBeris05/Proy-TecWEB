from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from crud_escolar_api.serializers import *
from crud_escolar_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json

class EventosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        eventos = Eventos.objects.order_by("id")
        eventos = EventoSerializer(eventos, many=True).data
        #Aquí convertimos los valores de nuevo a un array
        if not eventos:
            return Response({},400)
        for evento in eventos:
            evento["publico"] = json.loads(evento["publico"])

        return Response(eventos, 200)
    

class EventosView(generics.CreateAPIView):
    #Obtener evento por ID
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id = request.GET.get("id"))
        evento = EventoSerializer(evento, many=False).data

        return Response(evento, 200)

    #Registrar nuevo evento
    @transaction.atomic
    def post(self, request, *args, **kwargs):
            #Almacenar los datos del evento
            evento = Eventos.objects.create(nombre_evento = request.data["nombre_evento"],
                                            tipo_evento = request.data["tipo_evento"],
                                            fecha = request.data["fecha"],
                                            hora_inicio = request.data["hora_inicio"],
                                            hora_fin = request.data["hora_fin"],
                                            lugar = request.data["lugar"],
                                            publico = json.dumps(request.data["publico"]),
                                            programa = request.data["programa"],
                                            responsable_id =request.data["responsable_id"],
                                            descripcion = request.data["descripcion"],
                                            cupo_max = request.data["cupo_max"])
            evento.save()

            return Response({"evento_created_id": evento.id }, 201)


class EventosViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.data["id"])
        evento.nombre_evento = request.data["nombre_evento"]
        evento.tipo_evento = request.data["tipo_evento"]
        evento.fecha = request.data["fecha"]
        evento.hora_inicio = request.data["hora_inicio"]
        evento.hora_fin = request.data["hora_fin"]
        evento.lugar = request.data["lugar"]
        evento.publico = json.dumps(request.data["publico"])
        evento.programa = request.data["programa"]
        evento.responsable_id =request.data["responsable_id"]
        evento.descripcion = request.data["descripcion"]
        evento.cupo_max = request.data["cupo_max"]
        evento.save()
        
        a = EventoSerializer(evento, many=False).data

        return Response(a,200)
    
    def delete(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))
        try:
            evento.delete()
            return Response({"details":"Evento eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)