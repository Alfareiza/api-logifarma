from pydantic import BaseModel, EmailStr, NaiveDatetime, PastDate, AwareDatetime, PastDatetime


class InventarioSchema(BaseModel):
    # created_at: PastDate
    centro: str
    cod_mol: str
    cod_barra: str
    cum: str | None
    descripcion: str
    lote: str
    fecha_vencimiento: NaiveDatetime
    inventario: int
    costo_promedio: int
    cantidad_empaque: int


class InventarioSchemaList(BaseModel):
    result: list[InventarioSchema]


class SearchCriteria(BaseModel):
    ubi_dane: str
    cod_mol: str
