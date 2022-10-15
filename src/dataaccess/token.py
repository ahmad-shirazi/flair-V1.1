from src.util.db import executeval, fetch, execute
from src.util.misc import Token
from src.util.time import get_current_time
from src.config.enum import TABLE_NAMES


async def _get_result(query):
    result = await fetch(query)
    return [Token(token_id=row['id'], file_key=row['fileKey'], key=row['key'], value=row['value'],
                  created_at=row['createdAt'], updated_at=row['updatedAt'])
            for row in result]


async def insert(token_data):
    model_name = TABLE_NAMES['token']
    token_data.createdAt = get_current_time()
    field_names = ['fileKey', 'key', 'value', 'createdAt', 'updatedAt']
    values_string = ','.join(['$' + str(idx + 1) for idx, _ in enumerate(field_names)])
    values = [getattr(token_data, field_name) for field_name in field_names]

    fields_string = ','.join(['"' + field + '"' for field in field_names])

    query = '''
        INSERT INTO "{model_name}" ({fields_string}) VALUES ({values_str})
        '''.format(
        model_name=model_name,
        fields_string=fields_string,
        values_str=values_string
    )
    await executeval(query, values)


async def fetch_by_file_key(file_key):
    model_name = TABLE_NAMES['token']
    query = '''SELECT  "id", "fileKey", "key", "value", "createdAt", "updatedAt"
    FROM "{model_name}"
    WHERE "fileKey" = '{file_key}'
    '''.format(file_key=file_key, model_name=model_name)

    result = await _get_result(query)
    return result


async def fetch_by_id(token_id):
    model_name = TABLE_NAMES['token']

    query = '''SELECT  "id", "fileKey", "key", "value", "createdAt", "updatedAt"
    FROM "{model_name}"
    WHERE "id" = '{token_id}'
    '''.format(token_id=token_id, model_name=model_name)

    result = await _get_result(query)
    return result
