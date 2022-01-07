# Generated by Django 4.0.1 on 2022-01-07 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('podcast_title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('pub_date', models.DateTimeField()),
                ('url', models.URLField()),
                ('image', models.URLField()),
                ('podcast_name', models.CharField(max_length=100)),
                ('podcast_network', models.CharField(max_length=150)),
                ('guid', models.CharField(max_length=50)),
            ],
        ),
    ]