from django import forms


class ResultImagesUploadForm(forms.Form):

    def __init__(self, *args, color_amount=None, **kwargs):
        super(ResultImagesUploadForm, self).__init__(*args, **kwargs)
        for color in color_amount:
            self.fields['color_{}'.format(str(color))] = \
                forms.FileField(widget=forms.ClearableFileInput(attrs={
                    'type': 'file',
                    'accept': 'image/*',
                    'multiple': True}))


class EachColorUploadForm(forms.Form):
    color_images = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'type': 'file',
        'accept': 'image/*',
        'multiple': True}))
