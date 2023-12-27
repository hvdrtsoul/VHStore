# Generated by Django 4.2.8 on 2023-12-26 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VHStore', '0004_alter_membershipstatus_name_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VHStore.membershipstatus'),
        ),
        migrations.AddField(
            model_name='user',
            name='total_purchases',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='UserPlan',
        ),
    ]
