# Generated by Django 3.0.4 on 2020-04-10 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0024_auto_20200401_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcare',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='healthcare',
            name='lng',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='healthcare',
            name='region',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
