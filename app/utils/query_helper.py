import json
from sqlalchemy.orm import Session
from sqlalchemy import or_, inspect, text
from typing import Type, List, Tuple, Dict, Any
from app.core.redis import redis_client

def get_paginated_results(
    db: Session,
    model: Type,
    search_fields: List[str],
    search: str = "",
    skip: int = 0,
    limit: int = 100,
    joins: List[Dict] = [],
    select: List[str] = [],
    cache_expire: int = 60  # Waktu cache kadaluwarsa dalam detik
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Helper function to get paginated results with total count, with Redis caching.

    :param db: SQLAlchemy session
    :param model: SQLAlchemy model class
    :param search_fields: List of fields to search
    :param search: Search query string
    :param skip: Number of records to skip
    :param limit: Number of records to return
    :param joins: List of dictionaries for joins, each dict should contain
                  'model', 'join', 'search', 'fk', 'select'.
    :param select: List of fields to select from the main model
    :param cache_expire: Time in seconds for cache to expire
    :return: Tuple of results (as list of dictionaries) and total count
    """

    # Create a unique cache key
    cache_key = f"{model.__name__}:{search}:{skip}:{limit}:{json.dumps(select)}:{json.dumps(joins)}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        # If cache exists, return cached data
        return json.loads(cached_data)

    # Validate and prepare select fields from the main model
    valid_fields = [column.name for column in inspect(model).c]
    valid_select_fields = [field for field in select if field in valid_fields]
    query = db.query(*[getattr(model, field) for field in valid_select_fields])

    # Handle joins
    for join in joins:
        join_model = join['model']
        join_field = join['join']
        fk_field = join['fk']
        join_select = join.get('select', [])
        join_search_fields = join.get('search', [])

        # Validate and prepare select fields from the joined model
        valid_join_fields = [column.name for column in inspect(join_model).c]
        valid_join_select_fields = [field for field in join_select if field in valid_join_fields]

        # Join with the related model
        query = query.join(join_model, getattr(model, fk_field) == getattr(join_model, join_field))

        # Add selected fields from the joined model to the query
        if valid_join_select_fields:
            query = query.add_columns(*[getattr(join_model, field) for field in valid_join_select_fields])

        # Apply search filter on the joined model
        if search and join_search_fields:
            join_filters = [getattr(join_model, field).ilike(f"%{search}%") for field in join_search_fields]
            query = query.filter(or_(*join_filters))

    # Apply search filter on the main model
    if search and search_fields:
        filters = [getattr(model, field).ilike(f"%{search}%") for field in search_fields]
        query = query.filter(or_(*filters))

    # Clone the query to count the total records
    count_query = query.statement.with_only_columns([text('count(*)')]).order_by(None)
    total = db.execute(count_query).scalar()

    # Get paginated results
    results = query.offset(skip).limit(limit).all()

    # Convert results to list of dictionaries for better usability
    result_dicts = [
        {column.name: value for column, value in zip(query.column_descriptions, result)}
        for result in results
    ]

    # Cache the results
    redis_client.setex(cache_key, cache_expire, json.dumps((result_dicts, total)))

    return result_dicts, total
