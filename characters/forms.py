from django import forms

from characters.models import Character
from common.models import Role


# class CharacterForm(forms.Form):
#     name = forms.CharField(label='Character Name',max_length=100)
#     title = forms.CharField(label='Character Title',max_length=100)
#     type = forms.ChoiceField(label='Character Type',choices=Character.HeroType.choices,
#                              widget=forms.RadioSelect)
#     power = forms.IntegerField(label='Character Power',min_value=0)
#     description = forms.CharField(max_length=500,
#                                   widget=forms.Textarea(attrs={'placeholder': 'Enter Character Description...'}),)
#     slug = forms.SlugField(max_length=100,required=False)
#     image_url = forms.URLField(label='Character Image URL',required=False)

class CharacterForm(forms.ModelForm):
    attack = forms.IntegerField(min_value=0,max_value=100)
    defense = forms.IntegerField(min_value=0, max_value=100)
    hp = forms.IntegerField(min_value=0, max_value=100)

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
        attack = cleaned_data.get("attack") or 0
        defense = cleaned_data.get("defense") or 0
        hp = cleaned_data.get("hp") or 0

        if attack + defense + hp > 100:
            raise forms.ValidationError(
                "The total number of stats must not exceed 100"
            )

        return cleaned_data


    class Meta:
        exclude = ['slug']
        model = Character

class CharacterCreateForm(CharacterForm):
    ...

class CharacterEditForm(CharacterForm):
    ...

class CharacterDeleteForm(CharacterForm):
    ...

class CharacterSearchForm(forms.Form):
    query = forms.CharField(max_length=100,label='',required=False)