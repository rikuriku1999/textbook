# Generated by Django 3.0 on 2020-02-17 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('textapp', '0003_auto_20200217_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroommodel',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='textapp.Usermodel'),
        ),
    ]