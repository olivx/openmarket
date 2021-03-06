# Generated by Django 3.2.6 on 2021-08-08 21:42
from pathlib import Path

from django.db import migrations

from api.services.load_data import LoadData


def load_data(apps, schema_editor):
    """load data on migrate"""
    file_data_csv = Path(__file__).parents[2] / "contrib" / "open-markets-data.csv"
    LoadData(file=str(file_data_csv)).execute()


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [migrations.RunPython(load_data)]
