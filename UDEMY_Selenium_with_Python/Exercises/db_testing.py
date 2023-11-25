import mysql.connector

select_query = "SELECT * FROM employees"
insert_query = "INSERT INTO employees VALUES('Milena', 'Stankina', 1000)"
update_query = "UPDATE employees SET first_name='Nasko' WHERE first_name='Atanas'"
delete_query = "DELETE FROM employees WHERE first_name='Milena'"

try:
    connection = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="hotel")
    cursor = connection.cursor()
    cursor.execute(select_query)
    # connection.commit()
    for row in cursor:
        print(row[0], row[1], row[2])

    connection.close()
except:
    print("Connection unsuccessful...")
