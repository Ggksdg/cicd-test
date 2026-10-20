from aiomysql import DictCursor
from asyncio import shield

class MoviesService():
    def __init__(self, connection_pool) -> None:
        super().__init__()
        self.connection_pool = connection_pool

    async def create_movie(self, payload):
        async with self.connection_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await shield(cursor.execute(R'''
                    INSERT INTO movies (name, description, image_url)
                    VALUES (%(name)s, %(description)s, %(image_url)s)
                    ''', payload))
                await shield(connection.commit())
                return cursor.lastrowid

    async def get_movie_by_id(self, id):
        async with self.connection_pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await shield(cursor.execute(R'''
                    SELECT name, description, image_url FROM movies WHERE id = %s
                ''', id))
                await shield(connection.commit())
                return await cursor.fetchone()

    async def get_movies(self, limit, is_with_seances):
        async with self.connection_pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await shield(cursor.execute(R'''
                    SELECT * FROM movies LIMIT %s
                ''', limit))
                await shield(connection.commit())
                return await cursor.fetchall()