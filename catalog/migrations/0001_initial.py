# Generated by Django 4.2.1 on 2023-06-13 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('description', models.CharField(max_length=150, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('description', models.CharField(max_length=150, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
                ('price', models.IntegerField(verbose_name='Цена за покупку')),
                ('create_date', models.DateField(blank=True, null=True, verbose_name='Дата создания')),
                ('change_date', models.DateField(blank=True, null=True, verbose_name='Дата последнего изменения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('slug', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='URL')),
                ('content', models.TextField(max_length=15000, verbose_name='Содержимое')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='image/', verbose_name='Изображение')),
                ('date_of_creation', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('sign_of_publication', models.BooleanField(default=True, verbose_name='активный')),
                ('views', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'запись',
                'verbose_name_plural': 'записи',
                'ordering': ('record_title', 'slug', 'date_of_creation', 'sign_of_publication'),
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('number_ver', models.IntegerField(default=0.0, verbose_name='Номер версии')),
                ('name_ver', models.CharField(max_length=150, verbose_name='Наименование версии')),
                ('flag_ver', models.CharField(max_length=150, verbose_name='Признак текущей версии')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'версия',
                'verbose_name_plural': 'версии',
            },
        ),
    ]
