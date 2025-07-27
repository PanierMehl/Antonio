import uuid
from datetime import datetime, timedelta  
import os
import mysql.connector
from dotenv import load_dotenv
    
    ##################################################################################################################
                                        # D A S H B O A R D    S E S S I O N # 
    ##################################################################################################################

load_dotenv()

class DasboardDB:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("MEMBERNAME"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"))


        self.cursor = self.db.cursor()

    async def add_session(self, token, refresh_token, expires_in, user_id):
        session_id = str(uuid.uuid4())
        expires = datetime.now() + timedelta(seconds=expires_in)

        self.cursor.execute('''
            INSERT INTO dashboard_sessions (session_id, token, refresh_token, token_expires_at, user_id)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            token = VALUES(token), refresh_token = VALUES(refresh_token), token_expires_at = VALUES(token_expires_at), user_id = VALUES(user_id)''',
            (session_id, token, refresh_token, expires, user_id))

        self.db.commit()
        return session_id
    

    async def get_session(self, session_id):
        self.cursor.execute('''SELECT token, refresh_token, token_expires_at FROM dashboard_sessions WHERE session_id = %s''', (session_id,))
        output = self.cursor.fetchone()

        if output is not None:
            return output
        else:
            output = None

        return output
    

    async def update_session(self, session_id, token, refresh_token, token_expires_at):
        self.cursor.execute("UPDATE dashboard_sessions SET token = %s, refresh_token = %s, token_expires_at = %s WHERE session_id = %s",
                (token, refresh_token, token_expires_at, session_id,))
        self.db.commit()

    async def delete_session(self, session_id):
        self.cursor.execute("DELETE FROM dashboard_sessions WHERE session_id = %s", (session_id,))
        self.db.commit()

