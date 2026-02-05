from sqlalchemy import or_, func, case
from sqlalchemy.orm import Query


def apply_trigram_search(
    query: Query,
    search: str,
    fields: list,
    order_fields: list | None = None
):
    """
    Generic pg_trgm search helper

    :param query: SQLAlchemy query object
    :param search: search keyword
    :param fields: list of model fields for filtering
    :param order_fields: list of fields for ranking
    """

    if not search:
        return query

    # WHERE clause - handle NULL fields
    filters = []
    for field in fields:
        # Use coalesce to convert NULL to empty string
        filters.append(
            func.coalesce(field, '').op("%")(search)
        )
    
    query = query.filter(or_(*filters))


   # ORDER BY similarity - handle NULL fields
    if order_fields:
        similarities = []
        for field in order_fields:
            # Coalesce NULL fields to empty string, then calculate similarity
            similarities.append(
                func.coalesce(
                    func.similarity(func.coalesce(field, ''), search), 
                    0
                )
            )
        query = query.order_by(func.greatest(*similarities).desc())

    return query
