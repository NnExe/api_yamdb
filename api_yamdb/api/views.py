from categories.models import Category, Genre, Title
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Review
from users.models import User

from api.filters import TitleFilter
from api.permissions import (IsAdminOrReadOnly, IsAdminOrSuperadmin,
                             ReviewCommentPermissions)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReadOnlyTitleSerializer,
                             ReviewSerializer, SignupSerializer,
                             TitleSerializer, UserSerializer)


class UserPagination(PageNumberPagination):
    page_size = 20


@api_view(['POST'])
def user_signup(request):
    """
    Функция анализирует запрос на создание пользователя. Если он корректный -
    создается пользователь и отправляется письмо с кодом подтверждения.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    serializer = SignupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer.save()
    user = get_object_or_404(User, username=username)
    code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'{code}',
        from_email=f'{settings.ADMIN_EMAIL}',
        recipient_list=[f'{email}'],
        fail_silently=False,
    )
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def user_token(request):
    """
    Функция проверяет запрос на соответствие кода потверждения пользователю
    и если всё корректно выдаёт JWT токен.
    """
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    if not all((username, confirmation_code)):
        return Response(
            data={'message': 'Не заданы все поля (или заданы неверно)'},
            status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(
            data={'message': 'Код подтверждения невалидный'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token = str(AccessToken.for_user(user))
    return Response(data={'token': f'{token}'}, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_me(request):
    """
    Функция работает с эндпойнтом /api/v1/users/me.
    Выдавая информацию по текущему пользователи и разрешая поправить часть
    полей.
    """
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        if (
            'role' in request.data
            and request.user.role == User.USER
        ):
            serializer.validated_data['role'] = User.USER
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с эндпойнтами /api/v1/users/ и
    /api/v1/users/{username}/.
    """
    queryset = User.objects.all()
    lookup_value_regex = '[^/]+'
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdminOrSuperadmin)
    serializer_class = UserSerializer
    pagination_class = UserPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """Вью сет для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermissions,
                          permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для коментариев к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermissions,
                          permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
        )
        serializer.save(author=self.request.user, review=review)


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin, mixins.CreateModelMixin,
                  mixins.DestroyModelMixin):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с записями.
    """
    queryset = Title.objects.annotate(average_rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class GenreViewSet(BaseViewSet):
    """
    Вьюсет для работы с жанрами.
    """
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class CategoryViewSet(BaseViewSet):
    """
    Вьюсет для работы с категориями.
    """
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
