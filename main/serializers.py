# Serializers define the API representation.
from django.contrib.auth.models import User
from rest_framework import serializers


class ListUserSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'exposition de listes d'Users
    """
    birthday = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'birthday',)

    def get_birthday(self, obj):
        """
        Méthode qui récupère la date de naissance de l'instance de User sérialisée
        :param obj:
        :return:
        """
        try:
            return obj.profile.birthday.strftime("%d/%m/%Y")  #TODO : A gérer avec la localisation
        except:
            return ''


class DetailUserSerializer(ListUserSerializer):
    """
    Serializer pour l'exposition de détail d'User
    """

    class Meta(ListUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'birthday', 'is_superuser', 'is_staff',)