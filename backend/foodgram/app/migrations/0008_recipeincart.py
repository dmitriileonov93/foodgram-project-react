# Generated by Django 2.2.19 on 2022-02-02 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0007_recipeinfavorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeInCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(blank=True, help_text='Рецепт в корзину покупок', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_in_cart', to='app.Recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(blank=True, help_text='Тот, кто добавил в корзину', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_follower', to=settings.AUTH_USER_MODEL, verbose_name='Пользоватеть')),
            ],
            options={
                'verbose_name': 'Список',
                'verbose_name_plural': 'Списки',
            },
        ),
    ]
