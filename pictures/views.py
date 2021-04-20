from django.db import transaction
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView

from accounts.models import User
from pictures.models import Bundle, TargetImage, ReferenceImage, ResultImage
from pictures.slack import apply_slack_message, apply_slack_message
from django.http import Http404


class TryModelCutView(GenericAPIView):
    """
    [DEPRECATED]
    """
    serializer_class = None

    @transaction.atomic
    def post(self, request):
        data = request.data
        files = request.FILES

        email = data.pop('email')[0]
        phone = data.pop('phone')[0]
        shop_name = data.pop('shop_name')[0]
        target_img = files.pop('target')[0]
        reference_imgs = files.pop('ref')
        attrs = {'email': email, 'shop_name': shop_name}

        user, _ = User.objects.get_or_create(phone=phone,
                                             defaults=attrs)
        bundle = Bundle.objects.create(user=user)
        target = TargetImage.objects.create(bundle=bundle, kinds=0, image=target_img)
        for ref_img in reference_imgs:
            ReferenceImage.objects.create(target_image=target, image=ref_img)

        apply_slack_message("[착용 이미지 변경 신청] {} 쇼핑몰에서 착용이미지 변경을 신청했습니다.".format(user.shop_name))

        return Response(status=status.HTTP_201_CREATED)


class TryDetailCutView(GenericAPIView):
    serializer_class = None

    @transaction.atomic
    def post(self, request):
        data = request.data
        files = request.FILES

        # email = data.pop('email')[0]
        phone = data.pop('phone')[0]
        shop_name = data.pop('shop_name')[0]
        target_img = files.pop('target')[0]
        reference_imgs = files.pop('ref')
        attrs = {'shop_name': shop_name}

        user, _ = User.objects.get_or_create(phone=phone,
                                             defaults=attrs)
        bundle = Bundle.objects.create(user=user)
        target = TargetImage.objects.create(bundle=bundle, kinds=10, image=target_img)
        for ref_img in reference_imgs:
            ReferenceImage.objects.create(target_image=target, image=ref_img)
        apply_slack_message("[상세이미지 변경 신청] {} 쇼핑몰에서 상세이미지 변경을 신청했습니다.".format(user.shop_name))
        return Response(status=status.HTTP_201_CREATED)


class DownloadView(DetailView):
    template_name = 'download.html'
    queryset = TargetImage.objects.all()

    def get(self, request, *args, **kwargs):
        # try:
        print(kwargs)
        phone = request.GET.get('phone', None)
        pk = request.GET.get('query', None)
        print(phone)
        print(pk)
        # except Exception:
        #     return Http404

        if not User.objects.filter(phone=phone).exists():
            return Response(status.HTTP_404_NOT_FOUND)

        target_image = TargetImage.objects.get(pk=pk)
        user = User.objects.filter(phone=phone).last()

        if target_image.bundle.user != user:
            return Response(status.HTTP_400_BAD_REQUEST)
        results = target_image.results.all()

        color_numbers = results.values_list('color_number', flat=True).distinct().order_by('color_number')

        print(user)
        print(color_numbers)
        result_list = []
        for color_number in color_numbers:
            result_queryset = results.filter(color_number=color_number)
            image_url_list = []
            for result in result_queryset:
                image_url_list.append(result.image.url)
            result_list.append(image_url_list)
        print('--------')
        print(result_list)
        context = {}
        context['user'] = user
        context['result_list'] = result_list
        print('===')
        print(result_list)
        return render(request, 'download.html', context)
