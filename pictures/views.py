from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from accounts.models import User
from pictures.models import Bundle, TargetImage, ReferenceImage
from pictures.slack import apply_slack_message, apply_slack_message


class TryModelCutView(GenericAPIView):
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

        email = data.pop('email')[0]
        phone = data.pop('phone')[0]
        shop_name = data.pop('shop_name')[0]
        target_img = files.pop('target')[0]
        reference_imgs = files.pop('ref')
        attrs = {'email': email, 'shop_name': shop_name}

        user, _ = User.objects.get_or_create(phone=phone,
                                             defaults=attrs)
        bundle = Bundle.objects.create(user=user)
        target = TargetImage.objects.create(bundle=bundle, kinds=10, image=target_img)
        for ref_img in reference_imgs:
            ReferenceImage.objects.create(target_image=target, image=ref_img)
        apply_slack_message("[상세이미지 변경 신청] {} 쇼핑몰에서 상세이미지 변경을 신청했습니다.".format(user.shop_name))
        return Response(status=status.HTTP_201_CREATED)
