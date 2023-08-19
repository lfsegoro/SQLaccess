import mysql.connector

#  START mysql connector
#  ======================================================================
db = mysql.connector.connect(
    host="192.168.22.198",
    user="public",
    passwd="",
    database="radius_public"
)

mycursor = db.cursor()
#  ======================================================================
#  END mysql connector