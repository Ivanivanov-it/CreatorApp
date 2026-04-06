from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import  CreateView, ListView
from rest_framework.generics import get_object_or_404
from contacts.forms import ContactForm
from contacts.models import Contact


# Create your views here.



class CreateMailView(SuccessMessageMixin,CreateView):
    form_class = ContactForm
    success_url = reverse_lazy('common:home')
    template_name = 'contacts/contact.html'
    extra_context = {
        'page_title': "Contact Us"
    }
    # success_message = "Your message has been sent."





class ContactsListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Contact
    template_name = 'contacts/contact_list_page.html'
    context_object_name = 'contacts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Contacts"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="ContactManagers").exists()


    def handle_no_permission(self):
        return redirect('no_permission')

class FinishView(LoginRequiredMixin,UserPassesTestMixin,View):

    def test_func(self):
        return self.request.user.groups.filter(name="ContactManagers").exists()


    def handle_no_permission(self):
        return redirect('no_permission')

    def post(self,request,pk):
        contact = get_object_or_404(Contact, pk=pk)
        contact.is_finished = True
        contact.save(update_fields=['is_finished'])
        return redirect('contacts:user-contacts')