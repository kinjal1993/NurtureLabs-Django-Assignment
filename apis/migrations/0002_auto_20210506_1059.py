# Generated by Django 3.0.7 on 2021-05-06 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisor',
            name='photo',
            field=models.ImageField(upload_to='router_specifications'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_time', models.DateTimeField()),
                ('advisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.Advisor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.User')),
            ],
        ),
    ]
