from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from cards.forms import CardForm
from cards.models import Card


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


