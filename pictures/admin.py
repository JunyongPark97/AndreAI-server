from django.contrib import admin
from django.utils.safestring import mark_safe
from pictures.models import TargetImage, Bundle, ReferenceImage


class TargetImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'kind', 'target_image', 'ref_images', 'user', 'created_at']

    def kind(self, obj):
        return obj.get_kinds_display()

    def target_image(self, obj):
        if obj.image.url:
            return mark_safe('<a href= "{}" target="_blank"><img src="{}" width=200px "/></a>'.format(obj.image.url, obj.image.url))
        else:
            return None

    def ref_images(self, obj):
        if obj.references.exists():
            references = obj.references.all()
            val = ''
            for ref in references:
                val += '<a href= "{}" target="_blank"><img src="{}" width=200px "/></a>'.format(ref.image.url, ref.image.url)

            return mark_safe(val)
        else:
            return None

    def user(self, obj):
        if obj.bundle and obj.bundle.user:
            return obj.bundle.user.shop_name
        else:
            return None


class BundleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user']


class RefImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'target_img', 'ref_images', 'created_at']

    def target_img(self, obj):
        if obj.target_image.image.url:
            return mark_safe('<img src="%s" width=120px "/>' % obj.target_image.image.url)
        else:
            return None

    def user(self, obj):
        if obj.target_image.bundle:
            return obj.target_image.bundle.user.shop_name
        else:
            return None

    def ref_images(self, obj):
        if obj.image.url:
            return mark_safe('<img src="%s" width=120px "/>' % obj.image.url)
        else:
            return None


admin.site.register(Bundle, BundleAdmin)
admin.site.register(TargetImage, TargetImageAdmin)
admin.site.register(ReferenceImage, RefImageAdmin)
