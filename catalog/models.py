from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}, {self.description}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за покупку')
    create_date = models.DateField(verbose_name='Дата создания', null=True, blank=True)
    change_date = models.DateField(verbose_name='Дата последнего изменения', null=True, blank=True)

    def __str__(self):
        return f'{self.name}, {self.description}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Record(models.Model):
    record_title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(max_length=15000, verbose_name='Содержимое')
    preview = models.ImageField(upload_to='image/', verbose_name='Изображение', null=True, blank=True)
    date_of_creation = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    sign_of_publication = models.BooleanField(default=True, verbose_name='активный')
    views = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.record_title}'

    def get_absolute_url(self):
        return reverse('record_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
        ordering = ('record_title', 'slug', 'date_of_creation', 'sign_of_publication')

    def increase_views(self):
        self.views += 1
        self.save()


class Version(models.Model):
    product_name = models.CharField(max_length=150, verbose_name='Наименование')
    number_ver = models.IntegerField(default=0.0, verbose_name='Номер версии')
    name_ver = models.CharField(max_length=150, verbose_name='Наименование версии')
    flag_ver = models.CharField(max_length=150, verbose_name='Признак текущей версии')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return f'{self.product} {self.number_ver}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
