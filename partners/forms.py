from django import forms

from partners.models import Partner
from common.models import Role


class PartnerForm(forms.ModelForm):
    attack = forms.IntegerField(min_value=1, max_value=40, error_messages={
        "required": "Please enter a number between 1 and 40"
    })
    defense = forms.IntegerField(min_value=1, max_value=40, error_messages={
        "required": "Please enter a number  between 1 and 40"
    })
    hp = forms.IntegerField(min_value=1, max_value=40, error_messages={
        "required": "Please enter a number  between 1 and 40"
    })

    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def clean(self):
        cleaned_data = super().clean()
        attack = cleaned_data.get("attack") or 1
        defense = cleaned_data.get("defense") or 1
        hp = cleaned_data.get("hp") or 1

        name = cleaned_data.get("name", "")
        title = cleaned_data.get("title", "")

        if attack + defense + hp > 40:
            raise forms.ValidationError(
                "The total number of stats must not exceed 40"
            )

        if name and title and name == title:
            raise forms.ValidationError('Partner name and title cannot be the same')


        return cleaned_data

    class Meta:
        exclude = ['slug']
        model = Partner
        labels = {
            'character': "Select an existing character",
            'image_url': "Partner Image URL"
        }
        help_texts = {
            'image_url': "There will be default image if left empty",
            'character': "Character to receive support from this partner"
        }
        error_messages = {
            "name": {
                'max_length': "The Partner name is too long.",
                'required': "Please enter the name of your partner."
            },
            "title": {
                'max_length': "The Partner title is too long.",
                'required': "Please enter the title of your partner."
            },
            "description": {
                'required': "Please enter a description of your partner."
            },
            "character": {
                'required': "Please select a character."
            }
        }
        fields = [
            "name",
            "title",
            "attack",
            "defense",
            "hp",
            "roles",
            "description",
            "image_url",
            "character"
        ]


class PartnerCreateForm(PartnerForm):
    ...


class PartnerEditForm(PartnerForm):
    ...

class PartnerSearchForm(forms.Form):
    query = forms.CharField(max_length=100,label='',required=False)