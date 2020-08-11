import csv

from mrds.models import State, Commodity, OperationType, DevelopmentStatus, WorkType, County, Site


class MrdsDataImport:

    # Fields where CSV column name differs from model name.
    # ex. {'mrds csv name': 'model field name'}
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
    state_name_id_map = {}  # ex. {california: 1}
    county_name_id_map = {}
    commodity_name_id_map = {}
    operation_type_name_id_map = {}
    development_status_name_id_map = {}
    work_type_name_id_map = {}

    def __init__(self, file_name='mrds/data/mrds-f32003.txt'):
        super().__init__()
        with open(file_name, 'r') as file:
            d = csv.DictReader(file)
            self.rows = list(d)

        # Dict of functions to get values for foreign key fields.
        # County is excluded because it is handled separately
        self.fk_func_dict = {
            'state': self.get_state_value,
            'commodity_1': self.get_commodity_value,
            'commodity_2': self.get_commodity_value,
            'commodity_3': self.get_commodity_value,
            'operation_type': self.get_operation_type_value,
            'development_status': self.get_development_status_value,
            'work_type': self.get_work_type_value,

        }
        self.fk_field_names = list(self.fk_func_dict.keys())

    def process_row_data(self):
        for row in self.rows:
            data = self.get_row_db_data(row)
            dep_id = data.pop('dep_id', None)
            if dep_id:
                Site.objects.update_or_create(
                    dep_id=dep_id,
                    defaults=data
                )

    def get_state_value(self, csv_value):
        existing_database_value = self.state_name_id_map.get(csv_value)
        if existing_database_value:
            return existing_database_value

        obj, is_created = State.objects.get_or_create(name=csv_value)
        self.state_name_id_map[csv_value] = obj.id
        return obj.id

    def get_county_value(self, county_csv_value, state_csv_value):
        county_state_key = (county_csv_value, state_csv_value)
        existing_database_value = self.county_name_id_map.get(county_state_key)

        if existing_database_value:
            return existing_database_value

        state_id = self.get_state_value(state_csv_value)

        obj, is_created = County.objects.get_or_create(name=county_csv_value, state_id=state_id)
        self.state_name_id_map[county_state_key] = obj.id
        return obj.id

    def get_commodity_value(self, csv_value):
        existing_database_value = self.commodity_name_id_map.get(csv_value)
        if existing_database_value:
            return existing_database_value

        obj, is_created = Commodity.objects.get_or_create(name=csv_value)
        self.commodity_name_id_map[csv_value] = obj.id
        return obj.id

    def get_operation_type_value(self, csv_value):
        existing_database_value = self.operation_type_name_id_map.get(csv_value)
        if existing_database_value:
            return existing_database_value

        obj, is_created = OperationType.objects.get_or_create(name=csv_value)
        self.operation_type_name_id_map[csv_value] = obj.id
        return obj.id

    def get_development_status_value(self, csv_value):
        existing_database_value = self.development_status_name_id_map.get(csv_value)
        if existing_database_value:
            return existing_database_value

        obj, is_created = DevelopmentStatus.objects.get_or_create(name=csv_value)
        self.development_status_name_id_map[csv_value] = obj.id
        return obj.id

    def get_work_type_value(self, csv_value):
        existing_database_value = self.work_type_name_id_map.get(csv_value)
        if existing_database_value:
            return existing_database_value

        obj, is_created = WorkType.objects.get_or_create(name=csv_value)
        self.work_type_name_id_map[csv_value] = obj.id
        return obj.id

    def get_fk_ptr_value(self, db_field_name, csv_value):
        # Grab the appropriate func and get/create the ptr value for the given fk field 

        fk_func = self.fk_func_dict.get(db_field_name)
        if not fk_func:
            return None

        fk_ptr = fk_func(csv_value)
        return fk_ptr

    def get_row_db_data(self, row):

        data = {}
        for key in row.keys():

            # Convert csv field name to database field name
            if key in self.NAME_COLUMN_DIFFS:
                db_field_name = self.NAME_COLUMN_DIFFS[key]
            else:
                db_field_name = key
            csv_value = row[key].lower()

            if db_field_name == 'county':  # County is special case since it foreign keys to State
                fk_ptr = self.get_county_value(csv_value, row['state'].lower())
                data['county_id'] = fk_ptr
            elif db_field_name in self.fk_field_names:  # Get or create ptr value for FK field
                fk_ptr = self.get_fk_ptr_value(db_field_name, csv_value)
                db_field_name_ptr = '{}_id'.format(db_field_name)
                data[db_field_name_ptr] = fk_ptr
            else:
                data[db_field_name] = csv_value

        return data
