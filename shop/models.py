from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings

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

class Width(models.Model):
    width = models.FloatField('Ширина', null=True, blank=True)

    def __str__(self):
        return str(self.width)

class Diameter(models.Model):
    diameter = models.CharField('Диаметер', max_length=3, null=True, blank=True)

    def __str__(self):
        return str(self.diameter)



class NumberOfHoles(models.Model):
    number_of_holes = models.FloatField('Число отверстий', null=True, blank=True)

    def __str__(self):
        return str(self.number_of_holes)


class DiameterOfHoles(models.Model):
    diameter_of_holes = models.FloatField('Диаметр отверстий', null=True, blank=True)


    def __str__(self):
        return str(self.diameter_of_holes)
class Color(models.Model):
    color = models.CharField('Цвет', max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.color)

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
