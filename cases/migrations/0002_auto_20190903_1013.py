# Generated by Django 2.2.4 on 2019-09-03 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='paralegal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paralegal', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='case',
            name='victim_advocate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='victim_advocate', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='case',
            name='secretary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secretary', to=settings.AUTH_USER_MODEL),
        ),
    ]
