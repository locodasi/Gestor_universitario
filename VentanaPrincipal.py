import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as MessageBox


import MiExcepcion
import ConectorBD
import Ayudadores as ayuda
import Ventanas_de_admin.VentanaDeCargaDeMaterias as ventanaMaterias      
import VentanasDeAlumnos.VentanaDeMaterias as ventanaAlumno  
import VentanasDeDocentes.VentanaDeNotas as ventanaDocente

class VentanaPrincipal(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(ayuda.localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),800,450))
        self.title("Inicio")
        self.config(bg=ayuda.color)
        self.resizable(0,0)
        
        self.crearElementosDePagina()
        
        self.legajo.focus()
    
    def crearElementosDePagina(self):
        
        #Creo la variable y la seteo
        self.seleccion=tk.IntVar()
        self.seleccion.set(1)
        #Creo los radio y les doy un valor y una variable sobra la que se van a guiar
        self.radio1=tk.Radiobutton(self,text="Alumno", variable=self.seleccion, value=1, background=ayuda.color)
        self.radio1.place(x=320,y=40)
        self.radio2=tk.Radiobutton(self,text="Docente", variable=self.seleccion, value=2, background=ayuda.color)
        self.radio2.place(x=410,y=40)
        
        labelLegajo = ttk.Label(self, text="Legajo:", background=ayuda.color)
        labelLegajo.place(x=315,y=80)
        self.legajo = ttk.Entry(self,width=30,validate="key",validatecommand= (self.register(ayuda.entradaConLimite), "%P", 30))
        self.legajo.place(x=315, y= 100)
        self.legajo.bind("<Return>", lambda x: self.contra.focus())
        
        labelContra= ttk.Label(self, text="Contra:", background=ayuda.color)
        labelContra.place(x=315,y=180)
        self.contra = ttk.Entry(self,show="*",width=30,validate="key",validatecommand= (self.register(ayuda.entradaConLimite), "%P", 30))
        self.contra.place(x=315, y= 200)
        self.contra.bind("<Return>", lambda x: self.ingresar())
        
        self.boton_abrir = ttk.Button(
            self,
            text="Entrar",
            command=self.ingresar
        )
        self.boton_abrir.place(x=370, y=300)
        
        
    def ingresar(self):
        
        try:
            if self.seleccion.get()==1:
                
                query = f"select * from alumnos where id = {self.legajo.get()} and contra = '{self.contra.get()}'"
                datos = ConectorBD.run_query(query=query)
                
                if len(datos) == 0:
                    raise MiExcepcion.MiExcepcion("Datos incorrectos")
                    
                if len(datos) == 1:
                                       
                    self.ventanaAlumno = ventanaAlumno.VentanaDeMaterias(padre=self,ingresante=f"{datos[0][2]},{datos[0][1]} Legajo: {datos[0][0]}", id=datos[0][0])
                    self.limpiar()
                    self.withdraw()
                    
                
            if self.seleccion.get()==2:
                
                query = f"select * from docentes where id = {self.legajo.get()} and contra = '{self.contra.get()}'"
                datos = ConectorBD.run_query(query=query)

                if len(datos) == 0:
                    raise MiExcepcion.MiExcepcion("Datos incorrectos")
                    
                if len(datos) == 1:
                    
                    if datos[0][0] == 1:
                        self.ventanaAdmin = ventanaMaterias.VentanaDeAltasDeMaterias(padre=self,ingresante=datos[0][1])
                        self.limpiar()
                        self.withdraw()

                    else:
                        self.ventanaDocente = ventanaDocente.VentanaDeNotas(padre=self,ingresante=f"{datos[0][2]},{datos[0][1]} ID: {datos[0][0]}",id=datos[0][0])
                        self.limpiar()
                        self.withdraw()

                
        except MiExcepcion.MiExcepcion as e:
            MessageBox.showwarning("Alerta", 
                f"{e}")
            
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")

    def limpiar(self):
        self.legajo.delete(0,tk.END)
        self.contra.delete(0,tk.END)
        self.seleccion.set(1)

root = VentanaPrincipal()
root.mainloop()