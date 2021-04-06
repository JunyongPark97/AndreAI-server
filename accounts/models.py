from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, phone, **kwargs):
        if not phone:
            raise ValueError('핸드폰 번호를 입력해주세요')
        user = self.model(phone=phone, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(password, phone, **kwargs)

    def create_superuser(self, password, phone, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser=True')
        return self._create_user(password, phone, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    shop_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True,
                             help_text="만약 같은 번호로 신청한다면, 기존에 생성된 유저를 호출하여 모델컷 생성")
    email = models.EmailField(max_length=100, unique=True, db_index=True, blank=True, null=True)

    USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = ['phone']

    objects = UserManager()
    is_active = models.BooleanField(default=True, help_text="탈퇴/밴 시 is_active = False")
    is_staff = models.BooleanField(default=False, help_text="super_user와의 권한 구분을 위해서 새로 만들었습니다. 일반적 운영진에게 부여됩니다.")
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    quit_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        if self.is_staff:
            return '[staff] {}'.format(self.email)
        if self.shop_name:
            return '[shop] {}'.format(self.shop_name)
        return self.phone
