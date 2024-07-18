# OracleDBClient.py
import json
import cx_Oracle

class OracleDBClient:
    def __init__(self, dsn, user, password):
        self.connection = cx_Oracle.connect(user, password, dsn)

    def insert_document(self, data):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO ai_agent_states (agent_id, emotion, memory, emotion_history)
            VALUES (:1, :2, :3, :4)
        """, (data['agent_id'], data['emotion'], ','.join(data['memory']), json.dumps(data['emotion_history'])))
        self.connection.commit()
        cursor.close()

    def fetch_document(self, query):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT agent_id, emotion, memory, emotion_history
            FROM ai_agent_states
            WHERE agent_id = :1
        """, (query['agent_id'],))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return {
                'agent_id': row[0],
                'emotion': row[1],
                'memory': row[2].split(','),
                'emotion_history': json.loads(row[3])
            }
        return None

    def insert_generated_response(self, data):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO ai_generated_responses (timestamp, input_text, generated_response, emotion)
            VALUES (:1, :2, :3, :4)
        """, (data['timestamp'], data['input_text'], data['generated_response'], data['emotion']))
        self.connection.commit()
        cursor.close()
