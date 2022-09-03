import re

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Comment, Review
from categories.models import Category, Genre, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class SignupSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для эндпойнта /auth/sigignup/.
    """
    username = serializers.RegexField(r'^[\w.@+-]+$', required=True)
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """
        Проверка того, что пользователя с таким же емейлом нет в базе.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Данный емейл уже есть в базе')
        return value

    def validate_username(self, value):
        """
        Проверка того, что пользователя с таким же юзернеймом нет в базе.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Данный username уже есть в базе'
            )
        if not re.fullmatch(r'^[\w.@+-]+$', value) or value == 'me':
            raise serializers.ValidationError(
                'Данный username не подходит под требования'
            )
        return value

    class Meta:
        model = User
        fields = ('username', 'email',)


class UserSerializer(SignupSerializer):
    """
    Сериалайзер для кастмной пользовательской модели.
    """
    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug', ]
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug', ]
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(
        source='average_rating', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Title
