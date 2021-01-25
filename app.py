import os
from flask import Flask, render_template, request
import datetime
#from dotenv import load_dotenv
import pyodbc
import sqlparams

load_dotenv()
def create_app():
        app = Flask(__name__)
        app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

        #load_dotenv()

        connection = pyodbc.connect(
            "driver={ODBC Driver 17 for SQL Server};"
            "database=QuickAccess;"
            "server=DESKTOP-D4OLQNR\SQLEXPRESS;"
            "trusted_Connecton=yes;"
            "UID=prems;"
            "PWD=prem123;"
        )
        cursor = connection.cursor()
        db_entries = []
        query = sqlparams.SQLParams('named', 'qmark')

        @app.route('/', methods=["GET", "POST"])
        def home(lastname="", firstname=""):
            if request.method == 'POST':
                lastname = request.form.get('LastName')
                firstname = request.form.get('FirstName')
            sql, params = query.format("SELECT * FROM FIRST_QA_EMP where (:lname = '' OR (LAST_NAME != '' "
                                       "AND LAST_NAME = :lname)) "
                                       "AND (:fname = '' OR (FIRST_NAME != '' AND FIRST_NAME = :fname))",
                                       {"lname": lastname, "fname": firstname})
            db_entries = [
                (
                    entry[0],
                    entry[1],
                    entry[2]
                )
                for entry in cursor.execute(sql, params)
            ]
            sql, params = query.format("SELECT count(1) FROM FIRST_QA_EMP where (:lname = '' OR (LAST_NAME != '' "
                                       "AND LAST_NAME = :lname)) "
                                       "AND (:fname = '' OR (FIRST_NAME != '' AND FIRST_NAME = :fname))",
                                       {"lname": lastname, "fname": firstname})
            (count,) = cursor.execute(sql, params)
            return render_template("NewQuickAccess.html", entries=db_entries, lastname=lastname, firstname=firstname, counter=count)

        @app.route('/create', methods=["GET", "POST"])
        def create():
            if request.method == 'POST':
                lastname = request.form.get('LastName')
                firstname = request.form.get('FirstName')
                print(lastname + firstname)
                cursor.execute("Insert into FIRST_QA_EMP (LAST_NAME, FIRST_NAME) values (?, ?)",(lastname, firstname))
                cursor.commit()
                return "Record has been Saved."
            user_id = "After Save"
            return render_template("CreateNewUser.html", user=user_id, ClickMenuID="Create")

        @app.route('/delete/<int:user_id>', methods=["GET", "POST"])
        def delete(user_id):
            cursor.execute("Delete from FIRST_QA_EMP where SEQ_NO = ?", user_id)
            cursor.commit()
            return "Record has been Deleted."

        @app.route('/modify/<int:user_id>', methods=["GET", "POST"])
        def modify(user_id):
            print(request.method + "Modify")
            if request.method == 'POST':
                lastname = request.form.get('LastName')
                firstname = request.form.get('FirstName')
                print(lastname + firstname + str(user_id))
                cursor.execute("UPDATE FIRST_QA_EMP set LAST_NAME = ?, FIRST_NAME = ? where SEQ_NO = ?",
                               (lastname, firstname, user_id))
                cursor.commit()
                return "Record has been Modified."
            records = cursor.execute("Select LAST_NAME, FIRST_NAME FROM FIRST_QA_EMP where SEQ_NO = ?", user_id)
            for row in records:
                lastname = row[0]
                firstname = row[1]
            return render_template("CreateNewUser.html", user=user_id, LastName=lastname, FirstName=firstname, ClickMenuID="Modify")


        @app.route('/view/<int:user_id>', methods=["GET", "POST"])
        def view(user_id):
            records = cursor.execute("Select LAST_NAME, FIRST_NAME FROM FIRST_QA_EMP where SEQ_NO = ?", user_id)
            for row in records:
                lastname = row[0]
                firstname = row[1]
            return render_template("CreateNewUser.html", user=user_id, LastName=lastname, FirstName=firstname, ClickMenuID="View")

        return app
"""
if __name__ == '__main__':
    app.run(debug=True)"""