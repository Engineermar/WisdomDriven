# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-04 13:44
from __future__ import unicode_literals

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
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.CharField(db_index=True, max_length=150)),
                ('industry', models.IntegerField(choices=[(1, 'fuel'), (2, 'nondurable manfacturer'), (3, 'tech'), (4, 'retail'), (5, 'wholesale trade'), (6, 'state_military_federal'), (7, 'other')], max_length=50, null=True)),
                ('business_id', models.CharField(max_length=25, null='True')),
                ('date_established', models.DateField(max_length=500, null=True)),
                ('logo', models.ImageField(null=True, upload_to='')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='business', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MISC', models.TextField(blank=True)),
                ('order_id', models.CharField(max_length=25, null=True)),
                ('order_created', models.DateField(null=True)),
                ('service_type', models.IntegerField(choices=[(0, 'pickup'), (1, 'delivery')], max_length=50, null=True)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('distance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hazmat_class', models.IntegerField(choices=[(1, 'Non-hazard'), (2, 'Explosive'), (3, 'Gases'), (4, 'Flammable Liquid'), (5, 'Combustible Liquid'), (6, 'Flammable Solid'), (7, 'Spontanaeously Combustible'), (8, 'Dangerous When Wet'), (10, 'Oxidizer and Organic Peroxide'), (11, 'Poison (Toxic) and Poison Inhalation Hazard'), (12, 'Radioactive'), (models.TextField(blank=True), 'Miscellaneous, and the general Dangerous placard')], max_length=50, null=True)),
                ('business_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='b_id_set', to='wdapp.Business')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.CharField(max_length=9, null='True')),
                ('company', models.CharField(max_length=500, null=True)),
                ('trucking_specilization', models.IntegerField(choices=[('Fuel', 'fuel'), ('Manfacturer', 'manfacturer'), ('Technology', 'Technology'), ('Retail', 'retail'), ('Wholesale', 'wholesale'), ('Goverment', 'goverment'), ('Other', 'other')], max_length=50, null=True)),
                ('date_established', models.DateField(max_length=500, null=True)),
                ('logo', models.ImageField(null=True, upload_to='')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_id', models.CharField(max_length=25, null='True')),
                ('date_of_birth', models.DateField(null=True)),
                ('ssn', models.CharField(db_index=True, max_length=9, null=True)),
                ('wage_plan', models.IntegerField(choices=[('Hourly', 'hourly'), ('Miles', 'miles')], max_length=50, null=True)),
                ('license', models.IntegerField(choices=[('A', 'class a'), ('B', 'class b'), ('C', 'class c')], max_length=50, null=True)),
                ('other_license', models.IntegerField(choices=[('A', 'class a'), ('B', 'class b'), ('C', 'class c')], max_length=50, null=True)),
                ('other_license_2', models.IntegerField(choices=[('A', 'class a'), ('B', 'class b'), ('C', 'class c')], max_length=50, null=True)),
                ('license_number', models.IntegerField(null=True)),
                ('date_hired', models.DateField(null=True)),
                ('company', models.ForeignKey(null='True', on_delete=django.db.models.deletion.CASCADE, related_name='driver_id', to='wdapp.Company')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DriverExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expenses_id', models.CharField(max_length=25, null=True)),
                ('expense_type', models.CharField(choices=[(1, 'fuel'), (2, 'meal'), (3, 'emergency'), (4, 'other')], max_length=50, null=True)),
                ('amount_of_expense', models.CharField(default=0, max_length=50, null=True)),
                ('driver_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driverexpenses_driver_id_set', to='wdapp.BusinessOrder')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wdapp.BusinessOrder')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wdapp.Company')),
                ('date_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderstatus_date_created_set', to='wdapp.BusinessOrder')),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_id', models.CharField(blank='True', max_length=25, null='True')),
                ('stop_type', models.CharField(choices=[(1, 'fuel'), (2, 'meal'), (3, 'restroom'), (4, 'lodging'), (5, 'accident'), (6, 'other')], max_length=50, null=True)),
                ('time_stop', models.TimeField(auto_now_add=True)),
                ('departed_stop', models.TimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_id', models.CharField(max_length=25, null=True)),
                ('date', models.DateField(null=True)),
                ('estimated_arrival', models.DateField(blank=True, null=True)),
                ('trailer_license', models.CharField(max_length=7, null=True)),
                ('beginnning_weather_conditions', models.IntegerField(choices=[(1, 'normal'), (2, 'cloudy'), (3, 'rain'), (4, 'snow'), (5, 'hazardous'), (6, 'extremly hazardous')], max_length=50, null=True)),
                ('midway_weather_conditions', models.IntegerField(choices=[(1, 'normal'), (2, 'cloudy'), (3, 'rain'), (4, 'snow'), (5, 'hazardous'), (6, 'extremly hazardous')], max_length=50, null=True)),
                ('ending_weather_conditions', models.IntegerField(choices=[(1, 'normal'), (2, 'cloudy'), (3, 'rain'), (4, 'snow'), (5, 'hazardous'), (6, 'extremly hazardous')], max_length=50, null=True)),
                ('fuel_card_usage', models.IntegerField(choices=[('Yes', 'yes'), ('No', 'no')], max_length=50, null=True)),
                ('average_price_per_gallon', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('gallons_of_gas_used', models.IntegerField(null=True)),
                ('number_of_unscheduled', models.IntegerField(null=True)),
                ('total_miles_traveled', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('order_details', models.TextField(null=True)),
                ('business_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trips_driver_id_set', to='wdapp.BusinessOrder')),
                ('company_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trips_company_id_set', to='wdapp.BusinessOrder')),
                ('estimated_trip_distance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estimated_distance_set', to='wdapp.BusinessOrder')),
                ('order_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trips_order_created_set', to='wdapp.BusinessOrder')),
            ],
        ),
        migrations.AddField(
            model_name='stop',
            name='driver_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stop_driver_id_set', to='wdapp.Trip'),
        ),
        migrations.AddField(
            model_name='stop',
            name='trip_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stop_trip_id_set', to='wdapp.Trip'),
        ),
        migrations.AddField(
            model_name='orderstatus',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderstatus_name_set', to='wdapp.Trip'),
        ),
        migrations.AddField(
            model_name='orderstatus',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderstatus_order_id_set', to='wdapp.BusinessOrder'),
        ),
        migrations.AddField(
            model_name='orderstatus',
            name='service_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderstatus_service_type_set', to='wdapp.BusinessOrder'),
        ),
        migrations.AddField(
            model_name='driverexpense',
            name='stop_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driverexpenses_stop_id_set', to='wdapp.Stop'),
        ),
        migrations.AddField(
            model_name='businessorder',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_set', to='wdapp.Company'),
        ),
    ]
