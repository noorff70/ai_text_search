import sqlite3

class ConversationRepository:

    def __init__(self, db_path: str):
        self._db_path = db_path

    def create_conversation(self) -> int:
        
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        cursor.execute ("""INSERT INTO conversation DEFAULT VALUES""")

        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return conversation_id

    def add_message(self, conversation_id: int, role: str, content:str):

        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute("""
                INSERT INTO message
                ( conversation_id, role, content )
                VALUES (?, ?, ?)
            """, ( conversation_id, role, content ))

        conn.commit()
        conn.close()

    def get_messages( self, conversation_id: int ) -> list[dict]:

            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    role,
                    content
                FROM message
                WHERE conversation_id = ?
                ORDER BY id
            """, (conversation_id,))

            rows = cursor.fetchall()

            conn.close()

            return [
                {
                    "role": row[0],
                    "content": row[1]
                }
                for row in rows
            ]

    def get_all_msgs(self)-> list[dict]:
         conn = sqlite3.connect(self._db_path)
         cursor = conn.cursor()

         cursor.execute(""" SELECT * FROM message""")
         rows = cursor.fetchall()

         return [{
              "conversation_id": row[1],
              }
              for row in rows   
         ]

    # def delete_conversation(self, conversation_id: int):
    #      conn = sqlite3.connect(self._db_path)
    #      cursor = conn.cursor()

    #      cursor.execute(DELETE from )

