import server
import os
server.db.drop_all()
server.db.create_all()
print("db cleared")
os.system("pause")