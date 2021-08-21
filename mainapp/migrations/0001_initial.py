# Generated by Django 3.2.6 on 2021-08-20 13:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('acc_number', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('balance', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_amount', models.PositiveBigIntegerField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(max_length=10)),
                ('acc_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer')),
            ],
        ),
    ]
