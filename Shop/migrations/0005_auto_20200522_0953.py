# Generated by Django 3.0.6 on 2020-05-22 09:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0004_auto_20200522_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sneakersinstance',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
