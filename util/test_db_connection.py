
from util.db_conn_util import DBConnUtil
import os
print(" CWD:", os.getcwd())

conn = DBConnUtil.get_connection('./db.properties')
if conn:
    print(" Connection successful!")
else:
    print(" Connection failed.")
