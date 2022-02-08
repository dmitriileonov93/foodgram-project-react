from django.db.models import Sum
from app.models import IngredientInRecipe


def get_shopping_cart(user):
    shopping_cart_queryset = IngredientInRecipe.objects.filter(
        recipe__recipe_in_cart__user=user)
    shopping_cart_list = shopping_cart_queryset.values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    return shopping_cart_list
