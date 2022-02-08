from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

from users.models import User


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.CharField('Название', max_length=200)
    color = ColorField('Цвет', default='#FF0000')
    slug = models.SlugField('Slug', max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    name = models.CharField('Название', max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    text = models.CharField('Текст', max_length=256)
    image = models.ImageField(
        upload_to='media/recipes/images/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    cooking_time = models.IntegerField('Время приготовления', validators=[
        MinValueValidator(
            limit_value=1,
            message='Не менее 1'
        ),
    ])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeInFavorite(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='favoriter',
        verbose_name='Подписчик',
        help_text='Тот, кто добавил в избранное')
    recipe = models.ForeignKey(
        Recipe,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='favoriting',
        verbose_name='Рецепт',
        help_text='Избранный рецепт')

    def __str__(self):
        return f'Избранное {self.user.username}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class RecipeInCart(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='cart_follower',
        verbose_name='Пользоватеть',
        help_text='Тот, кто добавил в корзину')
    recipe = models.ForeignKey(
        Recipe,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='recipe_in_cart',
        verbose_name='Рецепт',
        help_text='Рецепт в корзину покупок')

    def __str__(self):
        return f'Корзина покупок {self.user.username}'

    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Списки'


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    amount = models.PositiveIntegerField('Количество ингредиента')

    def __str__(self):
        return f'{self.recipe}, {self.ingredient}, {self.amount}'

    class Meta:
        verbose_name = 'Связь "Ингридиент - Рецепт"'
        verbose_name_plural = 'Связи "Ингридиент - Рецепт"'
