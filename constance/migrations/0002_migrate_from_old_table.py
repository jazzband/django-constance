from logging import getLogger

from django.core.management.color import no_style
from django.db import DatabaseError
from django.db import migrations

logger = getLogger(__name__)


def _migrate_from_old_table(apps, schema_editor) -> None:
    """
    Copies values from old table.
    On new installations just ignore error that table does not exist.
    """
    connection = schema_editor.connection
    quoted_string = ', '.join([connection.ops.quote_name(item) for item in ['id', 'key', 'value']])
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f'INSERT INTO constance_constance ( {quoted_string} ) SELECT {quoted_string} FROM constance_config',  # noqa: S608
                [],
            )
            cursor.execute('DROP TABLE constance_config', [])
    except DatabaseError:
        logger.exception('copy data from old constance table to a new one')

    Constance = apps.get_model('constance', 'Constance')
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Constance])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)


class Migration(migrations.Migration):
    dependencies = [('constance', '0001_initial')]

    atomic = False

    operations = [
        migrations.RunPython(_migrate_from_old_table, reverse_code=lambda x, y: None),
    ]
