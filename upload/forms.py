from django import forms


class video_upload_form(forms.Form):
    docfile = forms.FileField(label='Selectionner un fichier')
