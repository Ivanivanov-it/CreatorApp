from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView
from rest_framework.generics import ListAPIView

from common.mixins import CreatorOrModeratorMixin
from enemies.forms import EnemySearchForm, EnemyEditForm, EnemyCreateForm
from enemies.models import Enemy
from enemies.serializers import EnemySerializer


# Create your views here.




class EnemiesListView(ListView):
    model = Enemy
    template_name = 'enemies/enemies_page.html'
    context_object_name = 'enemies'
    paginate_by = 9
    ordering = ['name']


    def get_queryset(self):
        queryset = super().get_queryset().select_related('card_theme')
        self.search_form = EnemySearchForm(self.request.GET or None)

        if 'query' in self.request.GET and self.search_form.is_valid():
            query = self.search_form.cleaned_data['query']
            queryset = queryset.filter(Q(name__icontains=query) | Q(title__icontains=query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        context['page_title'] = "Enemies"

        return context


def enemy_detail(request: HttpRequest, pk: int) -> HttpResponse:
    enemy = get_object_or_404(Enemy, pk=pk)
    context = {
        'page_title': f"{enemy.name} Details",
        'enemy': enemy,
    }

    return render(request, 'enemies/enemy_page.html', context)

class EnemyDetailView(DetailView):
    model = Enemy
    template_name = 'enemies/enemy_page.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{self.object.name} Details"
        context['can_modify'] = (
                self.request.user == self.object.creator or
                self.request.user.groups.filter(name="Moderators").exists()
        )
        return context


class CreateEnemyView(LoginRequiredMixin,CreateView):
    form_class = EnemyCreateForm
    success_url = reverse_lazy('enemies:enemies_list')
    template_name = 'enemies/create_enemy.html'
    extra_context = {
        'page_title': "Create Enemy"
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self,form):
        form.instance.creator = self.request.user
        return super().form_valid(form)



class EditEnemyView(LoginRequiredMixin,CreatorOrModeratorMixin,UpdateView):
    model = Enemy
    form_class = EnemyEditForm
    success_url = reverse_lazy('enemies:enemies_list')
    template_name = 'enemies/edit_enemy.html'
    extra_context = {
        'page_title': "Edit Enemy"
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs




class EnemyDeleteView(LoginRequiredMixin,CreatorOrModeratorMixin,DeleteView):
    model = Enemy
    template_name = 'common/delete_confirm.html'
    success_url = reverse_lazy('enemies:enemies_list')

class EnemyListApiView(ListAPIView):
    serializer_class = EnemySerializer
    queryset = Enemy.objects.select_related('creator').prefetch_related('weakness').all()