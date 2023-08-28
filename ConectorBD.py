import MySQLdb 

DB_HOST = 'localhost' 
DB_USER = 'root' 
DB_PASS = 'lucas1234+' 
DB_NAME = 'gestor_universitario' 

def run_query(query=''): 
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
    conn = MySQLdb.connect(*datos)  # Conectar a la base de datos 
    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 

    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select 
    
    elif query.upper().startswith('INSERT'): 
        conn.commit()
        data = cursor.lastrowid #Devuelve el id del dato ingresado
    else: 
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
 
    
    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 

    return data

#Esta funcion permite que le manden muchas querys y que si se hacen todas se comitean
#pero si hay un error hace un rollback
#util cunado hacemos muchas querys relacionadas, por ejemplo, cuando pasas plata a una cuenta
#del banco, si la segunda query de agregar la plata a la nueva cuneta falla, automaticamente
# hay que desacer la primera query de sacar la plata de la primera cuenta
def run_query_version_con_rollback(query):  # recibo una lista de querys, si quisiera que me pasen
                                            # muchas querys y que la funcion misma las empaquetara
                                            # en una lista, debo poner *query
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
    conn : MySQLdb.Connection = MySQLdb.connect(*datos)  # hago conn : MySQLdb.Connection para que se sepa que conn es un objeto tipo Connection, y asi me aparezcan sus metodos, como commit y rollback
    cursor = conn.cursor()         # Crear un cursor 
    data = ""
    
    #Este try atrapara solo fallos de las query para hacer un rollback, si se falla en la conexion
    #No se atrapara
    try:
        for q in query: #recorro la lista de querys
            cursor.execute(q)          # Ejecutar una consulta 

            if q.upper().startswith('SELECT'): 
                data = cursor.fetchall()   # Traer los resultados de un select 
            
            elif q.upper().startswith('INSERT'): 

                data = cursor.lastrowid #Devuelve el id del dato ingresado
            else: 
                            # Hacer efectiva la escritura de datos 
                data = None 
        
        conn.commit() #esto se ejecuta si todos las querys salen bien
    except Exception as e:
        print(type(e).__name__)
        print(e)
        #DATAZO, en mysqldb nunca se graban las ejecucion si explicitamente no hay un commit
        #Osea podria no tener el rollback y aun asi si la segunda query falla la primera no se
        #Guardara ya que no habria pasado por el commit dentro del try
        conn.rollback() #Esto se ejecuta si algun query fallo, para asi volver atras a todos las querys
        data = "Fallo" # asi me retorna si algo fallo
    
 
    
    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 

    return data


#Si paso  una lista 
# q = []
# q.append("insert into materias values(25,'c','c','c','c',1,1)")
# q.append("insert into materias values(26,'c','c','c")
# print(run_query_version_con_rollback(q))

# #Si paso muchas querys (tendria que en la funcion poner como parametro *query y no query, para 
# directo la funcion me los empaquete y me los convierta a una lista)
# q1 = "insert into materias values(25,'c','c','c','c',1,1)"
# q2 = "insert into materias values(26,'c','c','c','c',1,32)"
# print(run_query_version_con_rollback(q1,q2))


# #Como mostrar un select de mejor manera con pandas
# import pandas as pd

# print(pd.DataFrame(data=run_query("select * from materias"), columns=["ID", "Nombre","Dia","Desde","Hasta","ID docente","ID Carrera"]))


# #Asi me lee de forma mas linda una query
# import pandas as pd

# datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
# conn = MySQLdb.connect(*datos)

# #pd.read_sql_query automaticamente crea el cursos y nos devuleve los datos como los nombre de las
# #columnas de la BBDD, solo le tenemos que pasaar la query y la conexion
# print(pd.read_sql_query("select * from alumnos",conn))


