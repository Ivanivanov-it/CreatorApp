from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from partners.forms import PartnerCreateForm, PartnerEditForm
from partners.models import Partner


def partners_list(request: HttpRequest) -> HttpResponse:
    partners = Partner.objects.all()

    context = {
        'page_title': "Partners",
        'partners': partners,
    }

    return render(request, 'partners/partners_page.html', context)


def partner_detail(request: HttpRequest, id: int) -> HttpResponse:
    partner = get_object_or_404(Partner, pk=id)
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


def edit_partner(request: HttpRequest, id: int) -> HttpResponse:
    partner = get_object_or_404(Partner, pk=id)
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


def delete_partner(request: HttpRequest, id: int) -> HttpResponse:
    partner = get_object_or_404(Partner, pk=id)

    if partner:
        partner.delete()

    return redirect('partners:partners_list')
