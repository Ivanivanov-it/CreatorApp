from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView
from django.views.generic import TemplateView
from characters.forms import CharacterCreateForm, CharacterEditForm, CharacterSearchForm
from characters.models import Character


# Create your views here.




class LandingPageView(TemplateView):
    template_name = 'characters/landing_page.html'

    extra_context = {
        'page_title': "Home"
    }

class CharactersListView(ListView):
    model = Character
    template_name = 'characters/characters_page.html'
    context_object_name = 'characters'
    paginate_by = 9
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_form = CharacterSearchForm(self.request.GET or None)

        if 'query' in self.request.GET and self.search_form.is_valid():
            query = self.search_form.cleaned_data['query']
            queryset = queryset.filter(Q(name__icontains=query) | Q(title__icontains=query))

        return queryset


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        context['page_title'] = "Characters"
        return context


class CharacterDetailView(DetailView):
    template_name = 'characters/character_page.html'
    model = Character

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{self.object.name} Details"

        return context


class CreateCharacterView(CreateView):
    template_name = 'characters/create_character.html'
    form_class = CharacterCreateForm
    success_url = reverse_lazy('characters:characters_list')
    extra_context = {
        'page_title': "Create Character"
    }

class EditCharacterView(UpdateView):
    model = Character
    form_class = CharacterEditForm
    success_url = reverse_lazy('characters:characters_list')
    template_name = 'characters/edit_character.html'
    extra_context = {
        'page_title': "Edit Character"
    }


class CharacterDeleteView(DeleteView):
    model = Character
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('characters:characters_list')
