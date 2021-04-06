from django.db import models
from django.conf import settings


def target_img_directory_path(instance, filename):
    return 'target/image_{}'.format(filename)


def reference_img_directory_path(instance, filename):
    return 'reference/image_{}'.format(filename)


def result_img_directory_path(instance, filename):
    return 'result/image_{}'.format(filename)


class Bundle(models.Model):
    """
    유저가 업로드하는 모델컷들의 묶음입니다.
    체험은 하나의 Bundle에 하나의 ModelImage가 있고, 이후 서비스를 한다면 여러개의 ModelImage가 묶입니다.
    결제에 사용할 예정이며, 유저가 1회 사용할 때 count 할 수 있는 단위입니다.
    * 현재는 모든 이미지는 체험이라 생각하여 모델을 구성하였습니다.
    * 추후 실제 서비스를 하게 되었을 때 모델을 추가해야 합니다. (체험의 단위를 디테일컷으로 할지? 모델컷으로 할지?)
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class TargetImage(models.Model):
    """
    유저가 업로드하는 모델 컷 이미지입니다.
    """
    STATUS = [
        (0, '착용사진'),
        (10, '옷만 있는사진'),
        (100, 'other')
    ]
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, related_name='targets')
    kinds = models.IntegerField(choices=STATUS)
    image = models.FileField(upload_to=target_img_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReferenceImage(models.Model):
    """
    유저가 업로드하는 변환할 색상의 이미지입니다.
    * 만약 업로드 하지 않고 RGB 값을 주거나, 대표색상으로 변환할 때는 image=Null 입니다.
    """
    target_image = models.ForeignKey(TargetImage, on_delete=models.CASCADE, related_name="references")
    image = models.FileField(upload_to=reference_img_directory_path, null=True, blank=True)
    description = models.CharField(max_length=100, help_text="유저가 RGB값으로 요청시 사용하거나 필요에 의해 작성합니다.", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResultImage(models.Model):
    reference_image = models.ForeignKey(ReferenceImage, on_delete=models.CASCADE, related_name="results")
    image = models.FileField(upload_to=result_img_directory_path)
    is_usable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
