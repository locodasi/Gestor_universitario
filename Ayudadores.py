import MiExcepcion
import tkinter.font as tkFont
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as MessageBox

#Para tener entry multilinea
from tkinter import scrolledtext as st

import ConectorBD

#Librerias para envio de mail
from email.message import EmailMessage
import smtplib

#Fechas
import datetime




color = '#49A'

class VentanaDeCambioDeContra(tk.Toplevel):
    
    def __init__(self,id, tabla, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.id = id
        self.tabla = tabla
        
        self.config(bg=color)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.geometry(localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),450,150))
        self.title("Cambio de contraseña")
        self.label = ttk.Label(self, text=f"Cambio de contraseña", font= tkFont.Font(family="Arial", size=16), foreground="green", background=color)
        self.label.place(x=0,y=0)
        self.resizable(0,0)
        
        self.focus()
        self.crearElementodDePagina()
        self.entrycontra.focus()
    
    def crearElementodDePagina(self):
        
        self.labelAntigua = ttk.Label(self,text="Antigua contraseña:",background=color)
        self.labelAntigua.place(x=30, y= 50)
        
        self.entrycontra = ttk.Entry(self,width=30,show="*")
        self.entrycontra.bind("<Return>", lambda x : self.validar())
        self.entrycontra.place(x=150,y=50)
        
        #Creo los widget para la modificacion de contraseña pero no pongo los places para no mostrarlos
        self.contraNueva = ttk.Entry(self,width=30,show="*")
        self.contraNueva.bind("<Return>", lambda x : self.confirmarContra.focus())
        
        #Excepto aca que solo le saco el texto paa que no se vea
        self.labelConfirmarContra = ttk.Label(self,text="",background=color)
        self.labelConfirmarContra.place(x=30,y=85)

        self.confirmarContra = ttk.Entry(self,width=30,show="*")
        self.confirmarContra.bind("<Return>", lambda x : self.ingresar())
        
   
        self.botonValidar = ttk.Button(self,text="Valida", command=self.validar)
        self.botonValidar.place(x=341,y=48)
        
        self.botonModificar = ttk.Button(self,text="Modificar", command=self.ingresar)
        
        
       
        
    def ingresar(self):
        try:
            
            self.validarTexto(self.contraNueva.get())
            self.validarTexto(self.confirmarContra.get())
            
            if self.confirmarContra.get() != self.contraNueva.get():
                raise MiExcepcion.MiExcepcion("Contraseña diferentes")
            
            else:
                
                query = f"update {self.tabla} set contra = '{self.contraNueva.get()}' where id = {self.id}"
                
                ConectorBD.run_query(query=query)

                self.original()
            
        except MiExcepcion.MiExcepcion as e:
                MessageBox.showwarning("Alerta", 
                    f"{e}")
            
        except Exception as e:
            print(type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
    
    def validar(self):
        
        try:
            
            self.validarTexto(self.entrycontra.get())
            
            query = f"select * from {self.tabla} where id = {self.id} and contra = '{self.entrycontra.get()}'"
            
            dato = ConectorBD.run_query(query=query)
            
            if len(dato) == 0:
                raise MiExcepcion.MiExcepcion("Contraseña invalida")
            else:
                self.nuevaContra()
            
        except MiExcepcion.MiExcepcion as e:
                MessageBox.showwarning("Alerta", 
                    f"{e}")
            
        except Exception as e:
            print(type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
    
    def nuevaContra(self):
        self.labelAntigua['text'] = "Nueva contraseña:"
        
        self.contraNueva.place(x=150,y=50)
        
        self.labelConfirmarContra['text'] = "Confirmar Contra:"
        
        
        self.confirmarContra.place(x=150,y=85)
        
        self.botonModificar.place(x=341,y=67)
        
        self.entrycontra.place_forget()
        self.entrycontra.delete(0,tk.END)
        self.botonValidar.place_forget()
        
        self.contraNueva.focus()
    
    def original(self):
        
        self.labelAntigua['text'] = "Antigua contraseña:"
        self.labelConfirmarContra['text'] = ""
        
        self.contraNueva.delete(0,tk.END)
        self.confirmarContra.delete(0,tk.END)
        
        self.entrycontra.place(x=150,y=50)
        self.entrycontra.focus()
        self.botonValidar.place(x=341,y=48)
        
        self.contraNueva.place_forget()
        self.botonModificar.place_forget()
        self.confirmarContra.place_forget()
        
        
        
        
        
    def validarTexto(self,texto):
        
        validar_string(texto)
        
        if texto == "" or len(texto.replace(" ","")) == 0:
            raise MiExcepcion.MiExcepcion("Contraseña invalida")
    
    def cerrar_app(self):
        self.destroy()
    


class VentanaCorrelativas(tk.Toplevel):
    
    def __init__(self,idCarrera,idMateria, materia, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.idCarrera = idCarrera
        self.idMateria = idMateria
        
        self.config(bg=color)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.geometry(localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),400,350))
        self.title(f"Carga de correlativas de la materia {materia}")
        
        self.resizable(0,0)
        
        self.focus()
        self.crearElementoDePagina()
    
    def crearElementoDePagina(self):

        self.Busqueda = ttk.Entry(self,width=50) 
        self.Busqueda.place(x=20,y=30)
        
        #KeyRelease es luego de levantar la tecla
        self.Busqueda.bind("<KeyRelease>", self.buscar)
        
        
        labelListbox = ttk.Label(self, text=f"ID    Materia{crearEspacios(23)} Correlativa",font= tkFont.Font(family="Courier", size=9), background=color)
        labelListbox.place(x=20,y=50)      
        self.listbox = tk.Listbox(self,height=15, width=50, font= tkFont.Font(family="Courier", size=9),activestyle=tk.NONE)
        self.listbox.place(x=20,y=70)
        #'<Double-1>' es el evento doble click
        self.listbox.bind('<Double-1>', self.cambiarCorre)
        self.obtenerMaterias()
    
    def cambiarCorre(self,evento=None):
        
        if self.listbox.get(self.listbox.curselection())[-1] == "C":
            idCorre =self.listbox.get(self.listbox.curselection())
            idCorre = idCorre.split(" ")[0]
            idCorre = int(idCorre)
            query = f"""delete from correlativas
                    where id_materia = {self.idMateria} and id_correlativa = {idCorre}"""
                    
            try:
                ConectorBD.run_query(query=query)
                self.obtenerMaterias()
            except Exception as e:           
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
        
        else:
            idCorre =self.listbox.get(self.listbox.curselection())
            idCorre = idCorre.split(" ")[0]
            idCorre = int(idCorre)
            query = f"""insert into correlativas (id_materia,id_correlativa) values ({self.idMateria}, {idCorre})"""
                    
            try:
                ConectorBD.run_query(query=query)
                self.obtenerMaterias()
            except Exception as e:           
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
    
    def buscar(self, evento):
        
        if self.Busqueda.get() != "":
                
            query = f"""select m.id, m.nombre, 'C'
                from materias m inner join carreras c on c.id = m.id_carrera 
                where m.id != {self.idMateria} and c.id = {self.idCarrera} and m.id = any(
	                select co.id_correlativa
                    from correlativas co
                    where co.id_materia = {self.idMateria}
                )
                order by m.id"""
                    
            try:
                datos = ConectorBD.run_query(query=query)
            except Exception as e:           
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
            
            lista = []
            
            for dato in datos:
                consulta = f"{formatoConCeros(str(dato[0]),5)} {dato[1]}{crearEspacios(30-len(dato[1]))} C"
                consulta = consulta.upper()
                
                if consulta.find(self.Busqueda.get().upper()) != -1:
                    lista.append(f"{formatoConCeros(str(dato[0]),5)} {dato[1]}{crearEspacios(30-len(dato[1]))} C")
            
            query = f"""select m.id, m.nombre
                from materias m inner join carreras c on c.id = m.id_carrera 
                where m.id != {self.idMateria} and c.id = {self.idCarrera} and m.id != all(
	                select co.id_correlativa
                    from correlativas co
                    where co.id_materia = {self.idMateria}
                )
                order by m.id"""     
            
            datos = ConectorBD.run_query(query=query)
            
            for dato in datos:
                consulta = f"{formatoConCeros(str(dato[0]),5)} {dato[1]}{crearEspacios(30-len(dato[1]))}  "
                consulta = consulta.upper()
                
                if consulta.find(self.Busqueda.get().upper()) != -1:
                    lista.append(f"{formatoConCeros(str(dato[0]),5)} {dato[1]}{crearEspacios(30-len(dato[1]))}  ")
            
            
            
            self.listbox.delete(0,tk.END)
            self.listbox.insert(0,*lista)
        else:
            self.obtenerMaterias()    
    
    def obtenerMaterias(self):
        self.listbox.delete(0,tk.END)
        
        #Con esta consulta obtengo las que tienen correlativas
        query = f"""select m.id, m.nombre, 'C'
                from materias m inner join carreras c on c.id = m.id_carrera 
                where m.id != {self.idMateria} and c.id = {self.idCarrera} and m.id = any(
	                select co.id_correlativa
                    from correlativas co
                    where co.id_materia = {self.idMateria}
                )
                order by m.id"""
                
        try:
            datos = ConectorBD.run_query(query=query)
            
            lista = []
        
            for dato in datos:

                lista.append(f"{formatoConCeros(str(dato[0]),5)} {dato[1]}{crearEspacios(30-len(dato[1]))} C")
            
            #Con esta obtengo las que no son correlativas
            query = f"""select m.id, m.nombre
                from materias m inner join carreras c on c.id = m.id_carrera 
                where m.id != {self.idMateria} and c.id = {self.idCarrera} and m.id != all(
	                select co.id_correlativa
                    from correlativas co
                    where co.id_materia = {self.idMateria}
                )
                order by m.id"""     
            
            datos = ConectorBD.run_query(query=query)
        
            for dato in datos:

                lista.append(f"{formatoConCeros(str(dato[0]),5)} {dato[1]}{crearEspacios(30-len(dato[1]))}  ")
                   
            
            self.listbox.insert(0,*lista)
        
        except Exception as e:           
            print( type(e).__name__)
            print(e)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
        
    
    def cerrar_app(self):
        self.destroy()

class VentanaVerMaterias(tk.Toplevel):
    def __init__(self, carrera, idCarrera, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.idCarrera = idCarrera
        self.config(bg=color)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.geometry(localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),550,350))
        self.title(f"Materias de la carrera {carrera}")
        
        self.resizable(0,0)
        
        self.focus()
        self.crearElementoDePagina()
        self.obtenerMaterias()
    
    def crearElementoDePagina(self):
        
        self.busqueda = ttk.Entry(self,width=45)
        self.busqueda.place(x=20,y=30)
        self.busqueda.bind("<KeyRelease>", self.buscar)

        label = ttk.Label(self, text=f"ID    Materia{crearEspacios(23)} Correlativas" ,background=color,font= tkFont.Font(family="Courier", size=9))
        label.place(x=20,y=50)   
        
        self.listbox = tk.Listbox(self,width=70,height=15, font= tkFont.Font(family="Courier", size=9),activestyle=tk.NONE)
        self.listbox.place(x=20,y=70)
    
    def buscar(self, evento):
        
        if self.busqueda.get() != "":
                
            query = f"select m.id, m.nombre from materias m inner join carreras c on m.id_carrera = c.id where c.id = {self.idCarrera}"
        
            lista = [] 
                    
            try:
                materias = ConectorBD.run_query(query=query)
            
                for materia in materias:
                    #Obtengo sus correlativas
                    query = f"select id_correlativa from correlativas where id_materia = {materia[0]}"
                    correlativas = ConectorBD.run_query(query=query)
                    
                    #Hago que queden mas lindas a la vista
                    
                    corre = "("
                    if len(correlativas) == 0:
                        consulta = f"{formatoConCeros(str(materia[0]),5)} {materia[1]}{crearEspacios(30-len(materia[1]))} "
                        consulta = consulta.upper()
                        
                        if consulta.find(self.busqueda.get().upper()) != -1:
                            lista.append(f"{formatoConCeros(str(materia[0]),5)} {materia[1]}{crearEspacios(30-len(materia[1]))} ")
                    else:
                        for co in correlativas:
                            cor = str(co[0])
                            corre += f"{cor},"
                    
                        corre = corre[:-1]
                        corre += ")"
                        
                        consulta = f"{formatoConCeros(str(materia[0]),5)} {materia[1]}{crearEspacios(30-len(materia[1]))} {corre}"
                        consulta = consulta.upper()
                        
                        if consulta.find(self.busqueda.get().upper()) != -1:
                            lista.append(f"{formatoConCeros(str(materia[0]),5)} {materia[1]}{crearEspacios(30-len(materia[1]))} {corre}")
                
                self.listbox.delete(0,tk.END)
                self.listbox.insert(0,*lista)   
                        
                        
            except Exception as e:           
                print( type(e).__name__)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query")
        else:
            self.obtenerMaterias() 
    
    def obtenerMaterias(self):
        
        query = f"select m.id, m.nombre from materias m inner join carreras c on m.id_carrera = c.id where c.id = {self.idCarrera}"
        
        lista = [] 
        try:
            
            #Obtnego las materias
            materias = ConectorBD.run_query(query=query)
            
            for materia in materias:
                #Obtengo sus correlativas
                query = f"select id_correlativa from correlativas where id_materia = {materia[0]}"
                correlativas = ConectorBD.run_query(query=query)
                
                #Hago que queden mas lindas a la vista
                
                corre = "("
                if len(correlativas) == 0:
                    lista.append(f"{formatoConCeros(str(materia[0]),5)} {materia[1]}{crearEspacios(30-len(materia[1]))} ")
                else:
                    for co in correlativas:
                        cor = str(co[0])
                        corre += f"{cor},"

                    corre = corre[:-1]
                    corre += ")"
                    lista.append(f"{formatoConCeros(str(materia[0]),5)} {materia[1]}{crearEspacios(30-len(materia[1]))} {corre}")
            
            self.listbox.delete(0,tk.END)
            self.listbox.insert(0,*lista)
            
        except Exception as e:
            print(type(e).__name__)
            print(e)
            MessageBox.showwarning("Alerta", "Error al ejecutar la query")
        
    def cerrar_app(self):
        self.destroy()
        
        

class VentanaVerNotas(tk.Toplevel):
    
    def __init__(self,titulo,lista, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.titulo = titulo
        self.lista = lista
        
        self.config(bg=color)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.geometry(localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),850,400))
        self.title(self.titulo)
        
        self.resizable(0,0)
        
        self.focus()
        self.crearElementoDePagina()
        
    
    def crearElementoDePagina(self):

        labelObs = ttk.Label(self, text="Observaciones" ,background=color)
        labelObs.place(x=20,y=20)   
        self.entryObser=st.ScrolledText(self, width=63, height=6)
        self.entryObser.place(x=20,y=50)
        
        labelListbox = ttk.Label(self, text=f"ID    Fecha      Nota    Tipo                 Observacion",font= tkFont.Font(family="Courier", size=11), background=color)
        labelListbox.place(x=20,y=180)      
        self.listbox = tk.Listbox(self,width=90, font= tkFont.Font(family="Courier", size=11),activestyle=tk.NONE)
        self.listbox.place(x=20,y=200)
        self.listbox.bind("<Double-1>", self.traerObs)
        self.listbox.insert(0,*self.lista)
        
    def traerObs(self,evento=None):
        
        dato = self.listbox.get(self.listbox.curselection())
        id = int(dato.split(" ")[0])
        
        query = f"select observacion from notas where id = {id}"
        
        try:
            
            obs = ConectorBD.run_query(query=query)[0][0]
            
            self.entryObser.delete("1.0", tk.END)
            self.entryObser.insert("1.0",obs)
        
        except Exception as e:
                print(type(e).__name__)
                print(e)
                MessageBox.showwarning("Alerta", 
                    "Error al ejecutar la query") 
    
    def cerrar_app(self):
        self.destroy()



class VentanaDeNotas(tk.Toplevel):
    
    def __init__(self,padre,idMateria, idAlumno, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.idMateria = idMateria
        self.idAlumno = idAlumno
        self.padre = padre
        
        self.config(bg=color)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.geometry(localizarMitadPantalla(self.winfo_screenwidth(),self.winfo_screenheight(),800,450))
        self.title("Carga de notas")
        self.label = ttk.Label(self, text=f"Carga de notas", font= tkFont.Font(family="Arial", size=16), foreground="green", background=color)
        self.label.place(x=0,y=0)
        self.resizable(0,0)
        
        self.focus()
        self.crearElementodDePagina()
        self.obtenerNotas()
        self.nuevo()
        self.validarAprobar()
        self.entryNota.focus()
    
    def validarAprobar(self):
        
        if self.listNotas.size() == 0:
            self.botonAprobar['state'] = tk.DISABLED
        else:
            self.botonAprobar['state'] = tk.NORMAL
    
    def crearElementodDePagina(self):
        
        labelNota = ttk.Label(self,text="Nota:",background=color)
        labelNota.place(x=30, y= 50)
        
        self.entryNota = ttk.Entry(self,width=3,validate="key", validatecommand=(self.register(entradaConNumerosYLimite), "%S", "%P", 2))
        self.entryNota.bind("<Return>", lambda x : self.entryObser.focus())
        self.entryNota.place(x=30,y=70)
        
        labelTipo = ttk.Label(self,text="Tipo:",background=color)
        labelTipo.place(x=70,y=50)
        
        self.comboTipo = ttk.Combobox(self,values=["TP","Parcial","Final","Tesis","Presentacion","Proyecto"], state="readonly",width=15)
        self.comboTipo.place(x=70,y=70)
        self.comboTipo.current(0)
        
        labelObs = ttk.Label(self,text="Observaciones:",background=color)
        labelObs.place(x=210, y= 50)
        self.entryObser=st.ScrolledText(self, width=61, height=6)
        self.entryObser.place(x=210,y=70)
        
        
        self.botonIngresar = ttk.Button(self,text="Ingresar", command=self.ingresar)
        self.botonIngresar.place(x=720,y=70)
        self.botonLimpiar = ttk.Button(self,text="Limpiar", command=self.limpiar)
        self.botonLimpiar.place(x=720,y=95)
        self.botonModificar = ttk.Button(self,text="Modificar", command=self.modificar)
        self.botonModificar.place(x=720,y=120)
        self.botonEliminar = ttk.Button(self,text="Eliminar", command=self.eliminar)
        self.botonEliminar.place(x=720,y=145)
        
        self.botonAprobar = ttk.Button(self,text="Aprobar", command=self.aprobar)
        self.botonAprobar.place(x=350,y=180)
        
        labelLista = ttk.Label(self,text=f"ID    Fecha      Nota    Tipo{crearEspacios(16)} Observacion",background=color, font= tkFont.Font(family="Courier", size=9))
        labelLista.place(x=30,y=240)
        
        self.listNotas = tk.Listbox(self,font= tkFont.Font(family="Courier", size=9),width=80,activestyle=tk.NONE)
        self.listNotas.place(x=30,y=260)
        self.listNotas.bind("<Double-1>", self.recuperar)
    
    def recuperar(self,evento=None):
        dato : str = self.listNotas.get(self.listNotas.curselection())
        id = int(dato.split(" ")[0])
        
        query = f"""select id, nota, tipo, observacion
                    from notas
                    where id = {id}"""
                    
        try:
            datos = ConectorBD.run_query(query=query)[0]
            
        except Exception as e:           
            print( type(e).__name__)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
        self.limpiar()
        
        self.id= datos[0]
        self.entryNota.insert(0,datos[1])
        self.entryObser.insert("1.0",datos[3])
        self.comboTipo.set(datos[2])
        self.viejo()
        self.entryNota.focus()
        
    def ingresar(self):
        
        #"1.0" indica primera fila columna 0, si quisiera que imprima hasta tercera fila columna 2 hagi
        # "1.0","3.2", es de esta forma tanto insert como delete
        obs = self.entryObser.get("1.0",tk.END)
        query = f"insert into notas (id_alumno, id_materia, nota, tipo, observacion, dia) values ({self.idAlumno},{self.idMateria},{self.entryNota.get()},'{self.comboTipo.get()}','{obs}','{datetime.date.today()}')"
        
        try:
            self.validar()
            ConectorBD.run_query(query=query)
            self.limpiar()
            self.obtenerNotas()
            self.botonAprobar['state'] = tk.NORMAL
            
        except MiExcepcion.MiExcepcion as e:
            MessageBox.showwarning("Alerta", 
                f"{e}")
            
            self.entryNota.focus()
            
        except Exception as e:
            print(type(e).__name__)
            print(e)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
    
    def validar(self):
        
        if self.entryNota.get() == "":
            raise MiExcepcion.MiExcepcion("Falta la nota")
        
        if int(self.entryNota.get()) > 10:
            raise MiExcepcion.MiExcepcion("Nota no puede ser mayor a 10")
        
        

        validar_string(self.entryObser.get("1.0",tk.END))
    
    def obtenerNotas(self):
        
        query = f"""select n.dia, n.nota, n.tipo, n.observacion, n.id
                from notas n inner join alumnos a on n.id_alumno = a.id inner join materias m on n.id_materia = m.id
                where n.id_alumno = {self.idAlumno} and n.id_materia = {self.idMateria}"""
        
        try:
            
            datos = ConectorBD.run_query(query=query)
            
            lista = []
            
            for dato in datos:
                hasta = dato[3].find("\n")
                obs = dato[3][:hasta]
                lista.append(f"{formatoConCeros(str(dato[4]),5)} {dato[0]} {crearEspacios(2-len(str(dato[1])))}{dato[1]}      {dato[2]}{crearEspacios(20-len(dato[2]))} {obs[:15]}")

            self.listNotas.delete(0,tk.END)
            self.listNotas.insert(0,*lista)
            
        except Exception as e:
            print(type(e).__name__)
            print(e)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
    
    def eliminar(self):
        query = f"delete from notas where id = {self.id}"
        
        try:
            ConectorBD.run_query(query=query)            
            self.obtenerNotas()
            self.validarAprobar()
            self.limpiar()
        except Exception as e:
            print(type(e).__name__)
            print(e)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
    
    def modificar(self):
        obs = self.entryObser.get("1.0", tk.END)
        query = f"update notas set nota = {self.entryNota.get()}, tipo = '{self.comboTipo.get()}', observacion = '{obs}' where id = {self.id}"
        
        try:
            self.validar()
            ConectorBD.run_query(query=query)            
            self.obtenerNotas()
            self.limpiar()
        except MiExcepcion.MiExcepcion as e:
            MessageBox.showwarning("Alerta", 
                f"{e}")
            
            self.entryNota.focus()
        except Exception as e:
            print(type(e).__name__)
            print(e)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
    def aprobar(self):
        #Tengo que agregar que elimine de la tabla alumno_materia el registro de este alumno con esta materia aprobada, (Ademas si se gradua, tengo que hacer lo mismo con alumno_carrera, eliminando al alumno de su carrera graduada y todas las alumno_materias de ese alumno en cualquier materia de esa carrea [Talvez crear tabla graduados, con alumno y carrera])
        query = f"update alumnos_materias set estado = 'Aprobada' where id_alumno = {self.idAlumno} and id_materia = {self.idMateria}"
        
        try:
            
            ConectorBD.run_query(query=query)
            self.padre.obtenerAlumnos()
            self.cerrar_app()
        except Exception as e:
            print(type(e).__name__)
            print(e)
            MessageBox.showwarning("Alerta", 
                "Error al ejecutar la query")
            
    def limpiar(self):
        self.entryNota.delete(0,tk.END)
        self.entryObser.delete("1.0",tk.END)
        self.nuevo()
        self.entryNota.focus()
    
    def nuevo(self):
        self.botonEliminar['state'] = tk.DISABLED
        self.botonModificar['state'] = tk.DISABLED
        self.botonIngresar['state'] = tk.NORMAL
    
    def viejo(self):
        self.botonEliminar['state'] = tk.NORMAL
        self.botonModificar['state'] = tk.NORMAL
        self.botonIngresar['state'] = tk.DISABLED
        
    def cerrar_app(self):
        self.destroy()

#Si permito los ' alguien podria ingresar ');drop table materias;-- lo que me borraria la tabla
#Al prohibir las ', evito que eso suceda
def validar_string(string):
    if string.find("'") != -1:
     raise MiExcepcion.MiExcepcion("Invalidas las '")
 
def ObtenerId(dato):
    id = str(dato[0])
    id = id.replace("(", "")
    id = id.replace(")", "")
    id = id.replace(",", "")
    return int(id)

def crearEspacios(cant):
    string = ""
   
    return string + " " * cant

def formatoConCeros(string,cantNumeros):
    cantNumeros -= len(string)
    
    return "0" * cantNumeros + string

def entradaConNumerosYLimite(text, new_text,cant=""):
    
    #Si no pasan cant, significa que es infinito
    if cant != "":
        # Primero chequear que el contenido total no exceda los caracteres.
        if len(new_text) > int(cant):
            return False
        
    # Luego, si la validación anterior no falló, chequear que el texto solo
    # contenga números.
    return text.isdecimal()

def entradaConLimite(new_text,cant):
    

    if len(new_text) > int(cant):
        return False
        
    return True

def numeroConComa(text, new_text,cantEntera="", cantDecimal=""):
    
    #Esto es para que cunado recupero un segundo dato, me permia borra la duracion y pueda ingresar la nueva
    if new_text == "" :
        return True
    #Con esto separo
    
    d = new_text.split(".")
    
    if len(d[0]) > int(cantEntera):
        return False

    
    if text ==".":

        #Si da dos partes significa que recien es el primero
        if len(d) <= 2:
            return True
        else:
            return False
    
    if new_text.endswith("."):
        return True
    #Esto es para cunado pego un dato de una o cunado hago recuperara en la listbox
    if len(d) == 2:
        if len(d[1]) > int(cantDecimal):
            return False
        else:
            return d[1].isdecimal() and d[0].isdecimal()
        
    return text.isdecimal()

def ventanaDeMostrar(titulo, lista):
    mostrar = tk.Toplevel()
    mostrar.geometry(localizarMitadPantalla(mostrar.winfo_screenwidth(),mostrar.winfo_screenheight(),850,250))
    mostrar.resizable(0,0)
    mostrar.title(titulo)
    mostrar.config(bg=color)
    labelListbox = ttk.Label(mostrar, text=f"ID    Nombre{crearEspacios(14)} Apellido{crearEspacios(12)} DNI         Email",font= tkFont.Font(family="Courier", size=11), background=color)
    labelListbox.place(x=20,y=20)      
    listbox = tk.Listbox(mostrar,width=90, font= tkFont.Font(family="Courier", size=11),activestyle=tk.NONE)
    listbox.place(x=20,y=40)
    listbox.insert(0,*lista)
    
    
    return mostrar

 

def enviarEmailDeIngreso(mail,materia,carrera,alumno):

    #Podes poner tanto homtial,como gmail, etc
    remitente = "TuMail@hotmail.com"
    destinatario = mail
    mensaje = ""
    if len(materia) == 1:
        mensaje = f"""Hola {alumno}, fuiste correctamente inscripto en la materia de {materia[0][6:]} de la carrera de {carrera}.
    
    
    ATT.
        La direccion"""
    
    else:
        mensaje = f"Hola {alumno}, fuiste correctamente inscripto a las materias de "
        
        for dato in materia:
            mensaje += f"{dato[6:]},"
        
        #Para borrar la ultima coma
        mensaje = mensaje[:len(mensaje)-1]
        
        mensaje += f""" de la carrera de {carrera}.
    
    
    ATT.
        La direccion"""
        
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Inscripcion a materia"
    email.set_content(mensaje)
            
    #Aca depende que servidor use el remitente del mail, gmail, hotmail,etc, este es para hotmail
    #lo mismo con el puerto, dependera que uses
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "TuContra")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()
    
def enviarEmailDeBaja(mail,materia,carrera,alumno):

    remitente = "Tumail@hotmial.com"
    destinatario = mail
    mensaje = ""
    
    if len(materia) == 1:
        mensaje = f"""Hola {alumno}, abandonaste correctamente la materia de {materia[0][6:]} de la carrera de {carrera}.
        
        
        ATT.
            La direccion"""
    
    else:
        mensaje = f"Hola {alumno}, abandonaste correctamente las materias de "
        
        for dato in materia:
            mensaje += f"{dato[6:]},"
        
        #Para borrar la ultima coma
        mensaje = mensaje[:len(mensaje)-1]
        
        mensaje += f""" de la carrera de {carrera}.
    
    
    ATT.
        La direccion"""
        
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Baja a materia"
    email.set_content(mensaje)
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "TuContra")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()
    
def localizarMitadPantalla(anchoPantalla, alturaPantalla, anchoVentana, altoVentana):
    x_ventana = anchoPantalla // 2 - anchoVentana // 2
    y_ventana = alturaPantalla // 2 - altoVentana // 2
    
    posicion = str(anchoVentana) + "x" + str(altoVentana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    
    return posicion

    


    