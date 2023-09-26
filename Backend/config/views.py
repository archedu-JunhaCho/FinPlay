from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth import logout as real_logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from dj_rest_auth.views import LogoutView
from rest_framework import status

@method_decorator(csrf_exempt, name='dispatch')
class deleteU(LogoutView):
    def delete(self, request, *args, **kwargs):
        print('삭제할 유저는',request.user)
        request.user.delete()
        response = Response(
            {'detail': ('Successfully delete account.')},
            status=status.HTTP_200_OK,
        )
        return response