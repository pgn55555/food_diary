from sqlalchemy import create_engine, Integer, String, DateTime, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import pandas as pd

from datetime import datetime

class DataBase:
    Base = declarative_base()

    def __init__(self, db_path) -> None:
        self.engine = create_engine(db_path)
        self.Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    class Dishes(Base):
        __tablename__ = 'dishes'
        name = Column(String(), nullable=True)
        datetime_add = Column(DateTime(), primary_key=True)
        calories = Column(Integer(), nullable=False)
        proteins = Column(Integer(), nullable=False)
        fats = Column(Integer(), nullable=False)
        carbohydrates = Column(Integer(), nullable=False)

    def get_dishes(self, name: int) -> Dishes:
        row = self.session.query(self.Dishes).filter(
            self.Dishes.name == name)
        return row
    
    def add_dish(self, data: dict) -> None:        
        new_dish = self.Dishes(
            name = data['name'],
            datetime_add = datetime.now(),
            calories = data['calories'],
            proteins = data['proteins'],
            fats = data['fats'],
            carbohydrates = data['carbohydrates']
        )

        self.session.add(new_dish)
        self.session.new
        self.session.commit()
    
    def edit_dish(self, data: dict) -> None:
        row = self.get_dishes(data['name'])

        updated_values = {
            self.Dishes.name: data['name'],
            self.Dishes.calories: data['calories'],
            self.Dishes.proteins: data['proteins'],
            self.Dishes.fats: data['fats'],
            self.Dishes.carbohydrates: data['carbohydrates']
        }

        row.update(updated_values, synchronize_session=False)
        self.session.commit()
    
    def get_all_dishes(self) -> list:
        return [name[0] for name in self.session.query(self.Dishes.name).distinct()]
    
    def get_dataset(self) -> pd.DataFrame:
        query = "SELECT * FROM dishes"
        return pd.read_sql(query, self.engine)

