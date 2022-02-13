from django.contrib import admin

from .models import (Ingredient, IngredientInRecipe, Recipe, RecipeInCart,
                     RecipeInFavorite, Tag)


class IngredientInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('follow_count',)
    inlines = (IngredientInRecipeInline, )

    def follow_count(self, obj):
        return RecipeInFavorite.objects.filter(recipe=obj).count()

    follow_count.short_description = 'Кол-во добавлений в избранное'


class FavoriteAdmin(admin.ModelAdmin):
    list_filter = ('user', )
    list_display = ('user', 'recipe')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_filter = ('user', )
    list_display = ('user', 'recipe')


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name', )
    list_display = ('name', 'measurement_unit')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeInFavorite, FavoriteAdmin)
admin.site.register(RecipeInCart, ShoppingCartAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientInRecipe)
