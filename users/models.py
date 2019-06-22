from django.contrib.auth.models import AbstractUser
from django.db.models import *
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    image = ImageField(_("Image of User"), upload_to="img/", default="{% static 'image/bye.jpg' %}")
    followings = ManyToManyField("self", related_name='followers', symmetrical=False)

    # def get_absolute_url(self):
    #     return reverse("users:detail", kwargs={"username": self.username})
