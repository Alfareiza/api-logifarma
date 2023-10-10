from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.models import Inventario, Municipio, Centros
from app.schemas import SearchCriteria
from app.settings import settings
from app.utils import filter_inventario_by_cum, notify_email

router = APIRouter()


# @router.get('/', response_model=InventarioSchemaList)
# def list_inventario(session: Session = Depends(get_session)):
#     database = session.scalars(select(Inventario)).all()
#     return {'result': database}


@router.post('/reporte/ubiDaneCodMol', response_model=dict, status_code=200,
             summary="Inventario total de un código de molecula filtrado por código dane.")
def search_inventario(criteria: SearchCriteria, session: Session = Depends(get_session)):
    try:
        input_params = criteria.__dict__
        id_session = id(session)
        settings.LOG.info(f"{id_session=}, {input_params=}")

        dane = input_params.get('ubi_dane')
        cod_molecula = input_params.get('cod_mol')

        # Busca el municipio con base en el codigo dane
        municipio = session.query(Municipio).filter_by(cod_dane=dane).first()

        if not municipio:
            msg = f"No ha ido encontrado municipio con código dane {dane!r}."
            settings.LOG.info(f"{id_session=}, {msg}")
            return JSONResponse(status_code=404, content={"error": msg})

        # Busca los centros del municipio encontrado
        centros = session.query(Centros).filter_by(municipio_id=municipio.id).all()

        if not centros:
            msg = f"No han sido encontrados centros en {municipio.name.title()}."
            settings.LOG.info(f"{id_session=}, {msg}")
            return JSONResponse(status_code=404, content={"error": msg})

        result = session.query(Inventario).filter(
            Inventario.cod_mol == cod_molecula,
            Inventario.centro.in_([centro.disp for centro in centros])
        ).all()

        if not result:
            msg = f"No hay inventario para el código de molécula {cod_molecula!r}."
            settings.LOG.info(f"{id_session=}, {msg}")
            return JSONResponse(status_code=404, content={"error": msg})

        resp = {
            "cod_mol": cod_molecula,
            "ubi_dane": dane,
            "articulos": [art for art in filter_inventario_by_cum(result).values()],
            "cantidadTotal": sum(item.inventario for item in result)
        }

        settings.LOG.info(f"{id_session=}, {resp=}")

        return resp
    except Exception as e:
        notify_email(f"Error={e}\nParams={input_params}")
