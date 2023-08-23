from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return "accounts/user_{pk}/avatar/{filename}".format(
        pk=instance.user.pk,
        filename=filename
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(
        null=True,
        blank=True,
        default='avatar.jpg',
        upload_to=profile_avatar_directory_path,
        verbose_name='Avatar'
    )

    class Meta:
        permissions = (("change_avatar", "can change avatar of profile"),)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:userprofile', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     # save the profile first
    #     super().save(*args, **kwargs)

        ## resize the image
        # img = Image.open(self.avatar.path)
        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     # create a thumbnail
        #     img.thumbnail(output_size)
        #     # overwrite the larger image
        #     img.save(self.avatar.path)

