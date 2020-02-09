# Generated by Django 3.0 on 2020-01-30 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textapp', '0003_usermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='comment',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='textbookmodel',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='intro',
            field=models.TextField(blank=True, default=''),
        ),
    ]
