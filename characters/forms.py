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
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    type = forms.ChoiceField(
        choices=Character.HeroType.choices,
        widget=forms.RadioSelect,
    )
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