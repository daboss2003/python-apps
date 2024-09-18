from django import forms


class Audio(forms.Form):
    music = forms.FileField()