from django.db.models import Avg

from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrModerOrAdminOrSuperuser
                          )
from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          ReviewSerializer, TitleSerializer,
                          TitleSerializerGet, AdminUserCreateSerializer,
                          MeUserSerializer, MeUserUpdateSerializer,
                          UserSerializer, TokenObtainSerializer,
                          SignUpSerializer, GenreSerializer)


class UserSignupView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)


class CustomTokenObtainView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        user = User.objects.get(username=username)
        refresh = RefreshToken.for_user(user)
        data = {
            'token': str(refresh.access_token),
        }

        return Response(data, status=status.HTTP_200_OK)


class AdminCreateUserView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = AdminUserCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializerGet
        return TitleSerializer

    def get_queryset(self):
        """
        Переопределяем этот метод, чтобы добавить аннотацию с рейтингом.
        """
        return Title.objects.annotate(rating=Avg('reviews__score'))


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    ViewSet для работы с объектами модели Genre.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    ViewSet для работы с объектами модели Category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с объектами модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerOrAdminOrSuperuser,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        """Метод получает Title по ID, переданному в URL параметрах."""
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        """Метод возвращает все отзывы для конкретного произведения (Title)."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с объектами модели Comment.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModerOrAdminOrSuperuser,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        """
        Метод получает отзыв (Review) по ID, переданному в URL параметрах.
        """
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        """
        Метод возвращает все комментарии для конкретного отзыва (Review).
        Проверяет существование Title с id, связанным с отзывом.
        """
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'], title=title
        )
        return review.comments.all()

    def perform_create(self, serializer):
        """
        Метод сохраняет новый комментарий,
        связывая его с автором и отзывом (Review).
        """
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            data = request.data.copy()
            serializer = MeUserUpdateSerializer(
                user, data=data, partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = MeUserSerializer(user, context={'request': request})
        return Response(serializer.data)
