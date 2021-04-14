from django import forms
from string import Template
from django.utils.safestring import mark_safe

from pictures.models import TargetImage


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        html = Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))


class ResultImagesUploadForm(forms.Form):

    def __init__(self, *args, color_amount=None, **kwargs):
        super(ResultImagesUploadForm, self).__init__(*args, **kwargs)
        print(color_amount)
        for color in color_amount:
            print(color)
            self.fields['color_{}'.format(str(color))] = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
