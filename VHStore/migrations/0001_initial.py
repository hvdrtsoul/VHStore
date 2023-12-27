# Generated by Django 4.2.8 on 2023-12-26 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MembershipStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('release_year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('buyer', 'Buyer'), ('seller', 'Seller'), ('administrator', 'Administrator')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_purchases', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VHStore.membershipstatus')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='VHStore.user')),
            ],
        ),
        migrations.CreateModel(
            name='Cassette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(choices=[('MINT', 'Mint'), ('GOOD', 'Good'), ('FAIR', 'Fair'), ('POOR', 'Poor')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VHStore.movie')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cassette', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='VHStore.cassette')),
                ('equipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='VHStore.equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(to='VHStore.cartitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VHStore.user')),
            ],
        ),
    ]