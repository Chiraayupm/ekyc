from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(ImageUpload)
admin.site.register(VideoUpload)
admin.site.register(IdUpload)
admin.site.register(AddressUpload)
admin.site.register(OTP)