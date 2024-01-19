# Generated by Django 3.2.23 on 2024-01-15 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=20)),
                ('destination', models.CharField(max_length=20)),
                ('time', models.TimeField()),
                ('price', models.IntegerField()),
                ('seats_available', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('date_and_time_of_booking', models.DateTimeField(auto_now_add=True)),
                ('bus_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.bus')),
            ],
        ),
    ]