import mysql.connector

import pandas as pd

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

#Leer los datos ficticios de el archivo CSV

df= pd.read_csv('DatosTabla.csv')

#Conectar a mysql
conne= mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='CompanyData'
)
cursor= conne.cursor()

#insertar los datos en la tabla 

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO EmployeePerformance (employee_id, department, performance_score, years_with_company, salary)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['employee_id'], row['department'], row['performance_score'], row['years_with_company'], row['salary']))

conne.commit()
conne.close()