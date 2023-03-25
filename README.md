# Gestor_universitario

Aplicacion de escritorio

Aplicacion de Gestion universitario, progrado en python y MySQL con workbench

La aplicaion permite registrarse alumnos, docentes y al admin

El alumno podra anotarse a materias y ver sus notas
El docente podra cargar las notas de sus materias
El admin podra dar de alta a alumno, docentes y materias

En la carpeta BBDD esta la aquitectura de la base de datos, como el primer insert del admin en docentes, necesario para arrancar a usar el proyecto

Repaso de las ventanas:

IMPORTANTE: la mayoria de cajas de texto tienen que al presionar enter directamente te envie a la siguiente caja de texto, en algunas, si presionas enter, automaticamente te hacen el ingresar o modificar

VentanaDeCargaDeMaterias: -ABM de materias
                          -Doble click en un elemento de la listbox te permite traer esa materia para modificarla o eliminarla
                          -Triple click permite ver los alumnos anotados en esa materia
                          -La caja de texto arriba de la listbox permite buscar en la listbox, con cada tecla que pulses apareceran los items que contenta el texto dentro del cuadro, si esta vacio trae todas las materias
                          -Cuando seleccionas una materias podes pulsar el boton de correlativas, te llevara a otra ventana donde con solo hacer doble click, podras sumar esa materia como correlativa o sacarla, tambien tiene una caja de texto de busqueda

VentanaDeCargaDeDocentes: -ABM de docentes
                          -Doble click y busqueda igual que en VentanaDeCargaDeMaterias
                          -El DNI es la contraseña que se crea al dar el alta, no se modifica con el boton modificar
    
VentanaDeCargaDeAlumnos: -ABM de alumnos
                         -Comando iguales que VentanaDeCargaDeDocentes
                         -El DNI es la contraseña que se crea al dar el alta, no se modifica con el boton modificar
 
VentanaDeCargaDeCarreras: -ABM de carreras
                          -Comando iguales que VentanaDeCargaDeDocentes
                          -La duracion es float, con un numero entero y dos decimales
                          -Triple click permite ver los alumnos de esa carrera

VentanaDeMaterias: -Permite cursar o dejar materias
                   -Marcas las materias que queres cursar o dejar y presionas el boton, se enviara un mail al alumno que diga que logro bajarse como inscibirse en esas materias
                   -Solo apareceran en Materias:, quellas que respeten las correlativas
                   -En ver todas las materias, podras ver las materias de esa carrera con sus correlativas,tambien tiene una caja de texto de busqueda
                   -Doble click en las materias cursada o aprobadas, te dejara ver tus notas, y si haces doble click en alguna, podras ver la observacion del docente al completo
                   
VentanaDeNotas: -Podra ver los alumnos anotados en sus materias
                -Al hacer doble click en un alumno ira a la ventana para cargar notas
                -Con doble click podra recuperar la nota para modificarla o eliminarla
                -El boton aprobar estara disponible si hay al menos una nota, y al presionarlo aprobara al alumno, cerrando la ventana y eliminandolo de la listbox de alumnos
               
  
Aclaracion y consejo: En algunos Modulos, encotraran comentados:
 import sys
 sys.path.append('D:\\escritorio\\Python\\Sistema_de_gestor_universitario')

y

 root = VentanaDeMaterias(ingresante="ad", padre=None, id=1)
 root.mainloop()

Los ultimos dos permiten abrir directamnete el proyecto en esa ventana, por si se quiere modificar o observar algo especifico de esa ventana sin queres pasar por todo el proceso del proyecto, de entrar, contraseña, ir a esa ventana especifica, etc.

Los primeros dos Permiten poder usar los modulos de carpetas anteriores de la que estan usando, por eso va arriba con los imports y los veran en los modulos, de Ventanas_De_Admin, ya que si ejecutan ahi les dira que la carpeta ayudadores o conectorBD no existen, pero si agregan esas dos lineas, les funcionara


