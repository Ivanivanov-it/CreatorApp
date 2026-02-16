from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from enemies.forms import EnemySearchForm, EnemyEditForm, EnemyCreateForm
from enemies.models import Enemy


# Create your views here.


def enemies_list(request: HttpRequest) -> HttpResponse:
    search_form = EnemySearchForm(request.GET or None)

    enemies = Enemy.objects.all()

    if 'query' in request.GET:
        if search_form.is_valid():
            enemies = enemies.filter(Q(name__icontains=search_form.cleaned_data['query']) | Q(
                title__icontains=search_form.cleaned_data['query']))

    context = {
        'page_title': "Enemies",
        'enemies': enemies,
        'search_form': search_form
    }

    return render(request, 'enemies/enemies_page.html', context)

def enemy_detail(request: HttpRequest, pk: int) -> HttpResponse:
    enemy = get_object_or_404(Enemy, pk=pk)
    context = {
        'page_title': f"{enemy.name} Details",
        'enemy': enemy,
    }

    return render(request, 'enemies/enemy_page.html', context)

def create_enemy(request: HttpRequest) -> HttpResponse:
    form = EnemyCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        return redirect('enemies:enemies_list')

    context = {
        'page_title': "Create Enemy",
        'form': form,
    }

    return render(request, 'enemies/create_enemy.html', context)

def edit_enemy(request: HttpRequest, pk: int) -> HttpResponse:
    enemy = get_object_or_404(Enemy, pk=pk)
    form = EnemyEditForm(request.POST or None, instance=enemy)

    if request.method == "POST" and form.is_valid():
        form.save()

        return redirect('enemies:enemies_list')

    context = {
        'page_title': "Edit Enemy",
        'form': form,
    }

    return render(request, 'enemies/edit_enemy.html', context)

def delete_enemy(request: HttpRequest, pk: int) -> HttpResponse:
    enemy = get_object_or_404(Enemy, pk=pk)

    if enemy:
        enemy.delete()

    return redirect('enemies:enemies_list')

class EnemyDeleteView(DeleteView):
    model = Enemy
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('enemies:enemies_list')
