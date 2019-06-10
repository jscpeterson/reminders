# Generated by Django 2.1.5 on 2019-06-10 16:19

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
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('case_number', models.CharField(max_length=20, unique=True)),
                ('track', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], null=True)),
                ('arraignment_date', models.DateTimeField(null=True)),
                ('scheduling_conference_date', models.DateTimeField(null=True)),
                ('pti_request_date', models.DateTimeField(null=True)),
                ('trial_date', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_case_items', to=settings.AUTH_USER_MODEL)),
                ('paralegal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paralegal', to=settings.AUTH_USER_MODEL)),
                ('prosecutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prosecutor', to=settings.AUTH_USER_MODEL)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_case_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('type', models.IntegerField(choices=[(0, 'FFA'), (1, 'Scheduling Conference'), (2, 'Witness List'), (3, 'Defense Request PTIs'), (4, 'Defense Conduct PTIs'), (5, 'Witness PTIs'), (6, 'Scientific Evidence'), (7, 'Pretrial Motion Filing'), (8, 'Pretrial Motion Response'), (9, 'Pretrial Motion Hearing'), (10, 'Pretrial Conference'), (11, 'Final Witness List'), (12, 'Need for Interpreter'), (13, 'Plea Agreement'), (14, 'Trial')])),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Complete'), (2, 'Expired')], default=0)),
                ('datetime', models.DateTimeField()),
                ('reminders_sent', models.IntegerField(default=0)),
                ('invalid_notice_sent', models.BooleanField(default=False)),
                ('invalid_judge_approved', models.BooleanField(default=False)),
                ('invalid_extension_filed', models.BooleanField(default=False)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='remind.Case')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_deadline_items', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_deadline_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Motion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'In Limine'), (1, 'Review Conditions of Release'), (2, 'Motion to Suppress Witness'), (3, 'Motion to Suppress Evidence'), (4, 'Motion to Suppress Witness and Evidence'), (5, 'Motion to Dismiss'), (6, 'Motion to Suppress and Dismiss'), (7, 'Motion to Extend Deadline'), (8, 'Motion to Reconsider'), (9, 'Other')])),
                ('date_received', models.DateTimeField()),
                ('response_deadline', models.DateTimeField()),
                ('response_filed', models.DateTimeField()),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='remind.Case')),
            ],
        ),
    ]
