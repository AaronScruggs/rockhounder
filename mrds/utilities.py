import csv

from mrds.models import State


class MrdsDataImport:

    # Fields where CSV column name differs from model name.
    # ex. {'mrds csv name': 'model name'}
    NAME_COLUMN_DIFFS = {
        'url': 'mrds_url',
        'commod1': 'commodity_1',
        'commod2': 'commodity_2',
        'commod3': 'commodity_3',
        'oper_type': 'operation_type',
        'dev_stat': 'development_status',
        'model': 'geo_model',
        'names': 'alt_previous_names',
        'ore_ctrl': 'ore_control'
    }
    state_map = {}  # {california: 1}

    def __init__(self, file_name='mrds/data/mrds-f32003.txt'):
        super().__init__()
        with open(file_name, 'r') as file:
            d = csv.DictReader(file)
            self.rows = list(d)

        self.fk_func_dict = {
            'state': self.get_state_value,
            'county': None,
            'commodity_1': None,
            'commodity_2': None,
            'commodity_3': None,
            'operation_type': None,
            'development_status': None,
            'work_type': None,

        }
        self.fk_field_names = list(self.fk_func_dict.keys())

    def insert_data(self):
        # TODO: For starters only insert rows if they don't exist, don't update existing ones
        pass

    def get_state_value(self, value):
        obj, is_created = State.objects.get_or_create(name=value)
        return obj.id

    def get_fk_ptr(self, db_key, value):
        # TODO: track existing FK objects for all FK fields to avoid extraneous lookups
        fk_func = self.fk_func_dict.get(db_key)
        if not fk_func:
            return None

        fk_ptr = fk_func(value)
        return fk_ptr

    def process_row(self, row):
        # Convert csv field name to database field name
        data = {}
        for key in row.keys():
            if key in self.NAME_COLUMN_DIFFS:
                db_key = self.NAME_COLUMN_DIFFS[key]
            else:
                db_key = key
            value = row[key].lower()

            if db_key in self.fk_field_names:
                fk_ptr = self.get_fk_ptr(db_key, value)
                db_key_ptr = '{}_id'.format(db_key)
                data[db_key_ptr] = fk_ptr
            else:
                data[db_key] = value

        return data

