from unittest.mock import MagicMock

import pytest

from openapi_parser.builders import HeaderBuilder, SchemaFactory
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Header, Integer, Schema, String


def _get_schema_factory_mock(expected_value: Schema) -> SchemaFactory:
    mock_object = MagicMock()
    mock_object.create.return_value = expected_value

    return mock_object


string_schema = String(type=DataType.STRING)
integer_schema = Integer(type=DataType.INTEGER)

schema_data_provider = (
    (
        {
            "schema": {
                "type": "string"
            }
        },
        Header(schema=string_schema),
        _get_schema_factory_mock(string_schema)
    ),
    (
        {
            "description": "The number of allowed requests in the current period",
            "required": True,
            "deprecated": True,
            "schema": {
                "type": "integer",
            },
        },
        Header(
            required=True,
            description="The number of allowed requests in the current period",
            deprecated=True,
            schema=integer_schema
        ),
        _get_schema_factory_mock(integer_schema)
    ),
)

collection_data_provider = (
    (
        {
            "X-Header": {
                "schema": {
                    "type": "string"
                }
            }
        },
        {
            "X-Header": Header(schema=string_schema),
        },
        _get_schema_factory_mock(string_schema)
    ),
    (
        {
            "X-Header": {
                "description": "The number of allowed requests in the current period",
                "required": True,
                "deprecated": True,
                "schema": {
                    "type": "integer",
                },
            }
        },
        {
            "X-Header": Header(
                required=True,
                description="The number of allowed requests in the current period",
                deprecated=True,
                schema=integer_schema
            )
        },
        _get_schema_factory_mock(integer_schema)
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'schema_factory'], schema_data_provider)
def test_build(data: dict, expected: Header, schema_factory: SchemaFactory):
    builder = HeaderBuilder(schema_factory)

    assert expected == builder.build(data)


@pytest.mark.parametrize(['data', 'expected', 'schema_factory'], collection_data_provider)
def test_build_collection(data: dict, expected: Header, schema_factory: SchemaFactory):
    builder = HeaderBuilder(schema_factory)

    assert expected == builder.build_collection(data)