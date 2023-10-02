import logging
from pathlib import Path
from typing import List, Dict, Any

import emails
from emails.template import JinjaTemplate

from app.models import Inventario
from app.settings import settings


def filter_inventario_by_cum(articulos: List[Inventario]) -> dict:
    """
    A partir de una lista de Inventario, crea un diccionário donde
    la llave es el CUM y su value es un dicionario con el cum, descripcion
    cantidad, y fracción. Luego, la cantidad es sumada con los articulos
    que tengan el mismo cum.
    Obs.: Puede llegar a suceder que entre un articulo y otro tengan
          diferente fraccion y descripcion. Esto no es validado.
    :return: Ej.:
            {
             "19934333-3": {
                                "cum": "19934333-3",
                                "descripcion": "articulo xyz",
                                "cantidad": 2740,
                                "fraccion": "10"
                            },
               "19977328-1": {
                                "cum": "19977328-1",
                                "descripcion": "articulo nmp",
                                "cantidad": 97,
                                "fraccion": "300"
                            }
                }
    """
    cums = {}
    for articulo in articulos:
        if articulo.cum not in cums:
            cums[articulo.cum] = {}
            cums[articulo.cum]['cum'] = articulo.cum
            cums[articulo.cum]['descripcion'] = articulo.descripcion
            cums[articulo.cum]['cantidad'] = 0
            cums[articulo.cum]['fraccion'] = str(articulo.cantidad_empaque)
        cums[articulo.cum]['cantidad'] += articulo.inventario
    return cums


def send_email(email_to: str, subject_template: str = "", html_template: str = "", environment: Dict[str, Any] = {}) -> None:
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def notify_email(info: str) -> None:
    email_to = settings.EMAIL_ADMIN
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "info": info}
    )
