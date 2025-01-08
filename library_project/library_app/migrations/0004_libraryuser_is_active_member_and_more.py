# Generated by Django 5.1.4 on 2025-01-08 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0003_rename_copies_available_book_number_of_copies_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryuser',
            name='is_active_member',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='libraryuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
