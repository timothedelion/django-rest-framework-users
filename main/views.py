from datetime import timedelta, date

from django.contrib.auth.models import User

# Create your views here.
from django.utils.timezone import now
from rest_framework import viewsets

from DRF import settings
from main.serializers import ListUserSerializer, DetailUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint des Users
    """
    queryset = User.objects.all()

    # Dictionnaire de correspondance action : serialiseur
    serializers = {
        'default': ListUserSerializer,
        'list': ListUserSerializer,
        'retrieve': DetailUserSerializer,
    }

    def get_serializer_class(self):
        """
        Surcharge de get_serializer_class pour appeler un serializer different selon le type d'action
        :return:
        """
        return self.serializers.get(self.action,
                                    self.serializers['default'])

    def get_queryset(self):
        """
        Surcharge de get_queryset pour :
         - filtrer par année de naissance des Users sur le query parameter ?year=
         - filter par age manimal sur le query parameter ?age_min=
         - filter par age maximal sur le query parameter ?age_max=
         - filter par age exact (en années) sur le query parameter ?age_exact=
        """

        queryset = self.queryset

        # --- Année de naissance --- :
        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(profile__birthday__year=year)

        # --- Age Maxi --- :
        age_max = self.request.query_params.get('age_max', None)
        if age_max is not None:
            try:
                birthday_min = now().date() - timedelta(days=365*int(age_max))
                queryset = queryset.filter(profile__birthday__gte=birthday_min)
            except:
                pass

        # --- Age Mini --- :
        age_min = self.request.query_params.get('age_min', None)
        if age_min is not None:
            try:
                birthday_max = now().date() - timedelta(days=365*int(age_min))
                queryset = queryset.filter(profile__birthday__lte=birthday_max)
            except:
                pass

        # --- Age exact (en années) --- :
        age_exact = self.request.query_params.get('age_exact', None)

        if age_exact is not None:
            try:
                date_now = now().date()
                birthday_min = date(year=date_now.year - int(age_exact) - 1,
                                    month=date_now.month,
                                    day=date_now.day)
                birthday_max = date(year=date_now.year - int(age_exact),
                                    month=date_now.month,
                                    day=date_now.day)
                queryset = queryset.filter(profile__birthday__lte=birthday_max) \
                    .filter(profile__birthday__gte=birthday_min)
            except:
                pass

        return queryset
