from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    """
    Classe représentant le profil d'un User
    """
    user = models.OneToOneField(User,
                                related_name='profile',
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    birthday = models.DateField()

    def __str__(self):
        if self.user is not None:
            return 'Profil de {}'.format(self.user.username)
        else:
            return super(Profile, self).__str__()