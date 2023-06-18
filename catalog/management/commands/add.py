import json, os
from django.core.management import BaseCommand, call_command
from config import config
import psycopg2
from pprint import pprint
from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):

        params = config()
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"DROP DATABASE project")
        except psycopg2.errors.InvalidCatalogName:
            print(f'psycopg2.errors.InvalidCatalogName: ОШИБКА:  база данных django_project не существует')
        try:
            cur.execute(f"CREATE DATABASE django_project")
        except psycopg2.errors.DuplicateDatabase:
            print('ОШИБКА:  отношение "main_category" не существует')
        conn.close()

        os.system("python manage.py migrate")

        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            f.close()

        category_list = []
        for category in data:
            category_list.append(Category(**category["fields"]))
        Category.objects.bulk_create(category_list)



