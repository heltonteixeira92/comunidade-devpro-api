# Generated by Django 4.1.2 on 2023-04-26 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_author_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
