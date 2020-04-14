from server import *
import os

db.drop_all()
db.create_all()

test = Machine("testMachine1", 0, 0, 0, 900)
test1 = Machine("testMachine2", 0, 0, 0, 850)

db.session.add(test)
db.session.add(test1)

db.session.commit()

print("db reset, two test machines created.")

os.system("pause");