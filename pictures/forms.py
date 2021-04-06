from django import forms


class ProductImagesUploadForm(forms.Form):
    model_cut = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))