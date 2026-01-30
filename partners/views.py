from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def partners_list(request: HttpRequest) -> HttpResponse:
    pass

def partner_detail(request: HttpRequest,id: int) -> HttpResponse:
    pass

def create_partner(request: HttpRequest) -> HttpResponse:
    pass

def edit_partner(request: HttpRequest,id: int) -> HttpResponse:
    pass

def delete_partner(request: HttpRequest,id: int) -> HttpResponse:
    pass