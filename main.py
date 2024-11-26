import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import os

def ejecutar_codigo():
    codigo = editor.get("1.0", tk.END)
    try:
        estado.config(text="Ejecutando...", fg="orange")
        ventana.update()

        resultado = subprocess.run(
            ['python', '-c', codigo], capture_output=True, text=True, timeout=5
        )
        
        if resultado.returncode == 0:
            salida.config(state=tk.NORMAL)
            salida.delete(1.0, tk.END)
            salida.insert(tk.END, resultado.stdout)
        else:
            salida.config(state=tk.NORMAL)
            salida.delete(1.0, tk.END)
            salida.insert(tk.END, resultado.stderr)
        
        estado.config(text="Listo", fg="green")
    except Exception as e:
        salida.config(state=tk.NORMAL)
        salida.delete(1.0, tk.END)
        salida.insert(tk.END, f"Error al ejecutar el código: {e}")
        estado.config(text="Error", fg="red")

def abrir_archivo():
    archivo = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("All files", "*.*")])
    if archivo:
        with open(archivo, "r") as f:
            codigo = f.read()
            editor.delete(1.0, tk.END)
            editor.insert(tk.END, codigo)
        ventana.title(f"PyLite - {os.path.basename(archivo)}")

def guardar_archivo():
    archivo = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("All files", "*.*")])
    if archivo:
        with open(archivo, "w") as f:
            f.write(editor.get("1.0", tk.END))
        ventana.title(f"PyLite - {os.path.basename(archivo)}")

def nuevo_archivo():
    editor.delete(1.0, tk.END)
    ventana.title("PyLite - Nuevo archivo")

def insertar_plantilla(plantilla):
    if plantilla == "funcion":
        codigo = '''def mi_funcion(parametro1, parametro2):
    return parametro1 + parametro2
'''
    elif plantilla == "clase":
        codigo = '''class MiClase:
    def __init__(self, atributo1, atributo2):
        self.atributo1 = atributo1
        self.atributo2 = atributo2
    
    def mi_metodo(self):
        return self.atributo1 + self.atributo2
'''
    elif plantilla == "bucle":
        codigo = '''for i in range(10):
    print(f"Iteración {i}")
'''
    elif plantilla == "excepcion":
        codigo = '''try:
    x = 10 / 0
except ZeroDivisionError as e:
    print("Error de división por cero:", e)
except Exception as e:
    print(f"Error inesperado: {e}")
'''
    elif plantilla == "api":
        codigo = '''import requests

url = "https://api.example.com/endpoint"
response = requests.get(url)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error al obtener datos: {response.status_code}")
'''
    elif plantilla == "sqlite":
        codigo = '''import sqlite3

conexion = sqlite3.connect("mi_base_de_datos.db")
cursor = conexion.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT)")

cursor.execute("INSERT INTO usuarios (nombre) VALUES ('Juan')")
conexion.commit()

cursor.execute("SELECT * FROM usuarios")
print(cursor.fetchall())

conexion.close()
'''
    elif plantilla == "herencia":
        codigo = '''class Animal:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def hablar(self):
        print(f"{self.nombre} hace un sonido")

class Perro(Animal):
    def hablar(self):
        print(f"{self.nombre} dice ¡Guau!")

mi_perro = Perro("Firulais")
mi_perro.hablar()
'''
    elif plantilla == "documentacion":
        codigo = '''def mi_funcion(parametro1, parametro2):
    return parametro1 + parametro2
'''
    else:
        codigo = "# Plantilla no encontrada."
    
    editor.insert(tk.END, codigo)

def buscar_reemplazar():
    busqueda = simpledialog.askstring("Buscar", "Texto a buscar:")
    if busqueda:
        inicio = editor.search(busqueda, "1.0", tk.END)
        if inicio:
            editor.tag_add("highlight", inicio, f"{inicio}+{len(busqueda)}c")
            editor.tag_configure("highlight", background="yellow", foreground="black")
        else:
            messagebox.showinfo("Resultado", "No se encontró el texto.")

def deshacer():
    editor.edit_undo()

def rehacer():
    editor.edit_redo()

def sincronizar_scroll():
    salida.yview_moveto(editor.yview()[0])

ventana = tk.Tk()
ventana.title("PyLite - Nuevo archivo")
ventana.geometry("900x650")
ventana.iconbitmap("icono.ico")

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_archivo = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Nuevo", command=nuevo_archivo, accelerator="Ctrl+N")
menu_archivo.add_command(label="Abrir", command=abrir_archivo, accelerator="Ctrl+O")
menu_archivo.add_command(label="Guardar", command=guardar_archivo, accelerator="Ctrl+S")

menu_edicion = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Edición", menu=menu_edicion)
menu_edicion.add_command(label="Deshacer", command=deshacer, accelerator="Ctrl+Z")
menu_edicion.add_command(label="Rehacer", command=rehacer, accelerator="Ctrl+Y")
menu_edicion.add_command(label="Buscar y Reemplazar", command=buscar_reemplazar, accelerator="Ctrl+F")

menu_plantillas = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Plantillas", menu=menu_plantillas)
menu_plantillas.add_command(label="Función Básica", command=lambda: insertar_plantilla("funcion"))
menu_plantillas.add_command(label="Clase Básica", command=lambda: insertar_plantilla("clase"))
menu_plantillas.add_command(label="Bucle For", command=lambda: insertar_plantilla("bucle"))
menu_plantillas.add_command(label="Manejo de Excepciones", command=lambda: insertar_plantilla("excepcion"))
menu_plantillas.add_command(label="Consumo de API", command=lambda: insertar_plantilla("api"))
menu_plantillas.add_command(label="Base de Datos SQLite", command=lambda: insertar_plantilla("sqlite"))
menu_plantillas.add_command(label="Herencia en Clases", command=lambda: insertar_plantilla("herencia"))
menu_plantillas.add_command(label="Documentación", command=lambda: insertar_plantilla("documentacion"))

frame = tk.Frame(ventana)
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

editor = tk.Text(frame, width=90, height=25, wrap=tk.WORD, font=("Courier New", 12), undo=True)
editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

boton_ejecutar = tk.Button(ventana, text="Ejecutar Código", command=ejecutar_codigo, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED, bd=3)
boton_ejecutar.pack(pady=5)

salida = tk.Text(ventana, width=90, height=10, wrap=tk.WORD, font=("Courier New", 12), bd=3, relief=tk.SUNKEN, padx=5, pady=5)
salida.pack(pady=10)
salida.config(state=tk.DISABLED)

estado = tk.Label(ventana, text="Listo", bd=1, relief=tk.SUNKEN, anchor="w", font=("Arial", 10))
estado.pack(side=tk.BOTTOM, fill=tk.X)

ventana.mainloop()
