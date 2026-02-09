from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.


def enemies_list(request: HttpRequest) -> HttpResponse:
    ...

def enemy_detail(request: HttpRequest, id: int) -> HttpResponse:
    ...

def edit_enemy(request: HttpRequest, id: int) -> HttpResponse:
    ...

def delete_enemy(request: HttpRequest, id: int) -> HttpResponse:
    ...

def create_enemy(request: HttpRequest, id: int) -> HttpResponse:
    ...