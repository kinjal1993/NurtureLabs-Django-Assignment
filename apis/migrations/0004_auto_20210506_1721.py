# Generated by Django 3.0.7 on 2021-05-06 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_auto_20210506_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='advisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_advisors', to='apis.Advisor'),
        ),
    ]
