from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Ingredient, Recipe, Tag
from users.models import Follow, User
from .filters import RecipeFilter
from .mixins import CreateListRetrieveViewSet, RecpieActionsMixin
from .paginations import FoodgramPagination
from .permissions import FoodgramUsersPermission, IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, SetPasswordSerializer,
                          SubscriptionsSerializer, TagSerializer,
                          UserCreateSerializer, UserSerializer)
from .utils import RecpieDownloadPDFMixin


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [FoodgramUsersPermission, ]
    pagination_class = FoodgramPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def me(self, request):
        me = get_object_or_404(User, pk=request.user.pk)
        serializer = self.get_serializer(me)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def set_password(self, request):
        me = get_object_or_404(User, pk=request.user.pk)
        serializer = SetPasswordSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        me.set_password(serializer.data.get("new_password"))
        me.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def subscriptions(self, request):
        subscriptions = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionsSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        serializer = SubscriptionsSerializer(
            author, context={'request': request})
        if request.method == 'POST':
            if Follow.objects.filter(
                    user=request.user, author=author).exists():
                return Response(
                    {'errors': ['Вы уже подписаны на этого автора.']},
                    status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not Follow.objects.filter(
                    user=request.user, author=author).exists():
                return Response(
                    {'errors': ['Вы не подписаны на этого автора.']},
                    status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.get(user=request.user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny, ]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny, ]
    pagination_class = None

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet,
                    RecpieActionsMixin,
                    RecpieDownloadPDFMixin):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    pagination_class = FoodgramPagination

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return RecipeCreateSerializer
        return RecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.user
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_favorited == '1':
            queryset = queryset.filter(favoriting__user=user)
        if is_in_shopping_cart == '1':
            queryset = queryset.filter(recipe_in_cart__user=user)
        return queryset
