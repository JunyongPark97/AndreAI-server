import requests
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView

from custom_manage.forms import ResultImagesUploadForm
from pictures.models import TargetImage, ResultImage


class StaffUploadTemplateView(DetailView):
    """
    Staff Upload Page
    """
    template_name = 'upload/manage.html'
    queryset = TargetImage.objects.all()

    def get_context_data(self, **kwargs):
        context = super(StaffUploadTemplateView, self).get_context_data()
        color_amount = range(self.get_object().color_amount)
        form = ResultImagesUploadForm(color_amount=color_amount)
        context['user'] = self.request.user
        context['color_amount'] = color_amount
        context['form'] = form
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        target_image = self.get_object()
        c_a = target_image.color_amount
        form = ResultImagesUploadForm(color_amount=range(c_a), data=request.FILES)
        data = form.data
        for i in range(c_a):
            key = 'color_{}'.format(i)
            each_color = data.pop(key)
            for partial_color_result in each_color:
                ResultImage.objects.create(target_image=target_image, image=partial_color_result, color_number=i)

        return redirect('custom_manage:staff_confirm', pk)


class StaffUploadConfirmTemplateView(DetailView):
    """
    Staff Upload Confirm Page
    """
    template_name = 'upload/confirm.html'
    queryset = TargetImage.objects.all()

    def get_context_data(self, **kwargs):
        context = super(StaffUploadConfirmTemplateView, self).get_context_data()
        target_image = self.get_object()
        results_qs = ResultImage.objects.filter(target_image=target_image)
        color_numbers = results_qs.values_list('color_number', flat=True).distinct()
        ordered_data = {}
        for number in color_numbers:
            partial_results_qs = results_qs.filter(color_number=number)
            ordered_data[str(number)] = partial_results_qs
        context['ordered_data'] = ordered_data
        return context


def confirm_done(request, pk):
    #TODO 비즈톡 발송
    return HttpResponseRedirect('/admin/pictures/targetimage/')
