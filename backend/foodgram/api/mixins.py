from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Recipe, RecipeInCart, RecipeInFavorite
from .serializers import RecipeInSubscriptions


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


class RecpieActionsMixin:
    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, ],
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeInSubscriptions(recipe)
        if request.method == 'POST':
            if RecipeInFavorite.objects.filter(
                    user=request.user, recipe=recipe).exists():
                return Response(
                    {'errors': ['Рецепт уже в избранном.']},
                    status=status.HTTP_400_BAD_REQUEST)
            RecipeInFavorite.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not RecipeInFavorite.objects.filter(
                    user=request.user, recipe=recipe).exists():
                return Response(
                    {'errors': ['Вы не добавляли рецепт с избранное.']},
                    status=status.HTTP_400_BAD_REQUEST)
            RecipeInFavorite.objects.get(
                user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, ],
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeInSubscriptions(recipe)
        if request.method == 'POST':
            if RecipeInCart.objects.filter(
                    user=request.user, recipe=recipe).exists():
                return Response(
                    {'errors': ['Рецепт уже в корзине.']},
                    status=status.HTTP_400_BAD_REQUEST)
            RecipeInCart.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not RecipeInCart.objects.filter(
                    user=request.user, recipe=recipe).exists():
                return Response(
                    {'errors': ['Вы не добавляли рецепт с корзину.']},
                    status=status.HTTP_400_BAD_REQUEST)
            RecipeInCart.objects.get(
                user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(
    #     detail=False,
    #     permission_classes=[permissions.IsAuthenticated, ],
    # )
    # def download_shopping_cart(self, request):
    #     pdfmetrics.registerFont(TTFont(
    #         'Helvetica2', '/app/fonts/Helvetica.ttc'))
    #     buffer = io.BytesIO()
    #     c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    #     text_obj = c.beginText()
    #     text_obj.setTextOrigin(inch, inch)
    #     text_obj.setFont('Helvetica2', 14)
    #     text_obj.textLine('Список покупок:')
    #     shopping_cart_list = get_shopping_cart(request.user)
    #     lines = ['', ]
    #     for ingr in shopping_cart_list:
    #         lines.append(
    #             f"{ingr['ingredient__name']} - {ingr['amount']} "
    #             f"{ingr['ingredient__measurement_unit']}")
    #     for line in lines:
    #         text_obj.textLine(line)
    #     c.drawText(text_obj)
    #     c.showPage()
    #     c.save()
    #     buffer.seek(0)
    #     return FileResponse(
    #         buffer, as_attachment=True, filename='shopping_cart.pdf'
    #     )
