from django.urls import include, path

from rest_framework import routers


from api.customAuthToken import CustomAuthToken
from . import views
from . import models


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'categorie', views.CategorieViewSet)
router.register(r'lieux', views.getViewSet(models.Lieux))
router.register(r'media', views.getViewSet2(models.Photo))
router.register(r'annonce', views.AnnonceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view())
]
