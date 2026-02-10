from django import forms

from characters.models import Character
from common.models import Role




class CharacterForm(forms.ModelForm):
    attack = forms.IntegerField(min_value=1,max_value=100,error_messages={
        "required": "Please enter an integer between 1 and 100"
    })
    defense = forms.IntegerField(min_value=1, max_value=100,error_messages={
        "required": "Please enter an integer between 1 and 100"
    })
    hp = forms.IntegerField(min_value=1, max_value=100,error_messages={
        "required": "Please enter an integer between 1 and 100"
    })

    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    type = forms.ChoiceField(
        choices=Character.HeroType.choices,
        widget=forms.RadioSelect,
    )

    def clean(self):
        cleaned_data = super().clean()
        attack = cleaned_data.get("attack") or 1
        defense = cleaned_data.get("defense") or 1
        hp = cleaned_data.get("hp") or 1


        if attack + defense + hp > 100:
            raise forms.ValidationError(
                "The total number of stats must not exceed 100"
            )

        if cleaned_data['name'] == cleaned_data['title']:
            raise forms.ValidationError('Character name and title cannot be the same')


        return cleaned_data


    class Meta:
        exclude = ['slug']
        model = Character
        help_texts = {
            'image_url': 'There will be default image if left empty',
        }
        error_messages = {
            "name": {
                'max_length': "The Character name is too long.",
                'required': "Please enter the name of your character."
            },
            "title": {
                'max_length': "The Character title is too long.",
                'required': "Please enter the title of your character."
            },
            "description": {
                'required': "Please enter a description of your character."
            }
        }
        fields = [
            "name",
            "title",
            "type",
            "attack",
            "defense",
            "hp",
            "roles",
            "description",
            "image_url",
        ]



class CharacterCreateForm(CharacterForm):
    ...

class CharacterEditForm(CharacterForm):
    ...

class CharacterDeleteForm(CharacterForm):
    ...

class CharacterSearchForm(forms.Form):
    query = forms.CharField(max_length=100,label='',required=False)