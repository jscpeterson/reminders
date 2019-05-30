# Generated by Django 2.1.5 on 2019-05-30 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_number', models.CharField(max_length=20, unique=True)),
                ('track', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], null=True)),
                ('arraignment_date', models.DateTimeField(null=True)),
                ('scheduling_conference_date', models.DateTimeField(null=True)),
                ('pti_request_date', models.DateTimeField(null=True)),
                ('trial_date', models.DateTimeField(null=True)),
                ('paralegal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paralegal', to=settings.AUTH_USER_MODEL)),
                ('prosecutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prosecutor', to=settings.AUTH_USER_MODEL)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'FFA'), (1, 'Scheduling Conference'), (2, 'Witness List'), (3, 'Request PTIs'), (4, 'Conduct Initial PTIs'), (5, 'Winess PTIs'), (6, 'Scientific Evidence'), (7, 'Pretrial Motion Filing'), (8, 'Pretrial Motion Response'), (9, 'Pretrial Motion Hearing'), (10, 'Pretrial Conference'), (11, 'Final Witness List'), (12, 'Need for Interpreter'), (13, 'Plea Agreement'), (14, 'Trial')])),
                ('datetime', models.DateTimeField()),
                ('expired', models.BooleanField(default=False)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='remind.Case')),
            ],
        ),
        migrations.CreateModel(
            name='Motion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
