from tkinter import ttk
from tkinter import *
from models import Producto
import db
import ttkbootstrap as ttk # Libreria de booptstrap para dar colores a botones
from ttkbootstrap import Style # libreria para dar tema a la ventana

class ventanaPrincipal():

    def __init__(self, root):
        estilo = Style (theme="darkly") # tema
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1,1) # activa la redimencion de la ventana
        #self.ventana.call("wm", "iconphoto", root._w, PhotoImage(file="recursos/icon.png")) # otra forma
        #self.ventana.wm_iconbitmap("recursos/icon.png") # Para windows
        self.ventana.iconphoto(True, PhotoImage(file="recursos/icon.png")) # icono para linux

        # Creaciopn del contenedor principal (frame)
        frame = LabelFrame(self.ventana, text="                             Registrar un nuevo Producto                         ",
                           font=('Calibri', 14, 'bold'))
        frame.grid(row=0, column=0, pady=20, columnspan=6)

        # Label de Nombre
        self.etiquetaNombre = Label(frame, text="Nombre: ", font=('Calibri', 13))
        self.etiquetaNombre.grid(row=1, column=0)
        #Entry de Nombre
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.grid(row=1, column=1)
        self.nombre.focus()

        # Label de Categoria
        self.etiquetaCategoria = Label(frame, text="Categoria: ", font=('Calibri', 13))
        self.etiquetaCategoria.grid(row=1, column=3)
        # Entry de Categoria
        self.categoria = Entry(frame, font=('Calibri', 13))
        self.categoria.grid(row=1, column=4)

        # Label de Precio
        self.etiquetaPrecio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiquetaPrecio.grid(row=2, column=0)
        # Entry de Precio
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=2, column=1)

        # Label de Stock
        self.etiquetaStock = Label(frame, text="Stock: ", font=('Calibri', 13))
        self.etiquetaStock.grid(row=2, column=3)
        # Entry de Stock
        self.stock = Spinbox(frame,from_=0, to=100, font=('Calibri', 13))
        self.stock.grid(row=2, column=4)

        #Boton añadir Producto

        self.botonAnadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, bootstyle="success")
        self.botonAnadir.grid(row=3, columnspan=6, sticky=W+E)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=4, column=0, columnspan=2, sticky=W + E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=(2,3,4), style="mystyle.Treeview")
        self.tabla.grid(row=5, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 1
        self.tabla.heading('#2', text='Categoria', anchor=CENTER)  # Encabezado 2
        self.tabla.heading('#3', text='Stock', anchor=CENTER)  # Encabezado 3

        # Botones de Eliminar y Editar

        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, bootstyle="danger")
        self.boton_eliminar.grid(row=6, column=0, sticky=W + E)
        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, bootstyle="info")
        self.boton_editar.grid(row=6, column=1, sticky=W + E)
        self.getProductos()

    def getProductos(self):
        # Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla.get_children()  # Obtener todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)

        registros = db.session.query(Producto).all()
        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text=fila.nombre, values=(fila.precio,fila.categoria,fila.stock))

    def validacion_nombre(self):
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def add_producto(self):
        if not self.validacion_nombre():
            print("El nombre es obligatorio")
            self.mensaje['text'] = 'El nombre es obligatorio y no puede estar vacío'
            return
        if not self.validacion_precio():
            print("El precio es obligatorio")
            self.mensaje['text'] = 'El precio es obligatorio y debe ser un número válido mayor que 0'
            return

        producto = Producto(self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
        db.session.add(producto)
        db.session.commit()
        print("Datos guardados")
        self.mensaje['text'] = f'Producto {self.nombre.get()} añadido con éxito'
        self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
        self.precio.delete(0, END)  # Borrar el campo precio del formulario
        self.categoria.delete(0, END)  # Borrar el campo nombre del formulario
        self.stock.delete(0, END)  # Borrar el campo precio del formulario

        self.getProductos()  # Cuando se finalice la inserción de datos volvemos a invocar a este método para actualizar el contenido

    def del_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            mensaje = self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        print(nombre)
        respuesta = db.session.query(Producto).filter(Producto.nombre == nombre).first()
        db.session.delete(respuesta)
        db.session.commit()

        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.getProductos()  # Actualizar la tabla de productos

    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            categoria = self.tabla.item(self.tabla.selection())['values'][1]
            stock = self.tabla.item(self.tabla.selection())['values'][2]
            VentanaEditarProducto(self, nombre, precio, categoria, stock, self.mensaje)
        except IndexError:
            self.mensaje['text'] = 'Por favor, seleccione un producto'

class VentanaEditarProducto():

    def __init__(self, ventanaPrincipal, nombre, precio, categoria, stock, mensaje):
        self.ventanaPrincipal = ventanaPrincipal
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock
        self.mensaje = mensaje

        self.ventanaEditar = Toplevel()
        self.ventanaEditar.title("Editar Producto")

        # Creación del contenedor Frame para la edición del producto
        frame_ep = LabelFrame(self.ventanaEditar, text="                                   Editar el siguiente Producto                               ",
                              font=('Calibri', 16, 'bold'))
        frame_ep.grid(row=0, column=0, columnspan=6, pady=20, padx=20)

        # Label y Entry para el Nombre antiguo (solo lectura)
        Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13)).grid(row=1, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventanaEditar, value=nombre), state='readonly',
              font=('Calibri', 13)).grid(row=1, column=1)

        # Label y Entry para el Nombre nuevo
        Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13)).grid(row=2, column=0)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=2, column=1)
        self.input_nombre_nuevo.focus()

        # Label y Entry para el Categoria antigua (solo lectura)
        Label(frame_ep, text="Categoria antigua: ", font=('Calibri', 13)).grid(row=1, column=4)
        Entry(frame_ep, textvariable=StringVar(self.ventanaEditar, value=categoria), state='readonly',
              font=('Calibri', 13)).grid(row=1, column=5)

        # Label y Entry para el Categoria Nueva
        Label(frame_ep, text="Categoria nueva: ", font=('Calibri', 13)).grid(row=2, column=4)
        self.inputCategoriaNueva = Entry(frame_ep, font=('Calibri', 13))
        self.inputCategoriaNueva.grid(row=2, column=5)

        # Precio antiguo (solo lectura)
        Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13)).grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventanaEditar, value=precio), state='readonly',
              font=('Calibri', 13), fg="black").grid(row=3, column=1)

        # Precio nuevo
        Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13)).grid(row=4, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=4, column=1)

        # Stock antiguo (solo lectura)
        Label(frame_ep, text="Stock antiguo: ", font=('Calibri', 13)).grid(row=3, column=4)
        Entry(frame_ep, textvariable=StringVar(self.ventanaEditar, value=stock), state='readonly',
              font=('Calibri', 13), fg="black").grid(row=3, column=5)

        # Stock nuevo
        Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13)).grid(row=4, column=4)
        self.inputStockNuevo = Spinbox(frame_ep,from_=0, to=100, font=('Calibri', 13))
        self.inputStockNuevo.grid(row=4, column=5)

        # Botón Actualizar Producto

        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", command=self.actualizar, bootstyle="success")
        self.boton_actualizar.grid(row=5, columnspan=6, sticky=W + E)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio
        nuevaCategoria = self.inputCategoriaNueva.get() or self.categoria
        nuevoStock = self.inputStockNuevo.get() or self.stock

        if nuevo_nombre and nuevo_precio and nuevaCategoria and nuevoStock:
            respuesta = db.session.query(Producto).filter(Producto.nombre == self.nombre).first()
            respuesta.nombre = nuevo_nombre
            respuesta.precio = nuevo_precio
            respuesta.categoria = nuevaCategoria
            respuesta.stock = nuevoStock
            db.session.commit()

            self.mensaje['text'] = f'El producto {self.nombre} ha sido actualizado con éxito'
        else:
            self.mensaje['text'] = f'No se pudo actualizar el producto {self.nombre}'
        self.ventanaEditar.destroy()
        self.ventanaPrincipal.getProductos()


if __name__ == "__main__":
    root = Tk() # Instanccia de la ventana principal
    app = ventanaPrincipal(root) # enviamos y cedemos el control a la clase
    root.mainloop() # Loop para que mantenga la ventana abierta

