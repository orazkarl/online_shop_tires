from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings

# Create your models here.
slug_help_text = "Слаг - это короткая метка для представления страницы в URL. \
Содержит только буквы, цифры, подчеркивания или дефисы."


# class Category(models.Model):
#     class Meta:
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'
#
#     title = models.CharField('Название категории', max_length=150, null=True)
#     slug = models.SlugField(max_length=150, null=True, help_text=slug_help_text, db_index=True, unique=True)
#     description = models.TextField(blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.title


class Tag(models.Model):
    name = models.CharField('Название', max_length=150, db_index=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Product(models.Model):
    # category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Категория')
    detailpageurl = models.TextField(blank=True, null=True)
    name = models.CharField('Название продукта', max_length=150, null=True)
    slug = models.SlugField(max_length=150, null=True, help_text=slug_help_text, db_index=True, unique=True)
    description = RichTextField('Польное описание', blank=True, null=True)
    short = models.TextField('Короткое описание', blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    sale_price = models.DecimalField('Скидочная цена', max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField('Доступно', default=True)
    stock = models.PositiveIntegerField('Количество')
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    views = models.IntegerField('Просмотры', default=0, blank=True, null=True)
    manufacturer = models.CharField('Производитель', max_length=255, null=True)

    class Meta:
        # verbose_name = 'Продукт'
        # verbose_name_plural = 'Продукты'
        abstract = True

    # def __str__(self):
    #     return self.name


class Tire(Product):
    TYPES_OF_SEASON = [
        ('В', 'Всесезонные'),
        ('Л', 'Летние'),
        ('З', 'Зимние'),
    ]
    season = models.CharField('Сезонность', max_length=15, choices=TYPES_OF_SEASON, null=True, blank=True)
    width = models.FloatField('Ширина', null=True, blank=True)
    height = models.FloatField('Высота', null=True, blank=True)
    diameter = models.CharField('Диаметер', max_length=3, null=True, blank=True)

    class Meta:
        verbose_name = 'Шина'
        verbose_name_plural = 'Шины'

    def __str__(self):
        return self.name


class Disk(Product):
    width = models.FloatField('Ширина', null=True, blank=True)
    diameter = models.FloatField('Диаметр', null=True, blank=True)
    number_of_holes = models.FloatField('Число отверстий', null=True, blank=True)
    diameter_of_holes = models.FloatField('Диаметр отверстий', null=True, blank=True)
    color = models.CharField('Цвет', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Диск'
        verbose_name_plural = 'Диски'

    def __str__(self):
        return self.name


class TireImage(models.Model):
    tire = models.ForeignKey(Tire, related_name='image', on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='products/tires/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.tire.name)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

class DiskImage(models.Model):
    disk = models.ForeignKey(Disk, related_name='image', on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='products/disk/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.disk.name)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

# class Wishlist(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     wished_item = models.ForeignKey(Product, on_delete=models.CASCADE)
#     added_date = models.DateTimeField(auto_now_add=True)
