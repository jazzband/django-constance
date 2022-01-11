from django.db import migrations, connection, DatabaseError


def _migrate_from_old_table(apps, schema_editor) -> None:
    """
    Copies values from old table.
    On new installations just ignore error that table does not exist.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO constance_constance ( id, key, value ) SELECT id, key, value FROM constance_config', [])
    except DatabaseError:
        pass


class Migration(migrations.Migration):

    dependencies = [('constance', '0002_auto_20190129_2304')]

    operations = [
        migrations.RunPython(_migrate_from_old_table),
    ]
