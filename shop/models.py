from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings
import numpy as np

# Create your models here.
slug_help_text = "Слаг - это короткая метка для представления страницы в URL. \
Содержит только буквы, цифры, подчеркивания или дефисы."


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField('Название категории', max_length=150, null=True)
    slug = models.SlugField(max_length=150, null=True, help_text=slug_help_text, db_index=True, unique=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField('Название', max_length=150, db_index=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


TYPES_OF_SEASON = [
    ('Всесезонные', 'Всесезонные'),
    ('Летние', 'Летние'),
    ('Зимние', 'Зимние'),
]

class Height(models.Model):
    height = models.FloatField('Высота', null=True, blank=True)

    def __str__(self):
        return str(self.height)

    class Meta:
        verbose_name = 'Высота'
        verbose_name_plural = 'Высота'
class Width(models.Model):
    width = models.FloatField('Ширина', null=True, blank=True)

    def __str__(self):
        return str(self.width)

    class Meta:
        verbose_name = 'Ширина'
        verbose_name_plural = 'Ширина'
class Diameter(models.Model):
    diameter = models.CharField('Диаметер', max_length=3, null=True, blank=True)

    def __str__(self):
        return str(self.diameter)

    class Meta:
        verbose_name = 'Диаметер'
        verbose_name_plural = 'Диаметер'

class NumberOfHoles(models.Model):
    number_of_holes = models.FloatField('Число отверстий', null=True, blank=True)

    def __str__(self):
        return str(self.number_of_holes)

    class Meta:
        verbose_name = 'Число отверстий'
        verbose_name_plural = 'Число отверстий'

class DiameterOfHoles(models.Model):
    diameter_of_holes = models.FloatField('Диаметр отверстий', null=True, blank=True)


    def __str__(self):
        return str(self.diameter_of_holes)

    class Meta:
        verbose_name = 'Диаметер отверстий'
        verbose_name_plural = 'Диаметер отверстий'
class Color(models.Model):
    color = models.CharField('Цвет', max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.color)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвет'
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Категория')
    name = models.CharField('Название продукта', max_length=150, null=True)
    # slug = models.SlugField(max_length=150, null=True, help_text=slug_help_text, db_index=True, unique=True)
    description = RichTextField('Польное описание', blank=True, null=True)
    short = models.TextField('Короткое описание', blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    # sale_price = models.DecimalField('Скидочная цена', max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField('Доступно', default=True)
    stock = models.PositiveIntegerField('Количество')
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    views = models.IntegerField('Просмотры', default=0, blank=True, null=True)
    manufacturer = models.CharField('Производитель', max_length=255, null=True)
    # tire
    season = models.CharField('Сезонность', max_length=15, choices=TYPES_OF_SEASON, null=True, blank=True)
    # height = models.FloatField('Высота', null=True, blank=True)
    height = models.ForeignKey(Height, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Высота')
    # both
    # width = models.FloatField('Ширина', null=True, blank=True)
    # diameter = models.CharField('Диаметер', max_length=3, null=True, blank=True)
    width = models.ForeignKey(Width, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ширина')
    diameter = models.ForeignKey(Diameter, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Диаметр')
    # disk
    # number_of_holes = models.FloatField('Число отверстий', null=True, blank=True)
    # diameter_of_holes = models.FloatField('Диаметр отверстий', null=True, blank=True)
    # color = models.CharField('Цвет', max_length=100, null=True, blank=True)
    number_of_holes = models.ForeignKey(NumberOfHoles, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Число отверстий')
    diameter_of_holes = models.ForeignKey(DiameterOfHoles, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Диаметр отверстий')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Цвет')


    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        # abstract = True

    def __str__(self):
        return self.name

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        avg_rating = np.mean(list(all_ratings))
        if str(avg_rating) == 'nan':
            return 0
        return round(avg_rating)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='products/tires/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.product.name)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


# class DiskImage(models.Model):
#     disk = models.ForeignKey(Disk, related_name='image', on_delete=models.CASCADE)
#     image_path = models.ImageField(upload_to='products/disk/%Y/%m/%d', blank=True, null=True)
#
#     def __str__(self):
#         return '{}'.format(self.disk.name)
#
#     class Meta:
#         verbose_name = 'Фотография'
#         verbose_name_plural = 'Фотографии'


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    product_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='review')
    pub_date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField('Комментарий', max_length=250, null=True, blank=True)
    rating = models.PositiveIntegerField('Рейтинг', choices=RATING_CHOICES)

    def __str__(self):
        return f"{self.user} - {self.product}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'