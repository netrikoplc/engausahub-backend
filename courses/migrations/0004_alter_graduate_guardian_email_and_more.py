# Generated by Django 4.2.4 on 2023-09-27 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_graduate_options_alter_graduate_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduate',
            name='guardian_email',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='graduate',
            name='guardian_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='graduate',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
