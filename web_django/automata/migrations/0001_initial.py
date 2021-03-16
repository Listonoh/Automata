# Generated by Django 3.1.7 on 2021-03-16 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Automata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('json_specification', models.JSONField()),
                ('published_date', models.DateField(verbose_name='date published')),
            ],
        ),
    ]
