# Generated by Django 4.2.4 on 2023-09-26 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_transaction', to='courses.enrollment')),
            ],
            options={
                'verbose_name': 'course transaction',
                'verbose_name_plural': 'course transactions',
                'unique_together': {('enrollment', 'reference', 'created_at')},
            },
        ),
    ]
