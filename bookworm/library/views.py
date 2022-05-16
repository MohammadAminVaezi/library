from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import AuthorSerializer, BookSerializer, CommentSerializer
from .models import Author, Book, Comment
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class LogoutAPIView(GenericAPIView):
    permission_class = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': f"{request.user.username} byeeeeee!"})


class AuthorViewset(viewsets.ModelViewSet):
    permission_class = (IsAuthenticatedOrReadOnly,)
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    filterset_fields = ['firstname', 'lastname', 'nationality']


class BookViewset(viewsets.ModelViewSet):
    permission_class = (IsAuthenticatedOrReadOnly,)
    serializer_class = BookSerializer
    queryset = Book.objects.order_by('-rate')
    filterset_fields = ['title', 'genre', 'author', 'rate']

    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        object.view_count = object.view_count + 1
        object.save(update_fields=("view_count", ))
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        for book in queryset:
            rate = 0
            count = book.ratings.count()
            for user in book.ratings.all():
                object = Comment.objects.get(user=user.id, book=book.id)
                if object.rating:
                    rate += object.rating
                else:
                    count -= 1
            try:
                rate = rate/count

            except:
                rate = 0

            finally:
                book.rate = rate
                book.save()

        return queryset


class CommentViewset(viewsets.ModelViewSet):
    permission_class = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filterset_fields = ['user', 'book']

    def get_serializer_context(self):
        context = super(CommentViewset, self).get_serializer_context()
        context['user'] = self.request.user
        return context
