from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from contacts.forms import ContactForm


# Create your views here.

def create_mail(request: HttpRequest) -> HttpResponse:
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        return redirect('characters:home')

    context = {
        'page_title': "Contact Us",
        'form': form,
    }

    return render(request,'contacts/contact.html',context)


class WipPage(TemplateView):
    template_name = 'wip.html'