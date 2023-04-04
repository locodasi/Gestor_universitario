import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox as MessageBox
import matplotlib.pyplot as plt
import seaborn as sns

import ConectorBD
import Ayudadores as ayuda



class VentanaGraficos(tk.Toplevel):
    
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

        self.bind_all("<Control-a>", self.ventanaAlumnos)
        menu_ventanas.add_command(label= "Alumnos", accelerator="Ctrl+a", command=self.ventanaAlumnos)  
       
       
        menu_ventanas.add_separator()

        self.bind_all("<Control-s>", self.volverInicio)
        menu_ventanas.add_command(label= "Salir", accelerator="Ctrl+s", command=self.volverInicio)
       
        menu.add_cascade(menu=menu_ventanas, label="Ventanas")
        
        
        self.config(bg=ayuda.color, menu=menu)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.geometry(ayuda.localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),800,450))
        self.title("Graficos")
        self.label = ttk.Label(self, text=f"Bienvenido {ingresante}", font= tkFont.Font(family="Arial", size=16), foreground="green", background=ayuda.color)
        self.label.place(x=0,y=0)
        self.resizable(0,0)
        
        self.focus()
        self.crearElementosDePagina()
        
    def crearElementosDePagina(self):
        label = ttk.Label(self,text="Tipo de grafico",background=ayuda.color)
        label.place(x=300,y=30)
        self.cb_tipo_grafico = ttk.Combobox(self,state="readonly", values=["Torta","Barra"], width=8)
        self.cb_tipo_grafico.place(x=300,y=50)
        self.cb_tipo_grafico.current(0)
        
        self.bbt_por_carrera = ttk.Button(self,text="Por carreras",command=self.graficoPorCarrera)
        self.bbt_por_carrera.place(x=50,y=100)
        
        label2 = ttk.Label(self,text="Carrera:",background=ayuda.color)
        label2.place(x=440,y=100)
        self.cb_carrera = ttk.Combobox(self,state="readonly", values=self.obtenerCarreras(), width=27)
        self.cb_carrera.place(x=490,y=100)
        self.cb_carrera.current(0)
        
        self.bbt_por_materia = ttk.Button(self,text="Por Materia",command=self.graficoPorMateria)
        self.bbt_por_materia.place(x=680,y=100)
        
        
    
    def graficoPorCarrera(self):
        query = f"""select c.nombre, count(ac.id_carrera)
                from carreras c inner join alumnos_carreras ac on ac.id_carrera = c.id
                group by c.nombre""" 
        
        lista_nombre = []
        lista_cant = []
        
        try:
        #Obtengo los datos como una tula con tuplas
            datos = ConectorBD.run_query(query=query)
            
            for nombre, cant in datos:
                lista_nombre.append(nombre)
                lista_cant.append(cant)
            
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        if self.cb_tipo_grafico.get() == "Barra":
            sns.barplot(x=lista_nombre,y=lista_cant)
            plt.title("Alumnos por carrera")
            plt.show()
        else:
            plt.pie(labels=lista_nombre,x=lista_cant,colors=sns.color_palette('bright'))
            plt.title("Alumnos por carrera")
            plt.show()
    
    def graficoPorMateria(self):
        query = f"""select m.nombre, count(am.id_materia)
                from carreras c inner join materias m on m.id_carrera = c.id left outer join alumnos_materias am on am.id_materia = m.id
                where c.nombre = '{self.cb_carrera.get()}'
                group by m.nombre""" 
        
        lista_nombre = []
        lista_cant = []
        
        try:
        #Obtengo los datos como una tula con tuplas
            datos = ConectorBD.run_query(query=query)
            
            for nombre, cant in datos:
                lista_nombre.append(nombre)
                lista_cant.append(cant)
            
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        if self.cb_tipo_grafico.get() == "Barra":
            sns.barplot(x=lista_nombre,y=lista_cant)
            plt.title(f"Alumnos por materias de la carrera de {self.cb_carrera.get()}")
            plt.show()
        else:
            plt.pie(labels=lista_nombre,x=lista_cant,colors=sns.color_palette('bright'))
            plt.title(f"Alumnos por materias de la carrera de {self.cb_carrera.get()}")
            plt.show()
    
    def obtenerCarreras(self):
        query = f"select nombre from carreras" 
        
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
            lista.append(dato[0])
        
        return lista
    
    
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
        
    def ventanaAlumnos(self, event=None):
        from Ventanas_de_admin.VentanaDeCargaDeAlumnos import VentanaDeAltasDeAlumnos
        self.ventanaDeAlumnos = VentanaDeAltasDeAlumnos(ingresante=self.ingresante, padre=self.padre)
        self.destroy()