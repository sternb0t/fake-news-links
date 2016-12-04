# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FakeNewsLinkAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='fakenewslink',
            name='attributes',
            field=models.ManyToManyField(blank=True, to='api.FakeNewsLinkAttribute'),
        ),
    ]