# Generated by Django 5.0 on 2024-01-31 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=254)),
                ('email', models.CharField(max_length=254)),
                ('name', models.CharField(max_length=254)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
    ]
