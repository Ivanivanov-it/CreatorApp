import re

from django import forms

from cards.models import Card

HEX_COLOR_REGEX = re.compile(r"^#([0-9A-Fa-f]{6})$")

class CardForm(forms.ModelForm):
    border_color = forms.CharField(
        widget=forms.TextInput(attrs={"type": "color"})
    )

    background_color = forms.CharField(
        widget=forms.TextInput(attrs={"type": "color"})
    )

    image_border_color = forms.CharField(
        widget=forms.TextInput(attrs={"type": "color"})
    )

    accent_color = forms.CharField(
        widget=forms.TextInput(attrs={"type": "color"})
    )



    def clean_border_color(self):
        border_color = self.cleaned_data["border_color"]
        if not HEX_COLOR_REGEX.match(border_color):
            raise forms.ValidationError('Enter a valid hex border color like #ffffff')
        return border_color

    def clean_background_color(self):
        background_color = self.cleaned_data["background_color"]
        if not HEX_COLOR_REGEX.match(background_color):
            raise forms.ValidationError('Enter a valid hex background color like #ffffff')
        return background_color

    def clean_image_border_color(self):
        image_border_color = self.cleaned_data["image_border_color"]
        if not HEX_COLOR_REGEX.match(image_border_color):
            raise forms.ValidationError('Enter a valid hex image border color like #ffffff')
        return image_border_color

    def clean_accent_color(self):
        accent_color = self.cleaned_data["accent_color"]
        if not HEX_COLOR_REGEX.match(accent_color):
            raise forms.ValidationError('Enter a valid hex accent color like #ffffff')
        return accent_color

    class Meta:
        model = Card
        exclude = ['is_default','creator']
        widgets = {
            "border_style": forms.Select(attrs={"class": "form-select"}),
            "image_border_style": forms.Select(attrs={"class": "form-select"}),
        }

        labels = {
            'name': "Card Name"
        }
        help_texts = {
            'border_color': 'Select a border color',
            'background_color': 'Select a background color',
            'accent_color': 'Select a accent color',
            'image_border_color': 'Select an image border color',
            'border_style': 'Select a border style',
            'image_border_style': 'Select an image border style',
        }
        error_messages = {
            "name": {
                'max_length': "The Card name is too long.",
                'required': "Please enter the name of your card."
            },
            "border_color": {
                'required': "Please pick the color of the border."
            },
            "background_color": {
                'required': "Please pick the color of the background."
            },
            "accent_color": {
                'required': "Please pick the accent color of your card."
            }
            ,
            "image_border_color": {
                'required': "Please pick the image border color of your card."
            },
            "border_style": {
                'required': "Please pick the border style of your card."
            },
            "image_border_style": {
                'required': "Please pick the image border style of your card."
            }
        }


class CardEditForm(CardForm):
    creator_display = forms.CharField(disabled=True,required=False,label="Creator")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['creator_display'].initial = self.instance.creator.username

    class Meta(CardForm.Meta):
        fields = "__all__"




