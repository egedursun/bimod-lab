#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-12 13:19:51
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:19:51
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from neo4j.spatial import Point

from datetime import (
    date,
    time,
    datetime,
    timedelta
)


class Neo4JDataTypesNames:
    NULL = "Null"
    BOOLEAN = "Boolean"
    INTEGER = "Integer"
    FLOAT = "Float"
    STRING = "String"
    LIST = "List"
    MAP = "Map"
    POINT = "Point"
    DATE = "Date"
    TIME = "Time"
    DATE_TIME = "DateTime"
    DURATION = "Duration"
    MIXED = "Mixed"
    UNKNOWN = "Unknown"

    @staticmethod
    def as_list():
        return [
            Neo4JDataTypesNames.NULL,
            Neo4JDataTypesNames.BOOLEAN,
            Neo4JDataTypesNames.INTEGER,
            Neo4JDataTypesNames.FLOAT,
            Neo4JDataTypesNames.STRING,
            Neo4JDataTypesNames.LIST,
            Neo4JDataTypesNames.MAP,
            Neo4JDataTypesNames.POINT,
            Neo4JDataTypesNames.DATE,
            Neo4JDataTypesNames.TIME,
            Neo4JDataTypesNames.DATE_TIME,
            Neo4JDataTypesNames.DURATION,
            Neo4JDataTypesNames.UNKNOWN
        ]


def neo4j_infer_data_type(value):
    if value is None:
        return Neo4JDataTypesNames.NULL

    if isinstance(value, bool):
        return Neo4JDataTypesNames.BOOLEAN

    if isinstance(value, int):
        return Neo4JDataTypesNames.INTEGER

    if isinstance(value, float):
        return Neo4JDataTypesNames.FLOAT

    if isinstance(value, str):
        return Neo4JDataTypesNames.STRING

    if isinstance(value, list):
        if not value:
            return f"{Neo4JDataTypesNames.LIST}<Unknown>"

        element_types = {
            neo4j_infer_data_type(element) for element in value
        }

        if len(
            element_types
        ) == 1:
            return f"{Neo4JDataTypesNames.LIST}<{list(element_types)[0]}>"

        return f"List<{Neo4JDataTypesNames.MIXED}: {', '.join(sorted(element_types))}>"

    if isinstance(value, dict):
        return f"{Neo4JDataTypesNames.MAP}<" + ", ".join(f"{k}: {neo4j_infer_data_type(v)}" for k, v in value.items()) + ">"

    if isinstance(value, Point):
        return Neo4JDataTypesNames.POINT

    if isinstance(value, date):
        return Neo4JDataTypesNames.DATE

    if isinstance(value, time):
        return Neo4JDataTypesNames.TIME

    if isinstance(value, datetime):
        return Neo4JDataTypesNames.DATE_TIME

    if isinstance(value, timedelta):
        return Neo4JDataTypesNames.DURATION

    return Neo4JDataTypesNames.UNKNOWN
