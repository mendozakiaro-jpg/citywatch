from django.db import migrations


def create_default_departments(apps, schema_editor):
    Department = apps.get_model('assignments', 'Department')
    departments = [
        ('Fire', 'Fire and emergency response'),
        ('Health', 'Health and medical services'),
        ('DPWH', 'Public works and infrastructure'),
        ('Barangay Tanod', 'Community safety and patrol'),
    ]
    for name, description in departments:
        Department.objects.get_or_create(name=name, defaults={'description': description})


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_departments, migrations.RunPython.noop),
    ]