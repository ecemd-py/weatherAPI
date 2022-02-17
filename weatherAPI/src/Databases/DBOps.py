from sqlalchemy import create_engine
import pandas as pd

class DBOps:
    def __init__(self):
        conn_str = "postgresql://postgres:postgres@localhost:5432/postgres"
        self.engine = create_engine(conn_str)

    def check_user_exist(self, username):
        query = f"""
                SELECT *
                FROM user_info
                WHERE username = '{username}'
        """
        sql_response = self.__run_select_query__(query)

        if len(sql_response.values) > 0:
            return True
        else:
            return False

    def get_userinfo_by_userid(self, userid):
        query = f"""
                SELECT username, password, role
                FROM user_info
                WHERE user_id = '{userid}'
        """
        sql_response = self.__run_select_query__(query)

        if len(sql_response) > 0:
            return sql_response.to_dict('records')[0]
        return sql_response.to_dict('records')
    
    def check_correct_password(self, username, password):
        query = f"""
                SELECT password
                FROM user_info
                WHERE username = '{username}'
        """
        sql_response = self.__run_select_query__(query)

        if sql_response['password'][0] == password:
            return True
        else:
            return False
    
    def is_Admin(self, username):
        query = f"""
                SELECT LOWER(role) as role
                FROM user_info
                WHERE username = '{username}'
        """
        sql_response = self.__run_select_query__(query)

        if len(sql_response) > 0 and sql_response['role'][0] == 'admin':
            return True
        else:
            return False

    def update_userinfo_by_userid(self, userid, info):
        query = f"""
                UPDATE user_info
                SET {list(info.keys())[0]} = '{list(info.values())[0]}'
                WHERE user_id = '{userid}'
        """
        try:
            sql_response = self.__run_raw_query__(query)
            if sql_response.rowcount:
                return True
            else:
                return False
        except:
            return False  

    def insert_new_user(self, info):
        query = f"""
                INSERT INTO user_info(user_id, username, password, role)
                VALUES ('{info['user_id']}', '{info['username']}', '{info['password']}', '{info['role']}')
        """
        try:
            sql_response = self.__run_raw_query__(query)
            if sql_response.rowcount:
                return True
            else:
                return False
        except:
            return False        

    def delete_user(self, userid):
        query = f"""
                DELETE FROM user_info
                WHERE user_id = '{userid}'
        """
        try:
            sql_response = self.__run_raw_query__(query)
            if sql_response.rowcount:
                return True
            else:
                return False
        except:
            return False  


    def get_weather_info(self, filter):
        query = f"""
                SELECT time, location, condition, temperature
                FROM weather_info
        """
        
        sql_response = self.__run_select_query__(query)
        where = {key: filter[key] for key in ["time", "location", "condition", "temperature"] if not filter[key] is None}
        agg = {key: filter[key] for key in ["agg", "agg_column"] if not filter[key] is None}
        date_range = {key: filter[key] for key in ["start_date", "end_date"] if not filter[key] is None}

        if len(where) > 0 and len(sql_response) > 0:
            sql_response = sql_response.loc[(sql_response[list(where)] == pd.Series(where)).all(axis=1)]

        if len(date_range) > 0 and len(sql_response) > 0:
            sql_response = sql_response[(sql_response['time'] > date_range["start_date"]) & (sql_response['time'] < date_range["end_date"])]
        
        if len(agg) > 0 and len(sql_response) > 0:
            sql_response = sql_response.agg({agg["agg_column"]: agg["agg"].lower()})
            return sql_response.to_dict()

        return sql_response.to_dict(orient='index')

    def __run_select_query__(self, query):
        with self.engine.connect() as conn:
            sql_response = pd.read_sql_query(query, conn)
        return sql_response
    
    def __run_raw_query__(self, query):
        with self.engine.connect() as conn:
            sql_response = conn.execute(query)
        return sql_response