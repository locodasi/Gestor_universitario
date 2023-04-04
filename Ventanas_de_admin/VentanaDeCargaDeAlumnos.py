import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox as MessageBox

import re

import MiExcepcion
import ConectorBD
import Ayudadores as ayuda


class VentanaDeAltasDeAlumnos(tk.Toplevel):
    
    def __init__(self, ingresante, padre, *args, **kwargs):
        self.padre= padre
        self.ingresante = ingresante
        super().__init__(*args, **kwargs)
        
        menu = tk.Menu()
        menu_ventanas = tk.Menu(menu, tearoff=False)
        
        self.bind_all("<Control-m>", self.ventanaMaterias)
        menu_ventanas.add_command(label= "Materias", accelerator="Ctrl+m", command=self.ventanaMaterias)
        
        self.bind_all("<Control-d>", self.ventanaDocentes)
        menu_ventanas.add_command(label= "Docentes", accelerator="Ctrl+d", command=self.ventanaDocentes)     
        
        self.bind_all("<Control-c>", self.ventanaCarreras)
        menu_ventanas.add_command(label= "Carreras", accelerator="Ctrl+c", command=self.ventanaCarreras)  

        self.bind_all("<Control-g>", self.ventanaGraficos)
        menu_ventanas.add_command(label= "Graficos", accelerator="Ctrl+g", command=self.ventanaGraficos)  
       
       
        menu_ventanas.add_separator()

        self.bind_all("<Control-s>", self.volverInicio)
        menu_ventanas.add_command(label= "Salir", accelerator="Ctrl+s", command=self.volverInicio)
       
        menu.add_cascade(menu=menu_ventanas, label="Ventanas")
        
        
        self.config(bg=ayuda.color, menu=menu)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.geometry(ayuda.localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),800,450))
        self.title("Carga de Alumnos")
        self.label = ttk.Label(self, text=f"Bienvenido {ingresante}", font= tkFont.Font(family="Arial", size=16), foreground="green", background=ayuda.color)
        self.label.place(x=0,y=0)
        self.resizable(0,0)
        
        self.focus()
        self.crearElementosDePagina()
        
        self.nuevo()
        
        self.id = 0
        
        self.nombre.focus()
        
    def crearElementosDePagina(self):
        
        labelNombre = ttk.Label(self, text="Nombre del Alumno:", background=ayuda.color)
        labelNombre.place(x=20,y=60)
        self.nombre = ttk.Entry(self,validate="key",validatecommand= (self.register(ayuda.entradaConLimite), "%P", 20))
        self.nombre.place(x=20, y= 80)
        self.nombre.bind("<Return>", lambda x: self.apellido.focus())
        
        labelApellido = ttk.Label(self, text="Apellido del Alumno:", background=ayuda.color)
        labelApellido.place(x=170,y=60)
        self.apellido = ttk.Entry(self,validate="key",validatecommand= (self.register(ayuda.entradaConLimite), "%P", 20))
        self.apellido.place(x=170, y= 80)
        self.apellido.bind("<Return>", lambda x: self.mail.focus())
        
        labelMail = ttk.Label(self, text="Mail del Alumno:", background=ayuda.color)
        labelMail.place(x=320,y=60)
        self.mail = ttk.Entry(self, width=35)
        self.mail.place(x=320, y= 80)
        self.mail.bind("<Return>", lambda x: self.dni.focus())
        
        labelDNI = ttk.Label(self, text="DNI del Alumno:", background=ayuda.color)
        labelDNI.place(x=550,y=60)
        self.dni = ttk.Entry(self,width=8,justify=tk.RIGHT,validate="key",validatecommand= (self.register(ayuda.entradaConNumerosYLimite), "%S", "%P", 8))
        self.dni.place(x=550, y= 80)
        self.dni.bind("<Return>", lambda x: self.altaDeAlumnos())
        
        lim = ttk.Button(self,text="Limpiar", command=self.limpiarTodo,width=9)
        lim.place(x=685,y=50)
        
        self.ingresar = ttk.Button(self,text="Ingresar", command=self.altaDeAlumnos,width=9)
        self.ingresar.place(x=650,y=77)
        
        self.act = ttk.Button(self,text="Actualizar", command=self.actualizar,width=9)
        self.act.place(x=720,y=77)
        
        self.eli = ttk.Button(self,text="Eliminar", command=self.eliminar,width=9)
        self.eli.place(x=685,y=110)
        
        
        label = ttk.Label(self,text="Ctrl+click para seleccionar muchas:", background=ayuda.color)
        label.place(x=75,y=130)
        self.listboxCarreras = tk.Listbox(self,selectmode=tk.EXTENDED, width=30, height=3)
        self.listboxCarreras.place(x=280,y=115)
        self.obtenerCarreras()
        
        
        self.Busqueda = ttk.Entry(self,width=105) 
        self.Busqueda.place(x=50,y=190)
        
       
        self.Busqueda.bind("<KeyRelease>", self.buscar)
        
        
        labelListbox = ttk.Label(self, text=f"ID    Nombre{ayuda.crearEspacios(14)} Apellido{ayuda.crearEspacios(12)} DNI         Email",font= tkFont.Font(family="Courier", size=9), background=ayuda.color)
        labelListbox.place(x=20,y=230)      
        self.listbox = tk.Listbox(self,width=107, font= tkFont.Font(family="Courier", size=9),activestyle=tk.NONE)
        
        #'<Double-1>' es el evento doble click
        self.listbox.bind('<Double-1>', self.recuperar)
        
        
        self.obtenerAlumnos()

        self.listbox.place(x=20,y=250)
    
    def recuperar(self,evento):
        dato : str = self.listbox.get(self.listbox.curselection())
        id = int(dato.split(" ")[0])
        
        query = f"""select *
                    from alumnos
                    where id = {id}
                    order by id"""
                    
        try:
            datos = ConectorBD.run_query(query=query)[0]
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        self.limpiar()
        
        self.id= datos[0]
        self.nombre.insert(0,datos[1])
        self.apellido.insert(0,datos[2])
        self.mail.insert(0,datos[3])
        self.dni.insert(0,datos[4])
        
        query = f"""select c.nombre
                    from alumnos_carreras ac inner join carreras c on ac.id_carrera = c.id
                    where ac.id_alumno = {self.id}"""
                    
        try:
            datos = ConectorBD.run_query(query=query)
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        for dato in datos:        
            
            for i in range(self.listboxCarreras.size()):
                if self.listboxCarreras.get(i) == dato[0]:
                    self.listboxCarreras.selection_set(i)
  
        self.viejo()
            
    def buscar(self,evento):
        if self.Busqueda.get() != "":
                
            query = f"""select *
                    from alumnos
                    order by id"""
                    
            try:
                datos = ConectorBD.run_query(query=query)
            except Exception as e:           
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
            
            lista = []
            
            for dato in datos:
                consulta = f"{ayuda.formatoConCeros(str(dato[0]),5)}  {dato[1]} {dato[2]} {dato[4]} {dato[3]}"
                consulta = consulta.upper()
                
                if consulta.find(self.Busqueda.get().upper()) != -1:
                    lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}{ayuda.crearEspacios(20-len(dato[1]))} {dato[2]}{ayuda.crearEspacios(20-len(dato[2]))} {dato[4]} {dato[3]}")
            
            self.listbox.delete(0,tk.END)
            self.listbox.insert(0,*lista)
        else:
            self.obtenerAlumnos()      
        
    
    def altaDeAlumnos(self):
        
        if self.id != 0:
            self.actualizar()
        else:
            
            query = f"INSERT INTO alumnos (nombre,apellido,mail,dni,contra) VALUES ('{self.nombre.get()}','{self.apellido.get()}','{self.mail.get()}', {self.dni.get()},'{self.dni.get()}')" 
            
            try:
                
                self.validar()      
                id=ConectorBD.run_query(query=query)
                
                for posicion in self.listboxCarreras.curselection():
                    query = f"insert into alumnos_carreras values({id},{self.obtenerIdCarrera(self.listboxCarreras.get(posicion))})"
                    ConectorBD.run_query(query=query)
                
                
                self.limpiar()
                self.obtenerAlumnos()
                self.nuevo()
                
            except MiExcepcion.MiExcepcion as e:
                MessageBox.showwarning("Alerta", 
                    f"{e}")
                self.mail.focus()
                
            except Exception as e:
                
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
            
    def obtenerIdCarrera(self,nombre):
        query = f"select id from carreras where nombre='{nombre}'"
        
        try:
            return ayuda.ObtenerId(ConectorBD.run_query(query=query))
        
        except Exception as e:
            
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
    
    def obtenerAlumnos(self):
        self.listbox.delete(0,tk.END)
        
        query = f"""select * from alumnos"""
                
        try:
            datos = ConectorBD.run_query(query=query)
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        lista = []
        
        for dato in datos:

            lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}{ayuda.crearEspacios(20-len(dato[1]))} {dato[2]}{ayuda.crearEspacios(20-len(dato[2]))} {dato[4]} {dato[3]}")
        
        self.listbox.insert(0,*lista)
    
    def obtenerCarreras(self):
        query = f"""select nombre from carreras"""
        
        try:
            datos = ConectorBD.run_query(query=query)
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        lista = []
        
        for dato in datos:

            lista.append(f"{dato[0]}")       
             
        self.listboxCarreras.insert(0,*lista)
    
    def validar(self):
        ayuda.validar_string(self.nombre.get())
        ayuda.validar_string(self.apellido.get())
        
        patron = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}"
        
        if self.nombre.get() == "" or len(self.nombre.get().replace(" ","")) == 0 or self.apellido.get() == "" or len(self.apellido.get().replace(" ","")) == 0 or len(self.listboxCarreras.curselection())==0:
            raise MiExcepcion.MiExcepcion("Faltan datos")
        
        elif not re.match(patron,self.mail.get()):
            raise MiExcepcion.MiExcepcion("Mail invalido")
        
        elif int(self.dni.get()) < 10000000 or int(self.dni.get()) > 99999999:
            raise MiExcepcion.MiExcepcion("DNI invalido")
            
        
        
    def volverInicio(self, event=None):
         self.destroy()
         self.padre.deiconify()
    
    def cerrar_app(self):
        self.padre.destroy()
    
    def ventanaDocentes(self, event=None):
        
        from Ventanas_de_admin.VentanaDeCargaDeDocentes import VentanaDeAltasDeDocentes

        self.ventanaDeDocente = VentanaDeAltasDeDocentes(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
    
    def ventanaMaterias(self, event=None):
        from Ventanas_de_admin.VentanaDeCargaDeMaterias import VentanaDeAltasDeMaterias
        
        self.ventanaDeDocente = VentanaDeAltasDeMaterias(ingresante=self.ingresante, padre=self.padre)
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
        self.apellido.delete(0,tk.END)
        self.mail.delete(0,tk.END)
        self.dni.delete(0,tk.END)
        self.listboxCarreras.selection_clear(0,tk.END)
    
    def limpiarTodo(self):
        self.limpiar()
        self.nuevo()
        
    def nuevo(self):
        self.act['state'] = tk.DISABLED
        self.eli['state'] = tk.DISABLED
        self.ingresar['state'] = tk.NORMAL
    
    def viejo(self):
        self.act['state'] = tk.NORMAL
        self.eli['state'] = tk.NORMAL
        self.ingresar['state'] = tk.DISABLED
    
    def eliminar(self):
        query = f"delete from Alumnos where id ={self.id}" 
        try:
                 
            ConectorBD.run_query(query=query)
            self.limpiarTodo()
            self.obtenerAlumnos()
            
        except Exception as e:
            
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        self.nombre.focus()
        
        
        
    def actualizar(self):
        
        query = f"""UPDATE alumnos
        SET nombre = '{self.nombre.get()}', apellido = '{self.apellido.get()}', mail = '{self.mail.get()}', dni = {self.dni.get()}
        WHERE id={self.id}"""
        try:
            
            self.validar()
            ConectorBD.run_query(query=query)
            query = f"delete from alumnos_carreras where id_alumno = {self.id}"
            ConectorBD.run_query(query=query)
            
            for posicion in self.listboxCarreras.curselection():
                query = f"insert into alumnos_carreras values({self.id},{self.obtenerIdCarrera(self.listboxCarreras.get(posicion))})"
                ConectorBD.run_query(query=query)
                
            self.limpiarTodo()
            self.obtenerAlumnos()
        
        except MiExcepcion.MiExcepcion as e:
            MessageBox.showwarning("Alerta", 
                f"{e}")
            
            self.nombre.focus()
            
        except Exception as e:
            
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
        
        self.nombre.focus()
        
        
        
        
# root = VentanaDeAltasDeAlumnos(ingresante="ad", padre=None)
# root.mainloop()