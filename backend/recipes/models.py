from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг тега',
        unique=True,
        max_length=200,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}: {self.color}'
    

class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='\nRepeat ingredient\n',
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
            models.CheckConstraint(
                check=models.Q(measurement_unit__length__gt=0),
                name='\n%(app_label)s_%(class)s_measurement_unit is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'
    

class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        related_name='recipes',
        through='recipes.AmountIngredient',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    #image = картинка в Dase64
    text = models.TextField(
        verbose_name='Описание',
        max_length=2000,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_for_author',
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.author.get_username}: {self.name}'
    

class AmountIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='В каких рецептах',
        related_name='ingredient',
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name='Связанные ингредиенты',
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe', )
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredients', ),
                name='\n%(app_label)s_%(class)s ingredient alredy added\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredients}'
    

class Favorites(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранные рецепты',
        related_name='in_favorites',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user', ),
                name='\n%(app_label)s_%(class)s recipe is favorite alredy\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'
    

class Carts(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты в списке покупок',
        related_name='in_carts',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Владелец списка',
        related_name='carts',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user', ),
                name='\n%(app_label)s_%(class)s recipe is cart alredy\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'