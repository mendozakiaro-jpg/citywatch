from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_report_options_report_date_updated_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('announcement_type', models.CharField(choices=[('news', 'News'), ('advisory', 'Advisory')], default='news', max_length=20)),
                ('is_published', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_published', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-date_published', '-date_created'],
            },
        ),
    ]