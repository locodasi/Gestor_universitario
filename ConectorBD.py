import MySQLdb 

DB_HOST = 'localhost' 
DB_USER = 'root' 
DB_PASS = 'lucas1234+' 
DB_NAME = 'gestor_universitario' 

def run_query(query=''): 
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
    conn = MySQLdb.connect(*datos) # Conectar a la base de datos 
    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 

    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select 
    
    elif query.upper().startswith('INSERT'): #Devuelve el id del dato ingresado
        conn.commit()
        data = cursor.lastrowid 
    else: 
        
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
 
    
    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 

    return data