# Generated by Django 4.0.6 on 2022-08-11 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_askmoney_avans_payment_remove_story_proekt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='askmoney',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]