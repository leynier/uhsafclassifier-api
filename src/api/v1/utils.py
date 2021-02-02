from datetime import datetime
from typing import List

import pandas as pd

from .models import Options, PersonModel


def import_excel(path: str, sheets: List[str]):
    models = []
    for sheet in sheets:
        df: pd.DataFrame = pd.DataFrame(
            pd.read_excel(path, sheet_name=sheet, skiprows=2)
        )
        for row in df.iterrows():
            models.append(fromRow(row[1], sheet))
    return models


def export_excel(path: str, sheets: List[str], data: List[List[PersonModel]]):
    for municipality, mun_data in zip(sheets, data):
        final_data = {
            "Fecha": [],
            "SAF": [],
            "Nombre y Apellidos": [],
            "Carné de Identidad": [],
            "Dirección": [],
            "Diariamente": [],
            "Regularmente": [],
            "Ocasionalmente": [],
            "No asiste": [],
            "Alto": [],
            "Medio": [],
            "Bajo": [],
            "Bueno": [],
            "Regular": [],
            "Malo": [],
            "Opiniones generales sobre el servicio SAF": [],
            "En caso no asistir, ¿cuáles son las causas?:": [],
            "Observaciones": [],
            "Cambio de Dirección": [],
            "Fallecido": [],
            "Precio": [],
            "Mala Calidad": [],
            "Poca Cantidad": [],
            "Lejanía": [],
            "Otros": [],
        }
        for person in mun_data:
            addPerson(final_data, person)
        df: pd.DataFrame = pd.DataFrame(final_data)
        df.to_excel(path, sheet_name=municipality, startrow=2)


def buildDate(data):
    parts = data.split("/")
    return datetime(year=int(parts[2]), month=int(parts[1]), day=int(parts[0]))


def fromRow(row: pd.Series, municipality: str):
    persona = PersonModel(
        date=buildDate(row['Fecha']),
        municipality = municipality,
        saf = '' if pd.isna(row['SAF']) else row['SAF'],
        full_name= '' if pd.isna(row['Nombre y Apellidos'] ) else row['Nombre y Apellidos'],
        ci= '' if pd.isna(row['Carné de Identidad']) else row['Carné de Identidad'],
        direction= '' if pd.isna(row['Dirección']) else row['Dirección'],
        attend_daily = not pd.isna(row['Diariamente']),
        attend_regular = not pd.isna(row['Regularmente']),
        attend_ocasional = not pd.isna(row['Ocasionalmente']),
        dont_attend = not pd.isna(row['No asiste']),
        service_qual_high = not pd.isna(row['Alto']),
        service_qual_medium = not pd.isna(row['Medio']),
        service_qual_low = not pd.isna(row['Bajo']),
        satisfaction_good = not pd.isna(row['Bueno']),
        satisfaction_regular = not pd.isna(row['Regular']),
        satisfaction_bad = not pd.isna(row['Malo']),
        opinions= '' if pd.isna(row['Opiniones generales sobre el servicio SAF']) else row['Opiniones generales sobre el servicio SAF'],
        causes= '' if pd.isna(row['En caso no asistir, ¿cuáles son las causas?:']) else row['En caso no asistir, ¿cuáles son las causas?:'],
        observations= '' if pd.isna(row['Observaciones']) else row['Observaciones'],
    )
    return persona


def addPerson(final_data: dict, person: PersonModel):
    final_data["Fecha"].append(str(person.date).split(" ")[0])
    final_data["SAF"].append(person.saf)
    final_data["Nombre y Apellidos"].append(person.full_name)
    final_data["Carné de Identidad"].append(person.ci)
    final_data["Dirección"].append(person.direction)
    final_data["Diariamente"].append("x" if person.attend_daily else "")
    final_data["Regularmente"].append("x" if person.attend_regular else "")
    final_data["Ocasionalmente"].append("x" if person.attend_ocasional else "")
    final_data["No asiste"].append("x" if person.dont_attend else "")
    final_data["Alto"].append("x" if person.service_qual_high else "")
    final_data["Medio"].append("x" if person.service_qual_medium else "")
    final_data["Bajo"].append("x" if person.service_qual_low else "")
    final_data["Bueno"].append("x" if person.satisfaction_good else "")
    final_data["Regular"].append("x" if person.satisfaction_regular else "")
    final_data["Malo"].append("x" if person.satisfaction_bad else "")
    final_data["Opiniones generales sobre el servicio SAF"].append(person.opinions)
    final_data["En caso no asistir, ¿cuáles son las causas?:"].append(person.causes)
    final_data["Observaciones"].append(person.observations)
    final_data["Cambio de Dirección"].append(
        "x" if Options.causes_no_dir in person.causes_tags else ""
    )
    final_data["Fallecido"].append(
        "x" if Options.causes_deceased in person.causes_tags else ""
    )
    final_data["Precio"].append(
        "x" if Options.causes_price in person.causes_tags else ""
    )
    final_data["Mala Calidad"].append(
        "x" if Options.causes_low_quality in person.causes_tags else ""
    )
    final_data["Poca Cantidad"].append(
        "x" if Options.causes_quantity in person.causes_tags else ""
    )
    final_data["Lejanía"].append(
        "x" if Options.causes_distance in person.causes_tags else ""
    )
    final_data["Otros"].append(person.causes_others)
