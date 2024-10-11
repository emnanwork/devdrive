from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register("blogs", views.BlogModelViewSet)

urlpatterns = [
   path("", include(router.urls)),
#    path("blogs", views.blog_list),
#    path("blogs/<int:pk>", views.blog_detail)
]