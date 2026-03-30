from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from cards.forms import CardForm, CardEditForm
from cards.models import Card
from common.mixins import CreatorOrModeratorMixin


# Create your views here.

class CardListView(ListView):
    model = Card
    template_name = 'cards/cards_page.html'
    context_object_name = 'cards'
    paginate_by = 9
    ordering = ['name']
    extra_context = {
        'page_title': 'Cards',
    }

class CardCreateView(LoginRequiredMixin,CreateView):
    template_name = 'cards/create_card.html'
    form_class = CardForm
    success_url = reverse_lazy('cards:cards_list')
    extra_context = {
        'page_title': 'Create Card',
    }

    def form_valid(self,form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class CardDetailView(DetailView):
    template_name = 'cards/card_page.html'
    model = Card


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{self.object.name}  Details"
        context['can_modify'] = (
            self.request.user == self.object.creator or
            self.request.user.groups.filter(name="Moderators").exists()
        )

        return context

class EditCardView(LoginRequiredMixin,CreatorOrModeratorMixin,UpdateView):
    model = Card
    form_class = CardEditForm
    success_url = reverse_lazy('cards:cards_list')
    template_name = 'cards/edit_card.html'
    extra_context = {
        'page_title': "Edit Card"
    }



class CardDeleteView(LoginRequiredMixin,CreatorOrModeratorMixin,DeleteView):
    model = Card
    template_name = 'common/delete_confirm.html'
    success_url = reverse_lazy('cards:cards_list')

