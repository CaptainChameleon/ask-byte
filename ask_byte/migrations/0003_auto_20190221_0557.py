# Generated by Django 2.1.7 on 2019-02-21 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask_byte', '0002_auto_20190221_0546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questioncategory',
            old_name='category_name',
            new_name='name',
        ),
    ]