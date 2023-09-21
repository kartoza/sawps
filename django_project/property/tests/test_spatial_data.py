from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.db import connection
from property.spatial_data import (
    extract_spatial_data_from_property_and_layer,
    get_distinct_srids,
    columns_and_srid,
    ColumnInfo
)
from property.factories import PropertyFactory
from frontend.tests.model_factories import ContextLayerF


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
        cls.prop = PropertyFactory.create(
            geometry=GEOSGeometry("MULTIPOLYGON(((0 0, 0 1, 1 1, 1 0, 0 0)), ((2 2, 2 3, 3 3, 3 2, 2 2)))"))
        cls.context_layer = ContextLayerF.create(
            layer_names=['test_table']
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
