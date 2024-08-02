from django.urls import path
from . import views

urlpatterns = [
#    path("", include(router.urls)),
   path("blogs", views.blog_list),
   path("blogs/<int:pk>", views.blog_detail)
]