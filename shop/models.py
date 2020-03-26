from django.db import models
from ckeditor.fields import RichTextField

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


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Категория')
    detailpageurl = models.TextField(blank=True, null=True)
    name = models.CharField('Название продукта', max_length=150, null=True)
    slug = models.SlugField(max_length=150, null=True, help_text=slug_help_text, db_index=True, unique=True)
    description = RichTextField('Польное описание', blank=True, null=True)
    short = models.TextField('Короткое описание',blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    sale_price = models.DecimalField('Скидочная цена', max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField('Доступно', default=True)
    stock = models.PositiveIntegerField('Количество')
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    views = models.IntegerField('Просмотры', default=0, blank=True, null=True)
    manufacturer = models.CharField('Производитель',max_length=255, null=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.image.name)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'