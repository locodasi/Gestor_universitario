import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox as MessageBox

import re

import MiExcepcion
import ConectorBD
import Ayudadores as ayuda


class VentanaDeAltasDeMaterias(tk.Toplevel):
    def __init__(self, ingresante, padre, *args, **kwargs):
        
        self.padre = padre
        self.ingresante = ingresante
        super().__init__(*args, **kwargs)
        
        #Creo el menu
        menu = tk.Menu()
        # Crear el primer menú.
        menu_ventanas = tk.Menu(menu, tearoff=False)
        

        self.bind_all("<Control-d>", self.ventanaDocente)
        menu_ventanas.add_command(label= "Docentes", accelerator="Ctrl+d", command=self.ventanaDocente)     
        
        self.bind_all("<Control-a>", self.ventanaAlumnos)
        menu_ventanas.add_command(label= "Alumnos", accelerator="Ctrl+a", command=self.ventanaAlumnos)  
       
        self.bind_all("<Control-c>", self.ventanaCarreras)
        menu_ventanas.add_command(label= "Carreras", accelerator="Ctrl+c", command=self.ventanaCarreras)  
       
        self.bind_all("<Control-g>", self.ventanaGraficos)
        menu_ventanas.add_command(label= "Graficos", accelerator="Ctrl+g", command=self.ventanaGraficos)         
       
        menu_ventanas.add_separator()
         # Asociar el atajo del teclado del menú "Salir".
        self.bind_all("<Control-s>", self.volverInicio)
        menu_ventanas.add_command(label= "Salir", accelerator="Ctrl+s", command=self.volverInicio)
       
        
        # Agregarlo a la barra.
        menu.add_cascade(menu=menu_ventanas, label="Ventanas") 
        
        
        self.config(bg=ayuda.color, menu=menu)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        
        self.geometry(ayuda.localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),950,450))
        self.title("Carga de materias")
        self.label = ttk.Label(self, text=f"Bienvenido {ingresante}", font= tkFont.Font(family="Arial", size=16), foreground="green", background=ayuda.color)
        self.label.place(x=0,y=0)
        self.resizable(0,0)
        
        self.focus()
        self.crearElementosDePagina()
        
        self.nuevo()
        
        self.id = 0
        
        self.nombre.focus()
        self.focus()
        
    def crearElementosDePagina(self):
        
        labelCarrera = ttk.Label(self, text="Carrera a la que pertenece:", background=ayuda.color)
        labelCarrera.place(x=250,y=20)
        self.comboCarrera = ttk.Combobox(self,state="readonly", values=self.obtenerCarreras(), width=40)
        self.comboCarrera.place(x=250, y=40)
        self.comboCarrera.current(0)
        
        labelNombre = ttk.Label(self, text="Nombre de la materia:", background=ayuda.color)
        labelNombre.place(x=20,y=80)
        self.nombre = ttk.Entry(self,validate="key",validatecommand= (self.register(ayuda.entradaConLimite), "%P", 30))       
        self.nombre.place(x=20, y= 100)
        
        #Return es cunado haya un enter
        self.nombre.bind("<Return>", lambda x: self.desde1.focus())
        labeldia = ttk.Label(self, text="Dia de la materia:", background=ayuda.color)
        labeldia.place(x=170,y=80)
        self.combo = ttk.Combobox(self,state="readonly", values=["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"], width=13)
        self.combo.place(x=170, y=100)
        self.combo.current(0)
        
        labeldesde = ttk.Label(self, text="Desde:", background=ayuda.color)
        labeldesde.place(x=290,y=80)
        self.desde1 = ttk.Entry(self, width=3,justify=tk.RIGHT,validate="key",validatecommand= (self.register(ayuda.entradaConNumerosYLimite), "%S", "%P", 2)) 
        self.desde1.place(x=290,y=100)
        self.desde1.bind("<Return>", lambda x: self.desde2.focus())
        
        l = tk.Label(self,text=":", background=ayuda.color)
        l.place(x=312,y=100)
        
        self.desde2 = ttk.Entry(self, width=3,justify=tk.RIGHT,validate="key",validatecommand= (self.register(ayuda.entradaConNumerosYLimite), "%S", "%P", 2)) 
        self.desde2.place(x=320,y=100)
        self.desde2.bind("<Return>", lambda x: self.hasta1.focus())
            
        labelhasta = ttk.Label(self, text="Hasta:", background=ayuda.color)
        labelhasta.place(x=350,y=80)
        self.hasta1 = ttk.Entry(self,width=3,justify=tk.RIGHT,validate="key",validatecommand= (self.register(ayuda.entradaConNumerosYLimite), "%S", "%P", 2)) 
        self.hasta1.place(x=350,y=100)
        self.hasta1.bind("<Return>", lambda x: self.hasta2.focus())
        
        ll = tk.Label(self,text=":", background=ayuda.color)
        ll.place(x=372,y=100)
        
        self.hasta2 = ttk.Entry(self,width=3,justify=tk.RIGHT, validate="key",validatecommand= (self.register(ayuda.entradaConNumerosYLimite), "%S", "%P", 2))
        self.hasta2.place(x=380,y=100)
        
        labeldocente = ttk.Label(self, text="Docente de la materia:", background=ayuda.color)
        labeldocente.place(x=420,y=80)
        self.comboDocente = ttk.Combobox(self,state="readonly", values=self.obtenerDocentes(),width=33)
        self.comboDocente.place(x=420, y=100)
        self.comboDocente.current(0)
        
        
        lim = ttk.Button(self,text="Limpiar", command=self.limpiarTodo,width=9)
        lim.place(x=685,y=65)
        
        self.ingresar = ttk.Button(self,text="Ingresar", command=self.altaDeMateria,width=9)
        self.ingresar.place(x=650,y=97)
        
        self.act = ttk.Button(self,text="Actualizar", command=self.actualizar,width=9)
        self.act.place(x=720,y=97)
        
        self.eli = ttk.Button(self,text="Eliminar", command=self.eliminar,width=9)
        self.eli.place(x=685,y=130)
        
        self.corre = ttk.Button(self,text="Correlativas", command=self.correlativas)
        self.corre.place(x=350,y=138)
        
        
        self.Busqueda = ttk.Entry(self,width=105) 
        self.Busqueda.place(x=50,y=190)
        
        #KeyRelease es luego de levantar la tecla
        self.Busqueda.bind("<KeyRelease>", self.buscar)
        
        
        labelListbox = ttk.Label(self, text=f"ID    Carrera{ayuda.crearEspacios(23)} Materia{ayuda.crearEspacios(23)} Dia       Desde Hasta Nombre Docente{ayuda.crearEspacios(6)} Apellido Docente",font= tkFont.Font(family="Courier", size=9), background=ayuda.color)
        labelListbox.place(x=20,y=230)      
        self.listbox = tk.Listbox(self,width=130, font= tkFont.Font(family="Courier", size=9),activestyle=tk.NONE)
        
        #'<Double-1>' es el evento doble click
        self.listbox.bind('<Double-1>', self.recuperar)
        self.listbox.bind('<Triple-1>', self.mostrarAlumnos)
        
        
        self.obtenerMaterias()

        self.listbox.place(x=20,y=250)
        
    def recuperar(self, evento):
        dato : str = self.listbox.get(self.listbox.curselection())
        id = int(dato.split(" ")[0])
        
        query = f"""select m.id, m.nombre, m.dia, m.desde, m.hasta, d.nombre, d.apellido, c.nombre
                    from materias m inner join docentes d on m.id_docente = d.id inner join carreras c on m.id_carrera = c.id
                    where m.id = {id}
                    order by m.id"""
                    
        try:
            datos = ConectorBD.run_query(query=query)[0]
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
        
        self.limpiar()
               
        self.id = datos[0]
        self.nombre.insert(0,datos[1])
        
        #esta es solo para cunado llamo a la ventana correlativas
        self.materia = datos[1]
        
        self.combo.set(datos[2])
        
        desde : str = datos[3]
        desde = desde.split(":")
        self.desde1.insert(0,desde[0]) 
        self.desde2.insert(0,desde[1]) 
        
        hasta : str = datos[4]
        hasta = hasta.split(":")
        self.hasta1.insert(0,hasta[0])
        self.hasta2.insert(0,hasta[0])
        
        self.comboDocente.set(datos[6] + "," + datos[5])
        
        self.comboCarrera.set(datos[7])
        
        self.viejo()
        
    def buscar(self, evento):
        
        if self.Busqueda.get() != "":
                
            query = f"""select m.id, m.nombre, m.dia, m.desde, m.hasta, d.nombre, d.apellido, c.nombre
                    from materias m inner join docentes d on m.id_docente = d.id inner join carreras c on m.id_carrera = c.id
                    order by m.id"""
                    
            try:
                datos = ConectorBD.run_query(query=query)
            except Exception as e:           
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
            
            lista = []
            
            for dato in datos:
                consulta = f"{ayuda.formatoConCeros(str(dato[0]),5)}  {dato[7]}{ayuda.crearEspacios(30-len(dato[7]))} {dato[1]} {dato[2]} {dato[3]} {dato[4]} {dato[5]} {dato[6]}"
                consulta = consulta.upper()
                
                if consulta.find(self.Busqueda.get().upper()) != -1:
                    lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[7]}{ayuda.crearEspacios(30-len(dato[7]))} {dato[1]}{ayuda.crearEspacios(30-len(dato[1]))} {dato[2]}{ayuda.crearEspacios(9-len(dato[2]))} {ayuda.crearEspacios(5-len(dato[3]))}{dato[3]} {ayuda.crearEspacios(5-len(dato[4]))}{dato[4]} {dato[5]}{ayuda.crearEspacios(20-len(dato[5]))} {dato[6]}{ayuda.crearEspacios(20-len(dato[6]))}")
            
            self.listbox.delete(0,tk.END)
            self.listbox.insert(0,*lista)
        else:
            self.obtenerMaterias()        
                    
        
        
    def obtenerMaterias(self):
        self.listbox.delete(0,tk.END)
        
        query = f"""select m.id, m.nombre, m.dia, m.desde, m.hasta, d.nombre, d.apellido, c.nombre
                from materias m inner join docentes d on m.id_docente = d.id inner join carreras c on m.id_carrera = c.id
                order by m.id"""
                
        try:
            datos = ConectorBD.run_query(query=query)
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        lista = []
        
        for dato in datos:

            lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[7]}{ayuda.crearEspacios(30-len(dato[7]))} {dato[1]}{ayuda.crearEspacios(30-len(dato[1]))} {dato[2]}{ayuda.crearEspacios(9-len(dato[2]))} {ayuda.crearEspacios(5-len(dato[3]))}{dato[3]} {ayuda.crearEspacios(5-len(dato[4]))}{dato[4]} {dato[5]}{ayuda.crearEspacios(20-len(dato[5]))} {dato[6]}{ayuda.crearEspacios(20-len(dato[6]))}")
        
        self.listbox.insert(0,*lista)
        
    def obtenerDocentes(self):
        query = f"select nombre,apellido from docentes where id > 1" 
        
        lista = []
        
        try:
        #Obtengo los datos como una tula con tuplas
            datos = ConectorBD.run_query(query=query)
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")

        #Si devulevo los datos nomas me mostraria todo lo pedido EJ: gaby fradkin
        #por cada posicion del combobox, PERO si el apellido fuera Da Silva, me 
        #Apareceria entre {}, asi que de esta manera lo evito y hago que aparezcan como yo quiero
        for dato in datos:
            lista.append(f"{dato[1]},{dato[0]}")
        
        return(lista)

    def obtenerCarreras(self):
        query = f"select nombre,duracion from carreras" 
        
        lista = []
        
        try:
        #Obtengo los datos como una tula con tuplas
            datos = ConectorBD.run_query(query=query)
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")

        #Si devulevo los datos nomas me mostraria todo lo pedido EJ: gaby fradkin
        #por cada posicion del combobox, PERO si el apellido fuera Da Silva, me 
        #Apareceria entre {}, asi que de esta manera lo evito y hago que aparezcan como yo quiero
        for dato in datos:
            lista.append(f"{dato[0]}")
        
        return(lista)


        
    def volverInicio(self, event=None):
         self.destroy()
         self.padre.deiconify()
    
    def cerrar_app(self):
        self.padre.destroy()
    
    def correlativas(self):
        ventana = ayuda.VentanaCorrelativas(idCarrera=self.obtenerIdCarrera(), idMateria=self.id, materia=self.materia)
        ventana.grab_set()
        ventana.focus()
        ventana.Busqueda.focus()
    
    def altaDeMateria(self):
        
        desde = f"{self.desde1.get()}:{self.desde2.get()}"
        hasta = f"{self.hasta1.get()}:{self.hasta2.get()}"
        id = self.obtenerIdDocente()
        id_carrera = self.obtenerIdCarrera()
        query = f"INSERT INTO materias (nombre,dia,desde,hasta,id_docente,id_carrera) VALUES ('{self.nombre.get()}','{self.combo.get()}','{desde}','{hasta}',{id}, {id_carrera})" 
        try:
            
            self.validar()      
            ConectorBD.run_query(query=query)
            self.limpiar()
            self.obtenerMaterias()
            self.nuevo()
            
        except MiExcepcion.MiExcepcion as e:
            MessageBox.showwarning("Alerta", 
                f"{e}")
            
        except Exception as e:
            
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
        
        

    def validar(self):
        #Valido el string para que no me rompa la BD
        ayuda.validar_string(self.nombre.get())  

        if self.nombre.get() == "" or len(self.nombre.get().replace(" ","")) == 0:
            raise MiExcepcion.MiExcepcion("Faltan datos")
        
        elif int(self.desde1.get()) > int(self.hasta1.get()):
             raise MiExcepcion.MiExcepcion("desde no puede ser mayor a hasta")
        
        elif int(self.desde1.get()) >= 24 or int(self.hasta1.get()) >= 24 or int(self.desde2.get()) >= 60 or int(self.hasta2.get()) >= 60:
            raise MiExcepcion.MiExcepcion("Horarios invalidos")
         
        elif int(self.desde1.get()) == int(self.hasta1.get()):
            
            if int(self.desde2.get()) > int(self.hasta2.get()):
                raise MiExcepcion.MiExcepcion("desde no puede ser mayor a hasta")
            
            if int(self.desde2.get()) == int(self.hasta2.get()):
                raise MiExcepcion.MiExcepcion("No tiene sentido que los horarios sean iguales")
        
    def obtenerIdDocente(self):
        apellido,nombre = self.comboDocente.get().split(",")
        query = f"select id from docentes where nombre='{nombre}' and apellido='{apellido}'"
        
        try:
            
            return ayuda.ObtenerId(ConectorBD.run_query(query=query))
        
        except Exception as e:
            
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
        
    def obtenerIdCarrera(self):
        nombre = self.comboCarrera.get()
        query = f"select id from carreras where nombre='{nombre}'"
        
        try:
            return ayuda.ObtenerId(ConectorBD.run_query(query=query))
        
        except Exception as e:
            
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")

            
        
        
    def ventanaDocente(self, event=None):
        from Ventanas_de_admin.VentanaDeCargaDeDocentes import VentanaDeAltasDeDocentes

        self.destroy()
        self.ventanaDeDocente = VentanaDeAltasDeDocentes(ingresante=self.ingresante, padre=self.padre)
    
    def ventanaAlumnos(self, event=None):
        from Ventanas_de_admin.VentanaDeCargaDeAlumnos import VentanaDeAltasDeAlumnos

        self.ventanaDeAlumnos = VentanaDeAltasDeAlumnos(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
    
    def ventanaCarreras(self, event=None):
        from Ventanas_de_admin.VentanaDeCargaDeCarreras import VentanaDeCargaDeCarreras

        self.ventanaDeCarreras = VentanaDeCargaDeCarreras(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
        
    def ventanaGraficos(self, event=None):
        from Ventanas_de_admin.VentanaGraficos import VentanaGraficos
        
        self.ventanaGraficos = VentanaGraficos(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
        
    def limpiar(self):
        self.nombre.delete(0,tk.END)
        self.desde1.delete(0,tk.END)
        self.desde2.delete(0,tk.END)
        self.hasta1.delete(0,tk.END)
        self.hasta2.delete(0,tk.END)
    
    def limpiarTodo(self):
        self.limpiar()
        self.nuevo()
    
    def nuevo(self):
        self.act['state'] = tk.DISABLED
        self.eli['state'] = tk.DISABLED
        self.corre['state'] = tk.DISABLED
        self.ingresar['state'] = tk.NORMAL
        
    
    def viejo(self):
        self.act['state'] = tk.NORMAL
        self.eli['state'] = tk.NORMAL
        self.corre['state'] = tk.NORMAL
        self.ingresar['state'] = tk.DISABLED
    
    def eliminar(self):
        query = f"delete from materias where id ={self.id}" 
        try:
                 
            ConectorBD.run_query(query=query)
            self.limpiarTodo()
            self.obtenerMaterias()
            
        except Exception as e:
            
            if type(e).__name__ == "IntegrityError":
                MessageBox.showwarning("Alerta", 
                "Esta materia tiene alumnos inscriptos, no se puede borrar")
            else:
                
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
        
        self.nombre.focus()
            
        
        
        
    def actualizar(self):
        
        desde = f"{self.desde1.get()}:{self.desde2.get()}"
        hasta = f"{self.hasta1.get()}:{self.hasta2.get()}"
        id = self.obtenerIdDocente()
        id_carrera = self.obtenerIdCarrera()
        
        query = f"""UPDATE materias
        SET nombre = '{self.nombre.get()}', dia = '{self.combo.get()}', desde = '{desde}', hasta = '{hasta}', id_docente = {id}, id_carrera = {id_carrera}
        WHERE id={self.id}"""
        try:
            
            self.validar()
            ConectorBD.run_query(query=query)
            self.limpiarTodo()
            self.obtenerMaterias()
        
        except MiExcepcion.MiExcepcion as e:
            MessageBox.showwarning("Alerta", 
                f"{e}")
            
            self.nombre.focus()
            
        except Exception as e:
            
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
        
        self.nombre.focus()
    
    def mostrarAlumnos(self, evento):
        
        dato : str = self.listbox.get(self.listbox.curselection())
        id = int(dato.split(" ")[0])
        
        query = f"""select a.id, a.nombre, a.apellido, a.mail, a.dni
                from alumnos a inner join alumnos_materias ac on ac.id_alumno = a.id
                where ac.id_materia = {id} and ac.estado = 'Cursando'"""
                
        try:
            datos = ConectorBD.run_query(query=query)
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        lista = []
        
        for dato in datos:

            lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}{ayuda.crearEspacios(20-len(dato[1]))} {dato[2]}{ayuda.crearEspacios(20-len(dato[2]))} {dato[4]} {dato[3]}")
        
        materia = self.listbox.get(self.listbox.curselection())[36:66]
        
        #Strip es como un tipo de los trim de VB, elimina los espacios del inicio y del final, pero no los del medio
        materia = materia.strip()
        dialogo = ayuda.ventanaDeMostrar(f"alumnos de la materia {materia} de la carrera {self.listbox.get(self.listbox.curselection())[6:36]}",lista)
        dialogo.grab_set()



# root = VentanaDeAltasDeMaterias(ingresante="ad", padre=None)
# root.mainloop()