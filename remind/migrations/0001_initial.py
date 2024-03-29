# Generated by Django 2.2.4 on 2019-08-08 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('type', models.IntegerField(choices=[(0, 'FFA'), (1, 'Scheduling Conference'), (2, 'Initial Witness List'), (3, 'PTIs Requested'), (4, 'PTIs Conducted'), (5, 'Witness PTIs'), (6, 'Scientific Evidence'), (7, 'Pretrial Motion Filing'), (8, 'Pretrial Motion Response'), (9, 'Pretrial Motion Hearing'), (10, 'PTC/Docket Call'), (11, 'Final Witness List'), (12, 'Need for Interpreter'), (13, 'Plea Agreement'), (14, 'Trial')])),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Complete'), (2, 'Expired')], default=0)),
                ('datetime', models.DateTimeField()),
                ('reminders_sent', models.IntegerField(default=0)),
                ('invalid_notice_sent', models.BooleanField(default=False)),
                ('invalid_judge_approved', models.BooleanField(default=False)),
                ('invalid_extension_filed', models.BooleanField(default=False)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cases.Case')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_deadline_items', to=settings.AUTH_USER_MODEL)),
                ('motion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cases.Motion')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_deadline_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
