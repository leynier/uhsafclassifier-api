import pandas as pd

from typing import *

from datetime import datetime

from .models import PersonModel, Options

def import_excel(path: str, sheets:List[str]):
    models = []
    for sheet in sheets:
        df:pd.DataFrame = pd.DataFrame(pd.read_excel(path, sheet_name=sheet, skiprows=2))
        for row in df.iterrows():
            models.append(fromRow(row[1], sheet))
    return models

def export_excel(path:str, sheets:List[str], data:List[List[PersonModel]]):
    for municipality, mun_data in zip(sheets, data):
        final_data = {
        'Fecha': [],
        'SAF': [],
        'Nombre y Apellidos': [],
        'Carné de Identidad': [],
        'Dirección': [],
        'Diariamente': [],
        'Regularmente': [],
        'Ocasionalmente': [],
        'No asiste': [],
        'Alto': [],
        'Medio': [],
        'Bajo': [],
        'Bueno': [],
        'Regular': [],
        'Malo': [],
        'Opiniones generales sobre el servicio SAF': [],
        'En caso no asistir, ¿cuáles son las causas?:': [],
        'Observaciones': [],
        'Cambio de Dirección': [],
        'Fallecido': [],
        'Precio': [],
        'Mala Calidad': [],
        'Poca Cantidad': [],
        'Lejanía': [],
        'Otros': [],
        }
        for person in mun_data:
            addPerson(final_data, person)
        df:pd.DataFrame = pd.DataFrame(final_data)
        df.to_excel(path, sheet_name=municipality,startrow=2)

def buildDate(data):
    parts = data.split('/')
    return datetime(year=int(parts[2]), month=int(parts[1]), day=int(parts[0]))

def fromRow(row: pd.Series, municipality: str):
    persona = PersonModel()
    persona.date: datetime = buildDate(row['Fecha'])
    persona.municipality: str = municipality
    persona.saf: str = '' if pd.isna(row['SAF']) else row['SAF']
    persona.full_name: str = '' if pd.isna(row['Nombre y Apellidos'] ) else row['Nombre y Apellidos']
    persona.ci: str = '' if pd.isna(row['Carné de Identidad']) else row['Carné de Identidad']
    persona.direction: str = '' if pd.isna(row['Dirección']) else row['Dirección']
    persona.attend_daily: bool = not pd.isna(row['Diariamente'])
    persona.attend_regular: bool = not pd.isna(row['Regularmente'])
    persona.attend_ocasional: bool = not pd.isna(row['Ocasionalmente'])
    persona.dont_attend: bool = not pd.isna(row['No asiste'])
    persona.service_qual_high: bool = not pd.isna(row['Alto'])
    persona.service_qual_medium: bool = not pd.isna(row['Medio'])
    persona.service_qual_low: bool = not pd.isna(row['Bajo'])
    persona.satisfaction_good: bool = not pd.isna(row['Bueno'])
    persona.satisfaction_regular: bool = not pd.isna(row['Regular'])
    persona.satisfaction_bad: bool = not pd.isna(row['Malo'])
    persona.opinions: str = '' if pd.isna(row['Opiniones generales sobre el servicio SAF']) else row['Opiniones generales sobre el servicio SAF']
    persona.causes: str = '' if pd.isna(row['En caso no asistir, ¿cuáles son las causas?:']) else row['En caso no asistir, ¿cuáles son las causas?:']
    persona.observations: str = '' if pd.isna(row['Observaciones']) else row['Observaciones']
    return persona

def addPerson(final_data: dict, person: PersonModel):
    final_data['Fecha'].append(str(person.date).split(' ')[0])
    final_data['SAF'].append(person.saf)
    final_data['Nombre y Apellidos'].append(person.full_name)
    final_data['Carné de Identidad'].append(person.ci)
    final_data['Dirección'].append(person.direction)
    final_data['Diariamente'].append('x' if person.attend_daily else '')
    final_data['Regularmente'].append('x' if person.attend_regular else '')
    final_data['Ocasionalmente'].append('x' if person.attend_ocasional else '')
    final_data['No asiste'].append('x' if person.dont_attend else '')
    final_data['Alto'].append('x' if person.service_qual_high else '')
    final_data['Medio'].append('x' if person.service_qual_medium else '')
    final_data['Bajo'].append('x' if person.service_qual_low else '')
    final_data['Bueno'].append('x' if person.satisfaction_good else '')
    final_data['Regular'].append('x' if person.satisfaction_regular else '')
    final_data['Malo'].append('x' if person.satisfaction_bad else '')
    final_data['Opiniones generales sobre el servicio SAF'].append(person.opinions)
    final_data['En caso no asistir, ¿cuáles son las causas?:'].append(person.causes)
    final_data['Observaciones'].append(person.observations)
    final_data['Cambio de Dirección'].append('x' if Options.causes_no_dir in person.causes_tags else '')
    final_data['Fallecido'].append('x' if Options.causes_deceased in person.causes_tags else '')
    final_data['Precio'].append('x' if Options.causes_price in person.causes_tags else '')
    final_data['Mala Calidad'].append('x' if Options.causes_low_quality in person.causes_tags else '')
    final_data['Poca Cantidad'].append('x' if Options.causes_quantity in person.causes_tags else '')
    final_data['Lejanía'].append('x' if Options.causes_distance in person.causes_tags else '')
    final_data['Otros'].append(person.causes_others)
