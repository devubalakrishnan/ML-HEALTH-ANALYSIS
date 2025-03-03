# Generated by Django 3.1.3 on 2022-07-16 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0011_auto_20220716_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkup',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkup',
            name='scan_path',
            field=models.ImageField(null=True, upload_to='ecg scan'),
        ),
        migrations.AddField(
            model_name='checkup',
            name='verified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='health.doctor'),
        ),
        migrations.DeleteModel(
            name='Disease_prediction',
        ),
    ]
