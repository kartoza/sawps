from unittest.mock import patch, PropertyMock

from django.contrib.admin import AdminSite
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase, RequestFactory
from django.db import connection
from django.db.utils import InternalError
from django.core.exceptions import ObjectDoesNotExist

from frontend.models.spatial import SpatialDataModel
from property.admin import PropertyAdmin
from property.models import Property
from property.spatial_data import (
    extract_spatial_data_from_property_and_layer,
    save_spatial_values_from_property_layers,
    get_distinct_srids,
    columns_and_srid,
    ColumnInfo,
    SpatialDataValueModel
)
from property.factories import PropertyFactory
from frontend.tests.model_factories import (
    LayerF,
    ContextLayerF,
    SpatialDataModelF
)
from property.tasks import generate_spatial_filter_task


class TestSpatialFunctions(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a sample table with varying SRID (This is just a basic example)
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS layer;
                 CREATE TABLE layer.test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    geom GEOMETRY(Point, 4326)
                );
                INSERT INTO layer.test_table (name, geom) 
                    VALUES ('Point A', ST_GeomFromText('POINT(0 0)', 4326));
                INSERT INTO layer.test_table (name, geom) 
                    VALUES ('Point B', ST_GeomFromText('POINT(0 1)', 4326));
            """)
            cursor.execute("""
                 CREATE TABLE layer.test_table_2 (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    geom GEOMETRY(Point, 0)
                );
            """)
        cls.prop = PropertyFactory.create(
            geometry=GEOSGeometry("MULTIPOLYGON(((0 0, 0 1, 1 1, 1 0, 0 0)), ((2 2, 2 3, 3 3, 3 2, 2 2)))"))
        cls.context_layer = ContextLayerF.create(
            layer_names=['test_table']
        )
        cls.layer = LayerF.create(
            context_layer=cls.context_layer,
            name='test_table',
            spatial_filter_field='name'
        )

    @classmethod
    def tearDownClass(cls):
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE layer.test_table;")
        super().tearDownClass()

    def test_get_distinct_srids(self):
        srids = get_distinct_srids("test_table")
        expected_srids = [4326]

        self.assertCountEqual(srids, expected_srids)

        srids = get_distinct_srids("test_table_2")
        self.assertEqual(srids, [])

    def test_columns_and_srid(self):
        columns, srid = columns_and_srid("test_table")

        expected_columns = [
            ColumnInfo("id", "integer", "-"),
            ColumnInfo("name", "character varying", "-"),
            ColumnInfo("geom", "geometry", "4326")
        ]

        self.assertEqual(srid, "4326")
        self.assertEqual(len(columns), len(expected_columns))
        self.assertEqual(columns[0].column_name, 'id')
        self.assertEqual(columns[0].data_type, 'integer')
        self.assertEqual(columns[0].srid, '-')

    def test_extract_spatial_data(self):
        data = extract_spatial_data_from_property_and_layer(
            self.prop, self.context_layer)
        expected_data = {
            "test_table": [
                {
                    "id": 1,
                    "name": "Point A"
                },
                {
                    "id": 2,
                    "name": "Point B"
                }
            ]
        }

        self.assertEqual(data, expected_data)

    def test_extract_spatial_data_with_internal_error(self):
        with patch('django.db.models.sql.compiler.SQLCompiler') as mock_connection:
            mock_connection.cursor.side_effect = InternalError('Connection timed out')
            data = extract_spatial_data_from_property_and_layer(
                self.prop, self.context_layer)
            self.assertEqual(data, {})

    def test_extract_spatial_data_no_geometry(self):
        prop = PropertyFactory.create(
            geometry=None
        )
        data = extract_spatial_data_from_property_and_layer(
            prop, self.context_layer)
        self.assertEqual(data, {})

    def test_extract_spatial_data_no_srid(self):
        context_layer = ContextLayerF.create(
            layer_names=['test_table_2']
        )
        LayerF.create(
            name='test_table_2',
            context_layer=context_layer
        )
        data = extract_spatial_data_from_property_and_layer(
            self.prop, context_layer)
        self.assertEqual(data, {})

    def test_save_spatial_value(self):
        save_spatial_values_from_property_layers(
            self.prop
        )
        self.assertTrue(
            SpatialDataValueModel.objects.filter(
                layer=self.layer,
                context_layer_value='Point A'
            ).exists()
        )

    def test_save_spatial_value_no_context_layers(self):
        prop = PropertyFactory.create()
        save_spatial_values_from_property_layers(
            prop
        )
        self.assertFalse(SpatialDataModel.objects.filter(
            property=prop
        ).exists())

    def test_save_spatial_value_with_no_spatial_data(self):
        with patch('property.spatial_data.extract_spatial_data_from_property_and_layer', return_value={}):
            save_spatial_values_from_property_layers(self.prop)
        self.assertFalse(SpatialDataModel.objects.filter(
            property=self.prop
        ).exists())

    def test_save_spatial_value_layers_not_found(self):
        with patch('property.spatial_data.extract_spatial_data_from_property_and_layer', return_value={
            'test_layer': [{'id': '1'}]
        }):
            save_spatial_values_from_property_layers(self.prop)
        self.assertFalse(SpatialDataValueModel.objects.filter(
            layer=self.layer,
            context_layer_value='1'
        ).exists())

    def test_save_spatial_value_spatial_filter_not_found(self):
        with patch('property.spatial_data.extract_spatial_data_from_property_and_layer', return_value={
            'test_table': [{'id': '1'}]
        }):
            save_spatial_values_from_property_layers(self.prop)
        self.assertFalse(SpatialDataValueModel.objects.filter(
            layer=self.layer,
            context_layer_value='1'
        ).exists())

    def test_string_spatial_model(self):
        spatial_model = SpatialDataModelF.create()
        self.assertEqual(
            str(spatial_model),
            spatial_model.property.name
        )
        # mock property field to raise ObjectDoesNotExist
        with patch.object(SpatialDataModel, 'property', new_callable=PropertyMock) as mocked_obj:
            mocked_obj.side_effect = ObjectDoesNotExist('error')
            self.assertEqual(str(spatial_model),
                             "SpatialDataModel-{}".format(spatial_model.id))


class GenerateSpatialFilterTaskTest(TestCase):

    @patch('property.spatial_data.save_spatial_values_from_property_layers')
    @patch('property.tasks.generate_spatial_filter_task.delay')
    def test_generate_spatial_filter_task(self, mock_shared_task, mock_save_spatial):
        property_obj = PropertyFactory.create()
        generate_spatial_filter_task(property_obj.id)
        mock_save_spatial.assert_called_once_with(property_obj)


class GenerateSpatialFiltersTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()

    @patch('property.tasks.generate_spatial_filter.generate_spatial_filter_task')
    def test_generate_spatial_filters_for_properties(self, mock_task):
        property_1 = PropertyFactory.create()
        property_2 = PropertyFactory.create()

        property_1.spatialdatamodel_set.create()
        property_2.spatialdatamodel_set.create()

        self.assertEqual(property_1.spatialdatamodel_set.count(), 1)
        self.assertEqual(property_2.spatialdatamodel_set.count(), 1)

        ma = PropertyAdmin(Property, self.site)
        request = self.factory.get("/admin")
        queryset = Property.objects.filter(
            id__in=[property_1.id, property_2.id]
        )

        ma.generate_spatial_filters_for_properties(request, queryset)

        self.assertEqual(property_1.spatialdatamodel_set.count(), 0)
        self.assertEqual(property_2.spatialdatamodel_set.count(), 0)

        self.assertGreaterEqual(mock_task.delay.call_count, 2)
