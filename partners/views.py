from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from partners.forms import PartnerCreateForm, PartnerEditForm, PartnerSearchForm
from partners.models import Partner


def partners_list(request: HttpRequest) -> HttpResponse:
    search_form = PartnerSearchForm(request.GET or None)

    partners = Partner.objects.all()


    if 'query' in request.GET:
        if search_form.is_valid():
            partners = partners.filter(Q(name__icontains=search_form.cleaned_data['query']) | Q(title__icontains=search_form.cleaned_data['query']))


    context = {
        'page_title': "Partners",
        'partners': partners,
        'search_form': search_form,
    }

    return render(request, 'partners/partners_page.html', context)


def partner_detail(request: HttpRequest, pk: int) -> HttpResponse:
    partner = get_object_or_404(Partner, pk=pk)
    context = {
        'page_title': f"{partner.name} Details",
        'partner': partner,
    }

    return render(request, 'partners/partner_page.html', context)


def create_partner(request: HttpRequest) -> HttpResponse:
    form = PartnerCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        return redirect('partners:partners_list')

    context = {
        'page_title': "Create Partner",
        'form': form,
    }

    return render(request, 'partners/create_partner.html', context)


def edit_partner(request: HttpRequest, pk: int) -> HttpResponse:
    partner = get_object_or_404(Partner, pk=pk)
    form = PartnerEditForm(request.POST or None, instance=partner)

    if request.method == "POST" and form.is_valid():
        form.save()

        return redirect('partners:partners_list')

    context = {
        'page_title': "Edit Partner",
        'form': form,
        'partner': partner,
    }

    return render(request, 'partners/edit_partner.html', context)


# def delete_partner(request: HttpRequest, pk: int) -> HttpResponse:
#     partner = get_object_or_404(Partner, pk=pk)
#
#     if partner:
#         partner.delete()
#
#     return redirect('partners:partners_list')


class PartnerDeleteView(DeleteView):
    model = Partner
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('partners:partners_list')
