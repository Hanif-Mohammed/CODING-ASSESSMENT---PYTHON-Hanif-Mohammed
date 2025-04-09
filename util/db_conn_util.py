import pymysql
import os
from util.db_property_util import DBPropertyUtil

class DBConnUtil:
    @staticmethod
    def get_connection(prop_file_name):
        try:
            # Get absolute path to the project root
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            prop_path = os.path.join(base_dir, prop_file_name)

            props = DBPropertyUtil.get_property_value(prop_path)
            connection = pymysql.connect(
                host=props['host'],
                user=props['user'],
                password=props['password'],
                database=props['database']
            )
            return connection
        except Exception as e:
            print("Error while connecting to DB:", e)
            return None
