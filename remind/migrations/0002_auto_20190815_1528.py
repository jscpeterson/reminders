# Generated by Django 2.2.4 on 2019-08-15 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remind', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deadline',
            name='type',
            field=models.IntegerField(choices=[(0, 'FFA'), (1, 'Scheduling Conference'), (2, 'Initial Witness List'), (3, 'PTIs Requested'), (4, 'PTIs Conducted'), (5, 'Witness PTIs'), (6, 'Scientific Evidence'), (7, 'Pretrial Motion Filing'), (8, 'Pretrial Motion Response'), (9, 'Pretrial Motion Hearing'), (10, 'Final Witness List'), (11, 'Need for Interpreter'), (12, 'Plea Agreement'), (13, 'Certification of Readiness'), (14, 'PTC/Docket Call'), (15, 'Trial')]),
        ),
    ]
