from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    ...


class Municipio(Base):
    __tablename__ = "base_municipio"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    departamento = Column(String(128))
    activo = Column(Boolean(128))
    cod_dane = Column(Integer)


class Inventario(Base):
    __tablename__ = "base_inventario"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime())
    centro = Column(String(24))
    cod_mol = Column(String(24))
    cod_barra = Column(String(128))
    cum = Column(String(), nullable=True)
    descripcion = Column(String(250))
    lote = Column(String(24))
    fecha_vencimiento = Column(Date())
    inventario = Column(Integer)
    costo_promedio = Column(Integer)
    cantidad_empaque = Column(Integer)


class Centros(Base):
    __tablename__ = "base_centros"

    id = Column(Integer, primary_key=True, index=True)
    disp = Column(String())
    bod = Column(String())
    drogueria = Column(String())
    correo_coordinador = Column(String())
    dia_ped = Column(String())
    estado = Column(String())
    modalidad = Column(String())
    poblacion = Column(Integer())
    municipio_id = Column(Integer())
    tipo = Column(String())
    correo_disp = Column(String())
    responsable = Column(String())
    cedula = Column(String())
    celular = Column(String())
    direccion = Column(String())
    medicar = Column(String())
    tent = Column(Integer())
    analista = Column(String())
    ult_fecha_disp = DateTime()
    aux_pqr = Column(String())
    transp_1 = Column(String())
    transp_2 = Column(String())
    correo_contacto_eps = Column(String())
