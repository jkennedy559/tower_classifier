from django import forms


class FileForm(forms.Form):
    image = forms.ImageField(help_text="Upload image: ", required=True)
