from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import NotFound
from django.core.mail import send_mail

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User, validate_username


class MeUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
        read_only_fields = ('role',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'role', 'bio']


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[validate_username],
        required=True
    )
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound({'detail': 'User not found.'})

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                {'detail': 'Invalid confirmation code.'}
            )

        data['username'] = username
        return data


class AdminUserCreateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=['user', 'moderator', 'admin'],
        default='user'
    )

    class Meta:
        model = User
        fields = ['username', 'email',
                  'first_name', 'last_name', 'role', 'bio']

    def create(self, validated_data):
        role = validated_data.pop('role', 'user')
        user = User.objects.create_user(**validated_data)
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        elif role == 'moderator':
            user.is_staff = True
        user.save()
        return user


class MeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
        read_only_fields = ('role',)


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_username])

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if User.objects.filter(
            username=value).exists() and not User.objects.filter(
                email=self.initial_data.get('email')).exists():
            raise serializers.ValidationError(
                'Это имя пользователя уже занято.'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(
            email=value).exists() and not User.objects.filter(
                username=self.initial_data.get('username')).exists():
            raise serializers.ValidationError(
                'Этот email уже зарегистрирован.'
            )
        return value

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)

        # Отправка confirmation_code после всей валидации
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Your confirmation code',
            f'Your confirmation code is {confirmation_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    Используется для преобразования данных модели Category в JSON формат
    и обратно.
    """

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Genre.
    Используется для преобразования данных модели Genre в JSON формат
    и обратно.
    """

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializerGet(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    Используется для преобразования данных модели Title в JSON формат
    и обратно.
    """
    category = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    rating = serializers.FloatField(read_only=True)
    description = serializers.CharField(default='', allow_blank=True)

    class Meta:
        fields = '__all__'
        model = Title

    def get_category(self, obj):
        if obj.category is None:
            return {"name": "", "slug": ""}
        return {
            "name": obj.category.name,
            "slug": obj.category.slug
        }


class TitleSerializer(serializers.ModelSerializer):

    """
    Сериализатор для модели Title.
    Используется для преобразования данных модели Title в JSON формат
    и обратно.
    """
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    rating = serializers.FloatField(read_only=True)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate(self, attrs):
        # Проверка на пустой список жанров
        if 'genre' in attrs and not attrs['genre']:
            raise serializers.ValidationError(
                {'genre': 'Список жанров не может быть пустым.'}
            )
        return attrs

    def to_representation(self, instance):
        return TitleSerializerGet(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор моделей отзывов."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context['view'].kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)

        # Проверка на наличие поля score только для POST запросов
        if request.method == 'POST':
            # Проверка на наличие существующего отзыва
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise serializers.ValidationError(
                    "Отзыв уже существует для этого произведения."
                )

        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Преобразует данные модели Comment в JSON формат и обратно,
    включая информацию об авторе.
    """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
