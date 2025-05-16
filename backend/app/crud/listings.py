async def get_listings(
    pool,
    limit: int,
    offset: int,
    room_type: str | None = None,
    price_max: float | None = None,
    host_id: int | None = None,
):
    # Requête de base
    sql = """
    SELECT id, price, latitude, longitude, neighbourhood, room_type, host_id
    FROM listings
    WHERE TRUE
    """
    params: list = []
    # Filtres dynamiques
    if room_type:
        sql += f" AND room_type = ${len(params) + 1}"
        params.append(room_type)

    if price_max is not None:
        sql += f" AND price <= ${len(params) + 1}"
        params.append(price_max)
    # Pagination
    sql += f" ORDER BY id LIMIT {limit} OFFSET {offset}"

    rows = await pool.fetch(sql, *params)
    return [dict(row) for row in rows]
