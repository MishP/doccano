# Generated by Django 2.1.5 on 2019-05-02 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0013_gold_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='guideline',
            field=models.TextField(blank=True),
        ),
    ]
