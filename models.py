from sqlalchemy import Integer, Column, String
import db

class Producto(db.Base):
    __tablename__ = "producto"
    #__table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True) # Automaticamente sabe que es incremental
    nombre = Column(String, nullable=False, default="Desconocido")
    precio = Column(Integer, nullable=False, default=0)
    categoria = Column(String, nullable=False, default="Desconocido")
    stock = Column(Integer, nullable=False, default=0)



    def __init__(self,nombre,precio,categoria,stock):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock

    def __str__(self):
        return f"Producto: ({self.nombre},{self.precio},{self.categoria},{self.stock})"