# Generated by Django 4.1 on 2022-10-23 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=25)),
                ('condition', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('title', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to=None)),
            ],
        ),
    ]
