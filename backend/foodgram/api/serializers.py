from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from app.models import (Ingredient, IngredientInRecipe, Recipe, RecipeInCart,
                        RecipeInFavorite, Tag)
from users.models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            return Follow.objects.filter(
                user=self.context['request'].user,
                author=obj
            ).exists()
        return False


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        me = self.context['request'].user
        if not me.check_password(value):
            raise serializers.ValidationError('Неверный пароль!')
        return value


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngredientInRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), required=True,
        source='ingredient.id'
    )

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredientinrecipe_set', many=True, read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            return RecipeInFavorite.objects.filter(
                user=self.context['request'].user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            return RecipeInCart.objects.filter(
                user=self.context['request'].user, recipe=obj).exists()
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipeCreateSerializer(
        source='ingredientinrecipe_set', many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        author = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientinrecipe_set')
        recipe = Recipe.objects.create(**validated_data, author=author)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            current_ingredient = ingredient['ingredient']['id']
            IngredientInRecipe.objects.create(
                ingredient=current_ingredient, recipe=recipe,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        print(validated_data)
        if 'ingredientinrecipe_set' in validated_data:
            instance.ingredients.clear()
            ingredients = validated_data.pop('ingredientinrecipe_set')
            for ingredient in ingredients:
                current_ingredient = ingredient['ingredient']['id']
                IngredientInRecipe.objects.create(
                    ingredient=current_ingredient, recipe=instance,
                    amount=ingredient['amount']
                )
        if 'tags' in validated_data:
            instance.tags.set(validated_data.get('tags'))
        if 'name' in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if 'text' in validated_data:
            instance.text = validated_data.get('text', instance.text)
        if 'cooking_time' in validated_data:
            instance.cooking_time = validated_data.get(
                'cooking_time', instance.cooking_time)
        instance.save()
        return instance


class RecipeInSubscriptions(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionsSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        recipes = obj.recipes.all().order_by('-id')
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit):]
        return RecipeInSubscriptions(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        return True
