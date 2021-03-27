from django.db import models
from django.contrib.auth import models as mod

# Create your models here.

class Profile(models.Model):
    aadhar_no = models.CharField(max_length=50)
    pan_no = models.CharField(max_length=50)
    is_kyc_verified = models.BooleanField(default=False)
    user = models.OneToOneField(mod.User, on_delete=models.CASCADE)

    def __str__(self):
        return self.aadhar_no

class ImageUpload(models.Model):
    file = models.FileField(upload_to = 'images/')
    user = models.ForeignKey(mod.User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " Image doc."

class VideoUpload(models.Model):
    file = models.FileField(upload_to = 'videos/')
    user = models.ForeignKey(mod.User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " Video doc."

class IdUpload(models.Model):
    file = models.FileField(upload_to = 'ids/')
    user = models.ForeignKey(mod.User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " ID doc."


class AddressUpload(models.Model):
    file = models.FileField(upload_to = 'addrs/')
    user = models.ForeignKey(mod.User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " Address doc."

class OTP(models.Model):
    otp_code = models.IntegerField() 
    user = models.ForeignKey(mod.User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.otp_code)