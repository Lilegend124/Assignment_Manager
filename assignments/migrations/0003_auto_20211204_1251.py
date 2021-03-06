# Generated by Django 3.2.9 on 2021-12-04 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_document_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='document',
            name='class_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignments.class_item'),
        ),
    ]
