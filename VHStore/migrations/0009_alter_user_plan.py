# Generated by Django 4.2.8 on 2023-12-26 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VHStore', '0008_alter_membershipstatus_name_alter_user_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='plan',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='VHStore.membershipstatus'),
        ),
    ]