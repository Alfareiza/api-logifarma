from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.models import Inventario, Municipio, Centros
from app.schemas import InventarioSchemaList, InventarioSchema, SearchCriteria

app = FastAPI()


@app.get('/inventario/', response_model=InventarioSchemaList)
def list_inventario(session: Session = Depends(get_session)):
    database = session.scalars(select(Inventario)).all()
    return {'result': database}


@app.post('/inventario/', response_model=dict)
def search_inventario(criteria: SearchCriteria, session: Session = Depends(get_session)):
    params = criteria.__dict__

    # Agregar validaciones para que solo se permitan esos dos valores
    dane = params.get('ubi_dane')
    cod_molecula = params.get('cod_mol')

    # Busca el municipio con base en el codigo dane
    municipio = session.query(Municipio).filter_by(cod_dane=dane).first()

    # Busca los centros del municipio encontrado
    centros = session.query(Centros).filter_by(municipio_id=municipio.id).all()

    inventario_filtered = session.query(Inventario).filter(
        Inventario.centro.in_([centro.disp for centro in centros]),
        Inventario.cod_mol == cod_molecula
    ).all()

    return {
        "Cod_Molecula": cod_molecula,
        "CUM": inventario_filtered[0].cum,
        "Ubi_dane": dane,
        "Cantidad": sum(item.inventario for item in inventario_filtered)
    }
