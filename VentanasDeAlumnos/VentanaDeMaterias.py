import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox as MessageBox
import threading as hilos




# import sys
# sys.path.append('D:\\escritorio\\Python\\Sistema_de_gestor_universitario')

import MiExcepcion
import ConectorBD
import Ayudadores as ayuda



class VentanaDeMaterias(tk.Toplevel):
    
    def __init__(self, ingresante, padre, id, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.padre= padre
        self.ingresante = ingresante
        self.id = id
        
        menu = tk.Menu()
        menu_ventanas = tk.Menu(self, tearoff=False)
        
        self.bind_all("<Control-c>", self.cambiarContra)
        menu_ventanas.add_command(label= "Cambair contraseña", accelerator="Ctrl+c", command=self.cambiarContra)
        
        menu_ventanas.add_separator()
        
        self.bind_all("<Control-s>", self.volverInicio)
        menu_ventanas.add_command(label= "Salir", accelerator="Ctrl+s", command=self.volverInicio)
        
        
        menu.add_cascade(menu=menu_ventanas, label="Ventanas")
        
        self.config(bg=ayuda.color, menu=menu)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.geometry(ayuda.localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),800,450))
        self.title("Seleccion de Materias")
        self.label = ttk.Label(self, text=f"Bienvenido {ingresante}", font= tkFont.Font(family="Arial", size=16), foreground="green", background=ayuda.color)
        self.label.place(x=0,y=0)
        self.resizable(0,0)
        
        self.focus()
        self.crearElementosDePagina()
        
    def crearElementosDePagina(self):
        
        labelCarrera = ttk.Label(self,text="Carrera:",background=ayuda.color)
        labelCarrera.place(x=350,y=50)
        
        self.comboCarrera = ttk.Combobox(self,values=self.obtenerCarreras(),state="readonly",width=30)
        self.comboCarrera.place(x=280, y=70)
        self.comboCarrera.bind("<<ComboboxSelected>>", self.obtenerMaterias)
        self.comboCarrera.current(0)
        
        self.botonMaterias = ttk.Button(self,text="Ver todas las materias",command=self.verTodasMaterias)
        self.botonMaterias.place(x=320,y=100)
        labelMateria = ttk.Label(self,text="Materias:",background=ayuda.color)
        labelMateria.place(x=20,y=130)
        
        labelCursando = ttk.Label(self,text="Cursando:",background=ayuda.color)
        labelCursando.place(x=300,y=130)
        
        labelAprobado = ttk.Label(self,text="Aprobadas:",background=ayuda.color)
        labelAprobado.place(x=580,y=130)
        
        self.listboxMaterias = tk.Listbox(self, selectmode=tk.EXTENDED, height=16, width=25,activestyle=tk.NONE)
        self.listboxMaterias.place(x=20,y=150)
        
        botonCursar = ttk.Button(self,text="Cursar", command=self.cursarMateria)
        botonCursar.place(x=180,y=260)
        
        self.listboCursando = tk.Listbox(self, selectmode=tk.EXTENDED, height=16, width=25,activestyle=tk.NONE)
        self.listboCursando.place(x=300,y=150)
        self.listboCursando.bind("<Double-1>", lambda x : self.mostrarNotas(list="C"))
        
        botonDejar = ttk.Button(self,text="Dejar", command=self.dejarMateria)
        botonDejar.place(x=460,y=260)
        
        self.listboxAprobadas = tk.Listbox(self,height=16, width=25,activestyle=tk.NONE)
        self.listboxAprobadas.place(x=580,y=150)
        self.listboxAprobadas.bind("<Double-1>", lambda x : self.mostrarNotas(list="A"))
        
        label = ttk.Label(self,text="Ctrl+Click para seleccionara muchas",background=ayuda.color,font= tkFont.Font(family="Courier", size=13))
        label.place(x=230,y=415)
        
        self.obtenerMaterias()
    
    def verTodasMaterias(self):
        ventana = ayuda.VentanaVerMaterias(idCarrera=self.obtenerIdCarrera(), carrera= self.comboCarrera.get())
        ventana.grab_set()
        ventana.busqueda.focus()
        
    def obtenerCarreras(self):
        
        query = f"select c.nombre from carreras c inner join alumnos_carreras ac on ac.id_carrera = c.id where ac.id_alumno= {self.id} "
        
        try:
            
            datos = ConectorBD.run_query(query=query)
            
            lista = []
            
            for dato in datos:
                lista.append(dato[0])
            
            return lista
            
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
    def obtenerMaterias(self,evento=None):
        
        #Esta mal, no solo el inner join es inecesario, si no que si tengo mas alumnos anotados a las materias, entonces me daria un resultado amyor con materias repetidas
        # query = f"""select m.id, m.nombre, am.estado
        #         from materias m inner join carreras c on m.id_carrera = c.id left join alumnos_materias am on am.id_materia = m.id 
        #         where m.id_carrera = {self.obtenerIdCarrera()}"""
        
        #obtengo todas las materias de la carrera
        query = f"""select m.id, m.nombre
                from materias m 
                where m.id_carrera = {self.obtenerIdCarrera()}"""
                
        try:
            
            datos = ConectorBD.run_query(query=query)

            listaMaterias = []
            listaCursando = []
            listaAprobada = []
            
            
            for dato in datos:
                
                #Obtengo el esatado de la materia, si no retorna nada, es porque nunca la curse ni la aprobe
                query=f"""SELECT estado
                FROM alumnos_materias
                WHERE id_alumno = {self.id} AND id_materia = {dato[0]}"""
                estado = ConectorBD.run_query(query=query)
                if len(estado) == 0:
                    
                    id = str(dato[0])
                    
                    #me trae las correlativas
                    query = f"select id_correlativa from correlativas where id_materia = {id}"
                    
                    correlativas = ConectorBD.run_query(query=query)

                    #Si no tiene correlativas la suma ya que se puede cursar
                    if len(correlativas) == 0:                   
                        listaMaterias.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}")
                    else:
                        
                        #Muy ineficiente y compleja
                        
                        # #Esta es la base para pedir la correlativas del alumno
                        # query = f"""select m.id, m.nombre
                        #         from materias m inner join alumnos_materias am on am.id_materia = m.id inner join correlativas co on co.id_correlativa = m.id
                        #         where am.id_alumno = {self.id} and m.id_carrera = {self.obtenerIdCarrera()} and """
                        
                        # #Recorro la lista de las correlatibas y las voy agregando a la query
                        # #La idea es que yo estoy pidiendo que me traigan si tengo la correlativa aprobada
                        # #por eso recorro las listas de correlativas y las voy agregando al where
                        # #pero lo hago entre () y or asi si alguno no la tengo aun asi me trae las que si
                        # #siempre del mismo alumno, por que antes lo pusimos where am.id_alumno = {self.id}
                        # for corre in correlativas:
                        #     query += f"(co.id_correlativa = {corre[0]} and am.estado = 'Aprobada') or "
                        
                        # #Elimino el ultimo or del ultimo for
                        # query = query[:-3]
                        
                        # query += """
                        #          group by m.id"""
                        
                        #mejor asi
                        #En esta consulta el from me esta dando todas las querys de alumno_materia que sean materias que son correlativas de alguien
                        #Luego el where lo que hace, priemro) darme solo las que sean de mi alumno, por lo que ahora me daria los alumnos_materias de materias que sean correlativas de otro y que sean cursadas o hayan sido cursadas por mi.       2) darme aquellas materias que le hagan la correlativa a la materia que estoy buscando, por lo que ahora la tabla seria, alumno_materias de las de mi usuario y que le hagan correlativa a esta materia.                        3) que esten aprobadas, osea, aquellas alumno_materia, que le hagan la correlativa a mi materia y esten aprobadas.
                        #De esta manera lo que me retorna serian aquellas materias aprobadas por mi alumno que son correlativas a la materia que busco
                        query = f"""select *
                            from alumnos_materias am inner join correlativas co on co.id_correlativa = am.id_materia
                            where am.id_alumno = {self.id} and co.id_materia = {id} and am.estado = 'Aprobada'"""
           
                        correlativasAprobadas = ConectorBD.run_query(query=query)
                        
                        #Si la cantidad que tengo aprobada es la misma que de correlativas que necesita
                        #entonces puedo cursarla, si no no
                        if len(correlativasAprobadas) == len(correlativas):
                            listaMaterias.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}")
                        
                        
                elif estado[0][0] == "Cursando":
                    listaCursando.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}")
                
                elif estado[0][0] == "Aprobada":
                    listaAprobada.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}")
            
            self.listboxMaterias.delete(0,tk.END)
            self.listboxMaterias.insert(0,*listaMaterias)
            
            self.listboCursando.delete(0,tk.END)
            self.listboCursando.insert(0,*listaCursando)
            
            self.listboxAprobadas.delete(0,tk.END)
            self.listboxAprobadas.insert(0,*listaAprobada)
            
        except Exception as e:           
            print( type(e).__name__)
            print(e)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
        
    def obtenerIdCarrera(self):
        
        query = f"select id from carreras where nombre = '{self.comboCarrera.get()}'"
        
        try:
            
            datos = ConectorBD.run_query(query=query)
            
            return datos[0][0]
            
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
        
    def cursarMateria(self):
        
        #Para que no se ejecute si no hay nada seleccionado
        if len(self.listboxMaterias.curselection()) > 0:
            try:
                
                #Debo pasarlo a una lista para poder invertirlo y debo invertirlo porque si hago el for
                #en orden se terminan desconfigurando los metodos de los listbox
                #ya que al eliminar el primero los get, insert i delete me quedarian mal
                #Ej: luego de eliminar el 0, i seria = 1, pero ya que elimine el 0, el 1 ya no seria
                #El 1 que seleccione antes de iniciar el script, si no que seria el 2
                #Por eso simplemente debo agregarlos y eliminarlos en orden inversa para asi no romper todo
                lista = list(self.listboxMaterias.curselection())
                lista.reverse()
                
                materias = []
                
                for i in lista:
                    
                    query = f"insert into alumnos_materias (id_alumno, id_materia, estado) values ({self.id},{int(self.listboxMaterias.get(i)[0:5])}, 'Cursando')"
                    ConectorBD.run_query(query=query)
                                      
                    materias.append(self.listboxMaterias.get(i))
                    
                    self.listboCursando.insert(tk.END,self.listboxMaterias.get(i))
                    self.listboxMaterias.delete(i)
                    
                query = f"select mail, nombre, apellido from alumnos where id = {self.id}"
                datos = ConectorBD.run_query(query=query)
                    
                alumno = f"{datos[0][2]},{datos[0][1]}"
                
                hilo = hilos.Thread(target=ayuda.enviarEmailDeIngreso,kwargs={'materia':materias,'carrera':self.comboCarrera.get(),'alumno':alumno,'mail':datos[0][0]}, name="Hilo alta")
                hilo.start()
                #ayuda.enviarEmailDeIngreso(materia=materias,carrera=self.comboCarrera.get(), alumno=alumno, mail=datos[0][0])
               
            except Exception as e:           
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
            
            
    def dejarMateria(self):
        if len(self.listboCursando.curselection()) > 0:
            try:
                
                lista = list(self.listboCursando.curselection())
                lista.reverse()
                
                #hago materias para enviar en un solo mail varias inserciones o bajas de materias
                materias = []
                
                for i in lista:
                    
                    query = f"delete from alumnos_materias where id_alumno = {self.id} and id_materia = {int(self.listboCursando.get(i)[0:5])}"
                    ConectorBD.run_query(query=query)
                    
                    materias.append(self.listboCursando.get(i))
                    
                    self.listboxMaterias.insert(tk.END,self.listboCursando.get(i))
                    self.listboCursando.delete(i)
                
                query = f"select mail, nombre, apellido from alumnos where id = {self.id}"
                datos = ConectorBD.run_query(query=query)
                    
                alumno = f"{datos[0][2]},{datos[0][1]}"
                hilo = hilos.Thread(target=ayuda.enviarEmailDeBaja,kwargs={'materia':materias,'carrera':self.comboCarrera.get(),'alumno':alumno,'mail':datos[0][0]},name="Hilo baja")
                hilo.start()
                #ayuda.enviarEmailDeBaja(materia=materias,carrera=self.comboCarrera.get(), alumno=alumno, mail=datos[0][0])
               
                    
                    
            except Exception as e:           
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
    
    def mostrarNotas(self,list):
        
        if list == "C":
            dato : str = self.listboCursando.get(self.listboCursando.curselection())

        else:
            dato : str = self.listboxAprobadas.get(self.listboxAprobadas.curselection())
          
        id = int(dato[:5])
        materia = dato[5:]
        
        query = f"""select n.id, n.nota, n.tipo, n.observacion, n.dia
                from notas n inner join  alumnos a on a.id = n.id_alumno inner join materias m on m.id = n.id_materia
                where n.id_alumno = {self.id} and n.id_materia = {id}"""
                
        try:
            datos = ConectorBD.run_query(query=query)
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        lista = []
        
        for dato in datos:

            hasta = dato[3].find("\n")
            obs = dato[3][:hasta]
            lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[4]} {ayuda.crearEspacios(2-len(str(dato[1])))}{dato[1]}      {dato[2]}{ayuda.crearEspacios(20-len(dato[2]))} {obs[:15]}")
        
        #Strip es como un tipo de los trim de VB, elimina los espacios del inicio y del final, pero no los del medio
        materia = materia.strip()
        dialogo = ayuda.VentanaVerNotas(f"Notas de la materia {materia} de la carrera {self.comboCarrera.get()}",lista)
        dialogo.grab_set()
         
            
    def volverInicio(self, event=None):
         self.destroy()
         self.padre.deiconify()
    
    def cerrar_app(self):
        self.padre.destroy()
    
    def cambiarContra(self,evento=None):
        ventanaContra = ayuda.VentanaDeCambioDeContra(id=self.id, tabla="alumnos")
        ventanaContra.grab_set()
        ventanaContra.focus()
        ventanaContra.entrycontra.focus()
        
        
# root = VentanaDeMaterias(ingresante="ad", padre=None, id=1)
# root.mainloop()
