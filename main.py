import mysql.connector

#conexion a la base de datos

conne= mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)

cursor = conne.cursor()

#crear base de datos
cursor.execute('CREATE DATABASE IF NOT EXISTS CompanyData')
cursor.execute('USE CompanyData')

#crear tabla con el nombre EmployeePerformance 

cursor.execute("""
 CREATE TABLE IF NOT EXISTS EmployeePerformance (
     id INT AUTO_INCREMENT PRIMARY KEY,
        employee_id INT,
        department VARCHAR(255),
        performance_score FLOAT,
        years_with_company INT,
        salary FLOAT
               
    )

""")
conne.commit()