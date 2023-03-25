import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox as MessageBox



import sys
sys.path.append('D:\\escritorio\\Python\\Sistema_de_gestor_universitario')

import Ayudadores as ayuda
import ConectorBD

class VentanaDeNotas(tk.Toplevel):
    
    def __init__(self, ingresante, padre, id, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.padre = padre
        self.id = id
        self.ingresante = ingresante
        
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
        
        self.geometry(ayuda.localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),600,350))
        self.title("Alta de notas")
        self.label = ttk.Label(self, text=f"Bienvenido {ingresante}", font= tkFont.Font(family="Arial", size=16), foreground="green", background=ayuda.color)
        self.label.place(x=0,y=0)
        self.resizable(0,0)
        
        self.focus()
        self.crearElementosDePagina()
        
    def crearElementosDePagina(self):
        
        #Pongo el listbox primero porque si lo pongo despues de obtenerAlumnos o Materias
        #Va a dar error, ya que en ambas termino llamando a obtenerAlumnos, y en ella estoy borrando
        #como insertando datos en la listbox, y si aun no la tenia declarada entonces no existirira y daria atributte error
        #por eso primero creo la listbox y luego la lineas que llaman codigo que lo utilia
        labelAlumnos = ttk.Label(self,text=f"ID    Nombre alumno{ayuda.crearEspacios(7)} Apellido alumno{ayuda.crearEspacios(3)}   Mail",font= tkFont.Font(family="Courier", size=9), background=ayuda.color)
        labelAlumnos.place(x=20,y=130)
        self.listboxAlumnos = tk.Listbox(self, width=80, font= tkFont.Font(family="Courier", size=9),activestyle=tk.NONE)
        self.listboxAlumnos.place(x=20,y=150)
        self.listboxAlumnos.bind('<Double-1>', self.cargaNotas)
        
        labelCarrera = ttk.Label(self,text="Carrera:",background=ayuda.color)
        labelCarrera.place(x=20,y=50)
        
        self.comboCarrera = ttk.Combobox(self,values=self.obtenerCarreras(),state="readonly",width=30)
        self.comboCarrera.place(x=20, y=70)
        self.comboCarrera.bind("<<ComboboxSelected>>", self.obtenerMaterias)
        self.comboCarrera.current(0)
        
        labelMateria = ttk.Label(self,text="Materias:",background=ayuda.color)
        labelMateria.place(x=240,y=50)
        self.comboMateria = ttk.Combobox(self,state="readonly",width=30)
        self.comboMateria.place(x=240,y=70)
        self.obtenerMaterias()
        self.comboMateria.bind("<<ComboboxSelected>>", self.obtenerAlumnos)
        self.comboMateria.current(0)
        self.obtenerAlumnos()
        
        
        
    
    def obtenerCarreras(self):
        query = f"""select c.nombre 
from materias m inner join docentes d on d.id = m.id_docente inner join carreras c on c.id = m.id_carrera 
where d.id = {self.id}
group by c.nombre"""
        
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
        
        query = f"""select nombre from materias where id_carrera = {self.obtenerIdCarrera()} and id_docente = {self.id} """
                
        try:
            
            datos = ConectorBD.run_query(query=query)

            lista = []
            
            for dato in datos:
                lista.append(dato[0])

            
            self.comboMateria['values'] = lista
            self.comboMateria.current(0)
            self.obtenerAlumnos()
            
            
        except Exception as e:           
            print( type(e).__name__)
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
    
    def obtenerIdMateria(self):
        
        query = f"select id from materias where nombre = '{self.comboMateria.get()}'"
        
        try:
            
            datos = ConectorBD.run_query(query=query)

            return datos[0][0]
            
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
    
    def obtenerAlumnos(self,evento=None):
        
        query = f"""select a.id, a.nombre, a.apellido, a.mail, am.estado
                from alumnos a inner join alumnos_materias am on a.id = am.id_alumno
                where am.id_materia = {self.obtenerIdMateria()}"""
        try:
            

            datos = ConectorBD.run_query(query=query)            

            lista = []
            
            for dato in datos:
                if dato[4] != "Aprobada":
                    lista.append(f"{ayuda.formatoConCeros(str(dato[0]),5)} {dato[1]}{ayuda.crearEspacios(20-len(dato[1]))} {dato[2]}{ayuda.crearEspacios(20-len(dato[2]))} {dato[3]}")
            
            
                
           
            self.listboxAlumnos.delete(0,tk.END)

            self.listboxAlumnos.insert(0,*lista)
            
            
        except Exception as e:           
            print( type(e).__name__)
            print(e)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
        
    def cargaNotas(self,eveneto=None):  
        ventanaNotas = ayuda.VentanaDeNotas(padre=self,idMateria=self.obtenerIdMateria(), idAlumno= int(self.listboxAlumnos.get(self.listboxAlumnos.curselection())[:6]))
        ventanaNotas.grab_set()
        ventanaNotas.focus()
        ventanaNotas.entryNota.focus()
    
    def volverInicio(self, event=None):
         self.destroy()
         self.padre.deiconify()
    
    def cerrar_app(self):
        self.padre.destroy()
    
    def cambiarContra(self,evento=None):
        ventanaContra = ayuda.VentanaDeCambioDeContra(id=self.id, tabla="docentes")
        ventanaContra.grab_set()
        ventanaContra.focus()
        ventanaContra.entrycontra.focus()
        

# root = VentanaDeNotas(ingresante="ad", padre=None, id=2)
# root.mainloop()