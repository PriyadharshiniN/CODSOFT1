# Generated by Django 5.0.4 on 2024-04-19 06:32

import Shopping_App.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to=Shopping_App.models.getFileName)),
                ('description', models.TextField(max_length=500)),
                ('status', models.BooleanField(default=False, help_text='0-show,1-hidden')),
                ('trending', models.BooleanField(default=False, help_text='0-default, 1-trending')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('vendor', models.CharField(max_length=150)),
                ('product_image', models.ImageField(upload_to=Shopping_App.models.getFileName)),
                ('quantity', models.FloatField()),
                ('original_price', models.FloatField()),
                ('selling_price', models.FloatField()),
                ('description', models.TextField(max_length=500)),
                ('status', models.BooleanField(default=False, help_text='0-show,1-hidden')),
                ('trending', models.BooleanField(default=False, help_text='0-default, 1-trending')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('catagory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shopping_App.catagory')),
            ],
        ),
    ]
