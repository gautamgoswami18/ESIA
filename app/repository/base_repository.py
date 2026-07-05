from sqlalchemy import text
from sqlalchemy.orm import Session
from app.schemas.pagination import Pagination


class BaseRepository:

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------
    # SELECT
    # ---------------------------------------------------

    def fetch_all(self, sql, params=None):

        result = self.db.execute(text(sql), params or {})

        return [
            dict(row)
            for row in result.mappings().all()
        ]

    def fetch_one(self, sql, params=None):

        result = self.db.execute(text(sql), params or {})

        row = result.mappings().first()

        return dict(row) if row else None

    def fetch_scalar(self, sql, params=None):
        return self.db.execute(text(sql), params or {}).scalar()


    def fetch_paginated(self, sql, count_sql, params=None):

        data = self.fetch_all(sql, params)

        total = self.fetch_scalar(count_sql, params)

        return data, total    
    
    # ---------------------------------------------------
    # INSERT / UPDATE / DELETE
    # ---------------------------------------------------

    def execute(self, sql, params=None):

        self.db.execute(sql, params or {})

        self.db.commit()

    # ---------------------------------------------------
    # COUNT
    # ---------------------------------------------------

    def fetch_count(self, sql, params=None):

        result = self.db.execute(sql, params or {})

        return result.scalar()

    # ---------------------------------------------------
    # PAGINATION
    # ---------------------------------------------------

    def paginate(
        self,
        data_sql: str,
        count_sql: str,
        page: int = 1,
        size: int = 10,
        params=None
    ):

        offset = (page - 1) * size

        parameters = params.copy() if params else {}

        # -----------------------------
        # Get Total Records
        # -----------------------------

        total_records = self.db.execute(
            text(count_sql),
            parameters
        ).scalar()

        # -----------------------------
        # Get Paginated Data
        # -----------------------------

        paginated_sql = f"""
        {data_sql}
        LIMIT :limit
        OFFSET :offset
        """

        parameters.update({
            "limit": size,
            "offset": offset
        })

        result = self.db.execute(
            text(paginated_sql),
            parameters
        )

        records = [
            dict(row)
            for row in result.mappings().all()
        ]

        return {
            "items": records,
            "pagination": Pagination.create(
                page=page,
                size=size,
                total_records=total_records
            )
        }

    # ---------------------------------------------------
    # SEARCH
    # ---------------------------------------------------

    def search(
        self,
        base_sql: str,
        search_column: str,
        keyword: str,
        page: int = 1,
        size: int = 10
    ):

        sql = f"""
        {base_sql}

        WHERE

            {search_column}
            ILIKE :keyword

        """

        return self.paginate(

            sql,

            page,

            size,

            {
                "keyword": f"%{keyword}%"
            }

        )

    # ---------------------------------------------------
    # FILTER
    # ---------------------------------------------------

    def filter(
        self,
        base_sql: str,
        filters: dict,
        page: int = 1,
        size: int = 10
    ):

        conditions = []

        params = {}

        for key, value in filters.items():

            if value is None:
                continue

            conditions.append(
                f"{key} = :{key}"
            )

            params[key] = value

        sql = base_sql

        if conditions:

            sql += "\n WHERE "

            sql += " AND ".join(
                conditions
            )

        return self.paginate(

            sql,

            page,

            size,

            params

        )

    # ---------------------------------------------------
    # SORT
    # ---------------------------------------------------

    def sort(
        self,
        base_sql: str,
        sort_by: str,
        order: str = "ASC",
        page: int = 1,
        size: int = 10
    ):

        sql = f"""

        {base_sql}

        ORDER BY

            {sort_by}

            {order}

        """

        return self.paginate(
            sql,
            page,
            size
        )