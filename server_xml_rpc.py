import sqlite3
import uuid
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

sql_create_table = """
            create table notes
            (
                uuid        text
                    constraint notes_pk
                        primary key,
                note        text,
                status_view int default 1
            );
"""

sql_update_status = """
UPDATE notes
SET status_view = 0
WHERE
    uuid='{}' 
"""

class Database:
    def __init__(self):
        self._conn = sqlite3.connect('mydatabase.db')
        self._cursor = self._conn.cursor()
        self._check_and_create_table()

    def _check_and_create_table(self):
        self._cursor.execute("SELECT count() FROM sqlite_master WHERE type='table' AND name='notes';")
        result = self._cursor.fetchone()
        if not result[0]:
            self._cursor.execute(sql_create_table)
            self._conn.commit()
            print('Create table notes')

    def add(self, data):
        uuid_notes = uuid.uuid4()
        note = [str(uuid_notes), data, 1]
        try:
            self._cursor.execute("INSERT INTO notes VALUES(?, ?, ?);", note)
            self._conn.commit()
        except Exception as e:
            print(e)
            return ''
        return note[0]

    def get(self, uuid):
        self._cursor.execute(f"SELECT * FROM notes WHERE uuid='{uuid}'")
        result = self._cursor.fetchone()
        if not result or not result[2]:
            return ''

        uuid_resp, text, status = result
        self._cursor.execute(sql_update_status.format(uuid_resp))
        self._conn.commit()
        return text


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/notes',)


server = SimpleXMLRPCServer(('localhost', 8001), requestHandler=RequestHandler)
server.register_introspection_functions()

server.register_instance(Database())
server.serve_forever()
