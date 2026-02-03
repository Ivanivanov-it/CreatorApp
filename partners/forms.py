from django import forms

from partners.models import Partner
from common.models import Role


class PartnerForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        exclude = ['slug']
        model = Partner


class PartnerCreateForm(PartnerForm):
    ...


class PartnerEditForm(PartnerForm):
    ...
