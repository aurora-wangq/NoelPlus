# Generated by Django 4.2.1 on 2023-07-30 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='粉丝', to=settings.AUTH_USER_MODEL)),
                ('up', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='博主', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
