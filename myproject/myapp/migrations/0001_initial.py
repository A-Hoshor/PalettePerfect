# Generated by Django 5.0.3 on 2024-03-24 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('numberOfColors', models.IntegerField()),
                ('originalImage', models.ImageField(upload_to='originalImage/')),
                ('simplifiedImage', models.ImageField(upload_to='simplifiedImage/')),
            ],
        ),
    ]