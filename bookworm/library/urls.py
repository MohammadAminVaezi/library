from django import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from library.views import *


router = DefaultRouter()


router.register(r'authors', AuthorViewset)
router.register(r'books', BookViewset)
router.register(r'comments', CommentViewset)


urlpatterns = router.urls + [
    path('login/', view=obtain_auth_token),
    path('logout/', LogoutAPIView.as_view())
]
