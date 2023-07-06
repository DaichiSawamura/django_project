from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return f'{self.name}, {self.description}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    ACTIV = 'Активна'
    NO_ACTIV = 'Не активна'

    SELECT_STATUS = [
        (ACTIV, 'Активна'),
        (NO_ACTIV, 'Не активна'),
    ]

    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание', null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', null=True, blank=True)
    category = models.ForeignKey(verbose_name='Категория', to='Category', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена за покупку')
    create_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    change_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата последнего изменения')
    user = models.CharField(max_length=50, verbose_name='Создатель', null=True, blank=True)
    status = models.CharField(max_length=50, default=NO_ACTIV, choices=SELECT_STATUS, verbose_name='Статус')

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.record_title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
        ordering = ('record_title', 'slug', 'date_of_creation', 'sign_of_publication')

    def increase_views(self):
        self.views += 1
        self.save()


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number = models.IntegerField(unique=True, verbose_name='номер версии')
    name = models.CharField(max_length=150, verbose_name='Название версии')
    sign_of_publication = models.BooleanField(default=True, verbose_name='активный')

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
