from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def reviews_list(request: HttpRequest) -> HttpResponse:
    pass

def review_detail(request: HttpRequest,id: int) -> HttpResponse:
    pass

def create_review(request: HttpRequest) -> HttpResponse:
    pass

def edit_review(request: HttpRequest,id: int) -> HttpResponse:
    pass

def delete_review(request: HttpRequest,id: int) -> HttpResponse:
    pass

def like_review(request: HttpRequest,id: int) -> HttpResponse:
    pass