import configparser
import os

class DBPropertyUtil:
    @staticmethod
    def get_property_value(file_name):
        print(f" Trying to load: {file_name}")
        if not os.path.exists(file_name):
            print(" File not found at given path.")
        else:
            with open(file_name, 'r') as f:
                print(" Contents of db.properties:")
                print(f.read())

        config = configparser.ConfigParser()
        config.read(file_name)

        return {
            'host': config.get('mysql', 'host'),
            'user': config.get('mysql', 'user'),
            'password': config.get('mysql', 'password'),
            'database': config.get('mysql', 'database')
        }
