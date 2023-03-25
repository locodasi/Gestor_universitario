import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox as MessageBox

import re

import MiExcepcion
import ConectorBD
import Ayudadores as ayuda
import Ventanas_de_admin.VentanaDeCargaDeMaterias as VentanaDeCargaDeMaterias
import Ventanas_de_admin.VentanaDeCargaDeAlumnos as VentanaDeCargaDeAlumnos
import Ventanas_de_admin.VentanaDeCargaDeCarreras as VentanaDeCargaDeCarreras


class VentanaDeAltasDeDocentes(tk.Toplevel):
    
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
        
        self.bind_all("<Control-c>", self.ventanaCarreras)
        menu_ventanas.add_command(label= "Carreras", accelerator="Ctrl+c", command=self.ventanaCarreras)  
       
        menu_ventanas.add_separator()

        self.bind_all("<Control-s>", self.volverInicio)
        menu_ventanas.add_command(label= "Salir", accelerator="Ctrl+s", command=self.volverInicio)
        
        menu.add_cascade(menu=menu_ventanas, label="Ventanas")
        
        
        self.config(bg=ayuda.color, menu=menu)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.geometry(ayuda.localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),800,450))
        self.title("Carga de docentes")
        self.label = ttk.Label(self, text=f"Bienvenido {ingresante}", font= tkFont.Font(family="Arial", size=16), foreground="green", background=ayuda.color)
        self.label.place(x=0,y=0)
        self.resizable(0,0)
        
        self.focus()
        self.crearElementosDePagina()
        
        self.nuevo()
        
        self.id = 0
        
        self.nombre.focus()
        
    def crearElementosDePagina(self):
        
        labelNombre = ttk.Label(self, text="Nombre del docente:", background=ayuda.color)
        labelNombre.place(x=20,y=80)
        self.nombre = ttk.Entry(self,validate="key",validatecommand= (self.register(ayuda.entradaConLimite), "%P", 20))
        self.nombre.place(x=20, y= 100)
        self.nombre.bind("<Return>", lambda x: self.apellido.focus())
        
        labelApellido = ttk.Label(self, text="Apellido del docente:", background=ayuda.color)
        labelApellido.place(x=170,y=80)
        self.apellido = ttk.Entry(self,validate="key",validatecommand= (self.register(ayuda.entradaConLimite), "%P", 20))
        self.apellido.place(x=170, y= 100)
        self.apellido.bind("<Return>", lambda x: self.mail.focus())
        
        labelMail = ttk.Label(self, text="Mail del docente:", background=ayuda.color)
        labelMail.place(x=320,y=80)
        self.mail = ttk.Entry(self, width=35)
        self.mail.place(x=320, y= 100)
        self.mail.bind("<Return>", lambda x: self.dni.focus())
        
        labelDNI = ttk.Label(self, text="DNI del docente:", background=ayuda.color)
        labelDNI.place(x=550,y=80)
        self.dni = ttk.Entry(self,width=8,justify=tk.RIGHT,validate="key",validatecommand= (self.register(ayuda.entradaConNumerosYLimite), "%S", "%P", 8))
        self.dni.place(x=550, y= 100)
        
        #Se agrega lamda o a la funcion debo agregarle como parametro evento
        #Osea si la funcion es nombre(..), va con lambda y si es nombre(...,evento) puede ir sin
        self.dni.bind("<Return>", lambda x : self.altaDeDocente())
        
        
        lim = ttk.Button(self,text="Limpiar", command=self.limpiarTodo,width=9)
        lim.place(x=685,y=65)
        
        self.ingresar = ttk.Button(self,text="Ingresar", command=self.altaDeDocente,width=9)
        self.ingresar.place(x=650,y=97)
        
        self.act = ttk.Button(self,text="Actualizar", command=self.actualizar,width=9)
        self.act.place(x=720,y=97)
        
        self.eli = ttk.Button(self,text="Eliminar", command=self.eliminar,width=9)
        self.eli.place(x=685,y=130)
        
        
        
        self.Busqueda = ttk.Entry(self,width=105) 
        self.Busqueda.place(x=50,y=190)
        
       
        self.Busqueda.bind("<KeyRelease>", self.buscar)
        
        
        labelListbox = ttk.Label(self, text=f"ID    Nombre{ayuda.crearEspacios(14)} Apellido{ayuda.crearEspacios(12)} DNI         Email",font= tkFont.Font(family="Courier", size=9), background=ayuda.color)
        labelListbox.place(x=20,y=230)      
        self.listbox = tk.Listbox(self,width=107, font= tkFont.Font(family="Courier", size=9),activestyle=tk.NONE)
        
        #'<Double-1>' es el evento doble click
        self.listbox.bind('<Double-1>', self.recuperar)
        
        
        self.obtenerDocentes()

        self.listbox.place(x=20,y=250)
    
    def recuperar(self,evento):
        dato : str = self.listbox.get(self.listbox.curselection())
        id = int(dato.split(" ")[0])
        
        query = f"""select *
                    from docentes
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
        
        self.viejo()
    
    def buscar(self,evento):
        if self.Busqueda.get() != "":
                
            query = f"""select *
                    from docentes
                    where id > 1
                    order by id"""
                    
            try:
                datos = ConectorBD.run_query(query=query)
            except Exception as e:           
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
            
            lista = []
            
            for dato in datos:
                consulta = f"{ayuda.formatoConCeros(str(dato[0]),5)}  {dato[1]} {dato[2]} {dato[3]} {dato[4]}"
                consulta = consulta.upper()
                
                if consulta.find(self.Busqueda.get().upper()) != -1:
                    lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}{ayuda.crearEspacios(20-len(dato[1]))} {dato[2]}{ayuda.crearEspacios(20-len(dato[2]))} {dato[4]} {dato[3]}")
            
            self.listbox.delete(0,tk.END)
            self.listbox.insert(0,*lista)
        else:
            self.obtenerDocentes()      
        
    
    def altaDeDocente(self):
        
        if self.id != 0:
            self.actualizar()
        else:
        
            query = f"INSERT INTO docentes (nombre,apellido,mail,dni,contra) VALUES ('{self.nombre.get()}','{self.apellido.get()}','{self.mail.get()}',{self.dni.get()},'{self.dni.get()}')" 

            try:
                
                self.validar()      
                ConectorBD.run_query(query=query)
                self.limpiar()
                self.obtenerDocentes()
                self.nuevo()
                
            except MiExcepcion.MiExcepcion as e:
                MessageBox.showwarning("Alerta", 
                    f"{e}")
                self.mail.focus()
                
            except Exception as e:
                
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
    
    def obtenerDocentes(self):
        self.listbox.delete(0,tk.END)
        
        query = f"""select * from docentes where id > 1"""
                
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
    
    def validar(self):
        ayuda.validar_string(self.nombre.get())
        ayuda.validar_string(self.apellido.get())
        
        patron = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}"
        
        if self.nombre.get() == "" or len(self.nombre.get().replace(" ","")) == 0 or self.apellido.get() == "" or len(self.apellido.get().replace(" ","")) == 0:
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
    
    def ventanaMaterias(self, event=None):
        self.ventanaDeDocente = VentanaDeCargaDeMaterias.VentanaDeAltasDeMaterias(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
        
    def ventanaAlumnos(self, event=None):
        self.ventanaDeDocente = VentanaDeCargaDeAlumnos.VentanaDeAltasDeAlumnos(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
    
    def ventanaCarreras(self, event=None):
        self.ventanaDeCarreras = VentanaDeCargaDeCarreras.VentanaDeCargaDeCarreras(ingresante=self.ingresante, padre=self.padre)
        self.destroy()
    
    def limpiar(self):
        self.nombre.delete(0,tk.END)
        self.apellido.delete(0,tk.END)
        self.mail.delete(0,tk.END)
        self.dni.delete(0,tk.END)
    
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
        query = f"delete from docentes where id ={self.id}" 
        try:
                 
            ConectorBD.run_query(query=query)
            self.limpiarTodo()
            self.obtenerDocentes()
            
        except Exception as e:
            
            if type(e).__name__ == "IntegrityError":
                MessageBox.showwarning("Alerta", 
                "Este docente tiene materias a su cargo, no se puede borrar")
            else:
                
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
        
        self.nombre.focus()
            
        
        
        
    def actualizar(self):
        
        query = f"""UPDATE docentes
        SET nombre = '{self.nombre.get()}', apellido = '{self.apellido.get()}', mail = '{self.mail.get()}', dni = {self.dni.get()}
        WHERE id={self.id}"""
        try:
            
            self.validar()
            ConectorBD.run_query(query=query)
            self.limpiarTodo()
            self.obtenerDocentes()
            
        except MiExcepcion.MiExcepcion as e:
            MessageBox.showwarning("Alerta", 
                f"{e}")
            
            self.nombre.focus()
            
        except Exception as e:
            
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
        
        self.nombre.focus()
        
        
        
        
# root = VentanaDeAltasDeDocentes(ingresante="ad", padre=None)
# root.mainloop()