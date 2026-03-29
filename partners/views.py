from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView
from rest_framework.generics import ListAPIView

from common.mixins import CreatorOrModeratorMixin
from partners.forms import PartnerCreateForm, PartnerEditForm, PartnerSearchForm
from partners.models import Partner
from partners.serializers import PartnerSerializer


class PartnersListView(ListView):
    model = Partner
    template_name = 'partners/partners_page.html'
    context_object_name = 'partners'
    paginate_by = 9
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('card_theme')
        self.search_form = PartnerSearchForm(self.request.GET or None)

        if 'query' in self.request.GET and self.search_form.is_valid():
            query = self.search_form.cleaned_data['query']
            queryset = queryset.filter(Q(name__icontains=query) | Q(title__icontains=query))

        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        context['page_title'] = "Partners"
        return context


class PartnerDetailView(DetailView):
    model = Partner
    template_name = 'partners/partner_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{self.object.name} Details"
        context['can_modify'] = (
                self.request.user == self.object.creator or
                self.request.user.groups.filter(name="Moderators").exists()
        )

        return context


class PartnerCreateView(LoginRequiredMixin,CreateView):
    form_class = PartnerCreateForm
    template_name = 'partners/create_partner.html'
    success_url = reverse_lazy('partners:partners_list')
    extra_context = {
        'page_title': "Create Partner",
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self,form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class EditPartnerView(LoginRequiredMixin,CreatorOrModeratorMixin,UpdateView):
    model = Partner
    form_class = PartnerEditForm
    template_name = 'partners/edit_partner.html'
    success_url = reverse_lazy('partners:partners_list')
    extra_context = {
        'page_title': "Edit Partner",
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class PartnerDeleteView(LoginRequiredMixin,CreatorOrModeratorMixin,DeleteView):
    model = Partner
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('partners:partners_list')


class PartnerListApiView(ListAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.select_related('creator','character').prefetch_related('roles').all()