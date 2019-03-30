import csv
import zipfile
import tempfile

from .models import *


def generate_temp_csv_from_queryset_values(queryset):
    file = tempfile.TemporaryFile(mode='r+')
    writer = csv.DictWriter(file, queryset[0].keys())
    writer.writeheader()
    for model_values in queryset:
        writer.writerow(model_values)
    file.seek(0)
    return file


def generate_temp_zipfile(archive_names, file_data):
    file = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(file, 'w', zipfile.ZIP_DEFLATED)
    for archive_name, data in zip(archive_names, file_data):
        archive.writestr(archive_name, data)
    archive.close()
    file.seek(0)
    return file
