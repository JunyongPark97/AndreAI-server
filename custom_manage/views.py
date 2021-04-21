import uuid
from io import BytesIO

import boto3
import requests
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, DetailView
from rest_framework.views import APIView
from PIL import Image
from andreai.loader import load_credential
from custom_manage.forms import ResultImagesUploadForm, EachColorUploadForm
from pictures.models import TargetImage, ResultImage
SETTING_DEV_DIC = load_credential("develop")['S3']


class StaffUploadTemplateView(DetailView):
    """
    Staff Upload Page
    """
    template_name = 'upload/manage.html'
    queryset = TargetImage.objects.all()
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = SETTING_DEV_DIC['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key = SETTING_DEV_DIC['AWS_SECRET_ACCESS_KEY']
    )

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
                result = ResultImage.objects.create(target_image=target_image, image=partial_color_result, color_number=i)
                resp = requests.get(result.image_url)
                url_generator = str(uuid.uuid4())+'.jpg'
                t = BytesIO(resp.content)
                # S3 upload fileobj 의 file 은 read() 가 있어야 한다. BytesIO가 read 있음. PIL 의 Image 는 read 가 없음.
                self.s3_client.upload_fileobj(
                    t,
                    "andre-storages",
                    'media/downloadable/result/'+url_generator,
                    ExtraArgs={
                        "ContentType": 'image/jpeg',
                        "ContentDisposition": "attachment"
                    }
                )
                image_url = "https://andre-storages.s3.ap-northeast-2.amazonaws.com/media/downloadable/result/{}".format(url_generator)

                result.downloadable_image_url = image_url
                result.save()

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
        color_numbers = results_qs.values_list('color_number', flat=True).distinct().order_by('color_number')
        edit_form = EachColorUploadForm
        ordered_data = {}
        for number in color_numbers:
            partial_results_qs = results_qs.filter(color_number=number)
            ordered_data[str(number)] = partial_results_qs
        #TODO :target image 의 allim talk True면 hidden
        if target_image.bundle.allim_talk:
            is_send = True
        else:
            is_send = False
        context['ordered_data'] = ordered_data
        context['edit_form'] = edit_form
        context['is_send'] = is_send
        return context


class StaffEachColorEditDetailView(APIView):
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = SETTING_DEV_DIC['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key = SETTING_DEV_DIC['AWS_SECRET_ACCESS_KEY']
    )

    def get(self, request, *args, **kwargs):
        """Nope"""
        pk1 = kwargs['pk1']
        pk2 = kwargs['pk2']
        target_image = TargetImage.objects.get(id=pk1)
        results = ResultImage.objects.filter(target_image=target_image, color_number=pk2)
        form = EachColorUploadForm
        context = {}
        context['results'] = results
        context['object'] = target_image
        context['form'] = form

        return render(request, 'upload/each_color_upload.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pk1 = kwargs['pk1']
        pk2 = kwargs['pk2']
        target_image = TargetImage.objects.get(id=pk1)
        form = EachColorUploadForm(data=request.FILES)
        data = form.data
        images = data.pop('color_images')
        if images:
            before_results = ResultImage.objects.filter(target_image=target_image, color_number=pk2)
            before_results.delete()
            for image in images:
                result = ResultImage.objects.create(color_number=pk2, target_image=target_image, image=image)
                resp = requests.get(result.image_url)
                url_generator = str(uuid.uuid4()) + '.jpg'
                t = BytesIO(resp.content)
                self.s3_client.upload_fileobj(
                    t,
                    "andre-storages",
                    'media/downloadable/result/' + url_generator,
                    ExtraArgs={
                        "ContentType": 'image/jpeg',
                        "ContentDisposition": "attachment"
                    }
                )
                image_url = "https://andre-storages.s3.ap-northeast-2.amazonaws.com/media/downloadable/result/{}".format(
                    url_generator)

                result.downloadable_image_url = image_url
                result.save()
        return redirect('custom_manage:staff_confirm', pk1)


def confirm_done(request, pk):
    #TODO 비즈톡 발송
    target_image = TargetImage.objects.get(id=pk)
    bundle = target_image.bundle
    bundle.allim_talk = True
    bundle.save()
    return HttpResponseRedirect('/admin/pictures/targetimage/')
