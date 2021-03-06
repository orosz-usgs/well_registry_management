# The below suppresses pylint message: Module name "0003_country_lookups" doesn't conform to snake_case naming style
# pylint: disable-msg=C0103
# Enable check for the rest of the file
# pylint: enable-msg=C0103
"""
Migration for adding the country lookup table and
foreign key relationship with the registry table

"""
# Generated by Django 3.0.7 on 2020-06-26 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Country lookup migrations

    """

    dependencies = [
        ('registry', '0002_add_agency_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryLookup',
            fields=[
                ('country_cd', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('country_nm', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='registry',
            name='country_cd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.CountryLookup'),
        ),
    ]
