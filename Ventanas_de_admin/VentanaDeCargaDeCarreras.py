import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox as MessageBox

import re

#Esto lo hago si trabajo directo aca, ya que no me tomaria los modulos de la carpeta de atras
#cuando inicie desde ventana principal, ya no va a ser necesario
# import sys
# sys.path.append('D:\\escritorio\\Python\\Sistema_de_gestor_universitario')




import MiExcepcion
import ConectorBD
import Ayudadores as ayuda


class VentanaDeCargaDeCarreras(tk.Toplevel):
    
    def __init__(self, ingresante, padre, *args, **kwargs):
        self.padre= padre
        self.ingresante = ingresante
        super().__init__(*args, **kwargs)
        
        menu = tk.Menu()
        menu_ventanas = tk.Menu(menu, tearoff=False)
        
        self.bind_all("<Control-m>", self.ventanaMaterias)
        menu_ventanas.add_command(label= "Materias", accelerator="Ctrl+m", command=self.ventanaMaterias)
        
        self.bind_all("<Control-a>", self.ventanaAlumnos)
        menu_ventanas.add_command(label= "Alumnos", accelerator="Ctrl+a", command=self.ventanaAlumnos)
        
        self.bind_all("<Control-d>", self.ventanaDocentes)
        menu_ventanas.add_command(label= "Docentes", accelerator="Ctrl+d", command=self.ventanaDocentes)     
        
        self.bind_all("<Control-g>", self.ventanaGraficos)
        menu_ventanas.add_command(label= "Graficos", accelerator="Ctrl+g", command=self.ventanaGraficos)  
       
       
        menu_ventanas.add_separator()

        self.bind_all("<Control-s>", self.volverInicio)
        menu_ventanas.add_command(label= "Salir", accelerator="Ctrl+s", command=self.volverInicio)
        
        menu.add_cascade(menu=menu_ventanas, label="Ventanas")
        
        
        self.config(bg=ayuda.color, menu=menu)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.geometry(ayuda.localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),550,450))
        self.title("Carga de carreras")
        self.label = ttk.Label(self, text=f"Bienvenido {ingresante}", font= tkFont.Font(family="Arial", size=16), foreground="green", background=ayuda.color)
        self.label.place(x=0,y=0)
        self.resizable(0,0)
        
        self.focus()
        self.crearElementosDePagina()
        
        self.nuevo()
        
        self.id = 0
        
        self.nombre.focus()
        
    def crearElementosDePagina(self):
        
        labelNombre = ttk.Label(self, text="Nombre de la carrera:", background=ayuda.color)
        labelNombre.place(x=20,y=80)
        self.nombre = ttk.Entry(self,width=30,validate="key",validatecommand= (self.register(ayuda.entradaConLimite), "%P", 30))
        self.nombre.place(x=20, y= 100)
        self.nombre.bind("<Return>", lambda x: self.duracion.focus())
        
        labelDuracion = ttk.Label(self, text="Duracion de la carrera:", background=ayuda.color)
        labelDuracion.place(x=230,y=80)
        self.duracion = ttk.Entry(self,justify=tk.RIGHT,validate="key",validatecommand= (self.register(ayuda.numeroConComa),"%S", "%P", 1,2))
        self.duracion.place(x=230, y= 100)
        self.duracion.bind("<Return>", lambda x: self.altaDeCarrera())
        
        
        lim = ttk.Button(self,text="Limpiar", command=self.limpiarTodo,width=9)
        lim.place(x=415,y=65)
        
        self.ingresar = ttk.Button(self,text="Ingresar", command=self.altaDeCarrera,width=9)
        self.ingresar.place(x=380,y=97)
        
        self.act = ttk.Button(self,text="Actualizar", command=self.actualizar,width=9)
        self.act.place(x=450,y=97)
        
        self.eli = ttk.Button(self,text="Eliminar", command=self.eliminar,width=9)
        self.eli.place(x=415,y=130)
        
        
        
        self.Busqueda = ttk.Entry(self,width=70) 
        self.Busqueda.place(x=50,y=190)
        
       
        self.Busqueda.bind("<KeyRelease>", self.buscar)
        
        
        labelListbox = ttk.Label(self, text=f"ID    Nombre{ayuda.crearEspacios(24)} Duracion", background=ayuda.color,font= tkFont.Font(family="Courier", size=9))
        labelListbox.place(x=20,y=230)      
        self.listbox = tk.Listbox(self,width=70, font= tkFont.Font(family="Courier", size=9),activestyle=tk.NONE)
        
        #'<Double-1>' es el evento doble click
        self.listbox.bind('<Double-1>', self.recuperar)
        self.listbox.bind('<Triple-1>', self.mostrarAlumnos)
        
        
        self.obtenerCarreras()

        self.listbox.place(x=20,y=250)
        
    def recuperar(self,evento):
        dato : str = self.listbox.get(self.listbox.curselection())
        id = int(dato.split(" ")[0])
        
        query = f"""select *
                    from carreras
                    where id = {id}"""
                    
        try:
            datos = ConectorBD.run_query(query=query)[0]
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        self.limpiar()
        
        self.id= datos[0]
        self.nombre.insert(0,datos[1])
        self.duracion.insert(0,datos[2])
        self.viejo()
        self.nombre.focus()
    
    def buscar(self,evento):
        if self.Busqueda.get() != "":
                
            query = f"""select *
                    from carreras
                    order by id"""
                    
            try:
                datos = ConectorBD.run_query(query=query)
            except Exception as e:           
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
            
            lista = []
            
            for dato in datos:
                consulta = f"{ayuda.formatoConCeros(str(dato[0]),5)}  {dato[1]} {dato[2]}"
                consulta = consulta.upper()
                
                if consulta.find(self.Busqueda.get().upper()) != -1:
                    lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}{ayuda.crearEspacios(30-len(dato[1]))} {dato[2]}")
            
            self.listbox.delete(0,tk.END)
            self.listbox.insert(0,*lista)
        else:
            self.obtenerCarreras()      
        
    
    def altaDeCarrera(self):
        
        if self.id != 0:
            self.actualizar()
        
        else:
        
            query = f"INSERT INTO carreras (nombre,duracion) VALUES ('{self.nombre.get()}',{self.duracion.get()})" 
            
            try:
                self.validar()  
                ConectorBD.run_query(query=query)
                self.limpiar()
                self.obtenerCarreras()
                self.nuevo()
                
            except MiExcepcion.MiExcepcion as e:
                MessageBox.showwarning("Alerta", 
                    f"{e}")
                
            except Exception as e:
                
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
                
            
            self.nombre.focus()

    
    def obtenerCarreras(self):
        self.listbox.delete(0,tk.END)
        
        query = f"""select * from carreras"""
                
        try:
            datos = ConectorBD.run_query(query=query)
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        lista = []
        
        for dato in datos:

            lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}{ayuda.crearEspacios(30-len(dato[1]))} {dato[2]}")
        
        self.listbox.insert(0,*lista)
    
    def validar(self):
        ayuda.validar_string(self.nombre.get())  
        
        if self.nombre.get() == "" or len(self.nombre.get().replace(" ","")) == 0 or self.duracion.get() == "":
            raise MiExcepcion.MiExcepcion("Faltan datos")
        
        elif float(self.duracion.get()) == 0:
            raise MiExcepcion.MiExcepcion("La duracion debe ser mayor a 0")

            
        
        
    def volverInicio(self, event=None):
         self.destroy()
         self.padre.deiconify()
    
    def cerrar_app(self):
        self.padre.destroy()
    
    def ventanaMaterias(self, event=None):
        from Ventanas_de_admin.VentanaDeCargaDeMaterias import VentanaDeAltasDeMaterias

        self.ventanaDeDocente = VentanaDeAltasDeMaterias(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
        
    def ventanaAlumnos(self, event=None):
        from Ventanas_de_admin.VentanaDeCargaDeAlumnos import VentanaDeAltasDeAlumnos

        self.ventanaDeDocente = VentanaDeAltasDeAlumnos(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
        
    def ventanaDocentes(self, event=None):
        from Ventanas_de_admin.VentanaDeCargaDeDocentes import VentanaDeAltasDeDocentes

        self.ventanaDeDocente = VentanaDeAltasDeDocentes(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
        
    def ventanaGraficos(self, event=None):
        from Ventanas_de_admin.VentanaGraficos import VentanaGraficos
        
        self.ventanaGraficos = VentanaGraficos(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
    
    def limpiar(self):
        self.nombre.delete(0,tk.END)
        self.duracion.delete(0,tk.END)
        self.id = 0
            
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
        query = f"delete from carreras where id ={self.id}" 
        try:
                 
            ConectorBD.run_query(query=query)
            self.limpiarTodo()
            self.obtenerCarreras()
            
        except Exception as e:
            
            if type(e).__name__ == "IntegrityError":
                MessageBox.showwarning("Alerta", 
                "Esta carrera tiene alumnos inscriptos, no se puede borrar")
            else:
                
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
        
        self.nombre.focus()
            
        
        
        
    def actualizar(self):
        
        query = f"""UPDATE carreras
        SET nombre = '{self.nombre.get()}', duracion = {self.duracion.get()}
        WHERE id={self.id}"""
        
        try:
            
            self.validar()
            ConectorBD.run_query(query=query)
            self.limpiarTodo()
            self.obtenerCarreras()
            
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
                from alumnos a inner join alumnos_carreras ac on ac.id_alumno = a.id
                where ac.id_carrera = {id}"""
                
        try:
            datos = ConectorBD.run_query(query=query)
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        lista = []
        
        for dato in datos:

            lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}{ayuda.crearEspacios(20-len(dato[1]))} {dato[2]}{ayuda.crearEspacios(20-len(dato[2]))} {dato[4]} {dato[3]}")
        
        
        dialogo = ayuda.ventanaDeMostrar(f"alumnos de la carrera {self.listbox.get(self.listbox.curselection())[6:36]}",lista)
        dialogo.grab_set()
            
        
# root = VentanaDeCargaDeCarreras(ingresante="ad", padre=None)
# root.mainloop()