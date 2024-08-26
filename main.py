import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


#clase para gestionar la conexion y las consultas a la base de datos.

class BaseDatos:
   def __init__(self, host,user,password, database=None):
       #se inicializa los parametros de conexion.
       # Encapsulamiento: Los detalles de conexión están encapsulados dentro de esta clase.
       self.host= host
       self.user=user
       self.password=password
       self.database=database
       self.connection=None
       self.cursor=None

   def connect(self):
       #establece la conexion a la base de datos
       # Abstracción: La conexión a la base de datos está abstraída en un método.
       self.connection= mysql.connector.connect(
           host=self.host,
           user=self.user,
           password=self.password,
           database=self.database
       )
       #crea un cursor para ejecutar consultas.
       self.cursor= self.connection.cursor()

   #conecta al servidor y crea la base de datos si no existe.
   def create_database(self,db_name):
       # Conéctate sin especificar una base de datos para crearla
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')
        self.connection.commit()
        
        # Luego vuelve a conectar a la base de datos recién creada
        self.database = db_name
        self.connect()

   def ejecutar_consulta(self,query,params=None):
       #ejecuta una consulta  con o sin los parametros.
       self.cursor.execute(query,params)
       #guarda los cambios en la base de datos.
       self.connection.commit()
   
   def close(self):
       #cierra el cursor y la conexion a la base de datos.
       self.cursor.close()
       self.connection.close()

#
#clase para manejar las operaciones relacionadas con la tabla.

class EmployeePerformance:
    def __init__(self,db):
        #recibe una isntancia de la database para operar en la base de datos.
        self.db=db
        self.nombre_tabla= "EmployeePerformance"

    def crear_tabla(self):
        #crea la tabla si no existe.
        create_tabla_query=f"""
        CREATE TABLE IF NOT EXISTS {self.nombre_tabla} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id INT,
                department VARCHAR(255),
                performance_score FLOAT,
                years_with_company INT,
                salary FLOAT
            )

      """
        #ejecuta la consulata de l creacion de la tabla.
        self.db.ejecutar_consulta(create_tabla_query)

    def insertar_datos(self,data_frame):
        #inserta los datos del archivo que estan en data_frame a la tabla.
        insert_query= f"""
          INSERT INTO {self.nombre_tabla} (employee_id, department, performance_score, years_with_company, salary)
            VALUES (%s, %s, %s, %s, %s)
       
       """
        #itera sobre cada fila del dataFrame para insertar en la tabla.
        for _, row in data_frame.iterrows():
            self.db.ejecutar_consulta(insert_query,(
                 row['employee_id'],
                row['department'],
                row['performance_score'],
                row['years_with_company'],
                row['salary']
            ))

    def analizar_datos(self):
        # Consulta todos los datos de la tabla EmployeePerformance
        query = f"SELECT * FROM {self.nombre_tabla}"
        df = pd.read_sql(query, self.db.connection)

        # Análisis de datos por departamento
        departamentos = df['department'].unique()

        for dept in departamentos:
            print(f"\nEstadísticas para el departamento: {dept}")
            dept_data = df[df['department'] == dept]

            # Media, mediana y desviación estándar del performance_score
            print("Performance Score:")
            print(f"Media: {dept_data['performance_score'].mean()}")
            print(f"Mediana: {dept_data['performance_score'].median()}")
            print(f"Desviación Estándar: {dept_data['performance_score'].std()}")

            # Media, mediana y desviación estándar del salary
            print("\nSalary:")
            print(f"Media: {dept_data['salary'].mean()}")
            print(f"Mediana: {dept_data['salary'].median()}")
            print(f"Desviación Estándar: {dept_data['salary'].std()}")

            # Número total de empleados por departamento
            print(f"\nNúmero total de empleados: {dept_data['employee_id'].count()}")

            # Correlación entre years_with_company y performance_score
            print(f"\nCorrelación entre Years with Company y Performance Score: {dept_data['years_with_company'].corr(dept_data['performance_score'])}")

            # Correlación entre salary y performance_score
            print(f"Correlación entre Salary y Performance Score: {dept_data['salary'].corr(dept_data['performance_score'])}")

            # Visualización de los datos
            plt.figure()
            plt.hist(dept_data['performance_score'], bins=10, alpha=0.7, color='blue')
            plt.title(f'Histograma del Performance Score - {dept}')
            plt.xlabel('Performance Score')
            plt.ylabel('Frecuencia')
            plt.show()

            plt.figure()
            plt.scatter(dept_data['years_with_company'], dept_data['performance_score'], alpha=0.7)
            plt.title(f'Years with Company vs Performance Score - {dept}')
            plt.xlabel('Years with Company')
            plt.ylabel('Performance Score')
            plt.show()

            plt.figure()
            plt.scatter(dept_data['salary'], dept_data['performance_score'], alpha=0.7)
            plt.title(f'Salary vs Performance Score - {dept}')
            plt.xlabel('Salary')
            plt.ylabel('Performance Score')
            plt.show()

 # Ejecuta la secuencia principal:
#  conectar a la base de datos, crear la tabla, leer e insertar datos, y cerrar la conexión.
if __name__== "__main__":
      # Inicializar la base de datos y conectarse
    db = BaseDatos(host='localhost', user='root', password='')
    db.create_database('DataCompany')
    db.connect()

    # Crear la tabla EmployeePerformance
    employee_performance = EmployeePerformance(db)
    employee_performance.crear_tabla()

    # Leer los datos desde el archivo CSV
    df = pd.read_csv('DatosTabla.csv')

    # Insertar los datos en la tabla
    employee_performance.insertar_datos(df)
    # Realizar análisis de datos por departamento
    employee_performance.analizar_datos()

    # Cerrar la conexión a la base de datos
    db.close()

