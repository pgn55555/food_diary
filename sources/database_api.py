from sqlalchemy import create_engine, Integer, String, DateTime, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from datetime import datetime

class DataBase:
    Base = declarative_base()

    def __init__(self, db_path) -> None:
        self.engine = create_engine(db_path)
        self.Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    class Dishes(Base):
        __tablename__ = 'dishes'
        name = Column(String(), primary_key=True)
        datetime_add = Column(DateTime(), nullable=True)
        calories = Column(Integer(), nullable=False)
        proteins = Column(Integer(), nullable=False)
        fats = Column(Integer(), nullable=False)
        carbohydrates = Column(Integer(), nullable=False)

    def get_dish(self, name: int):  # TODO: что возвращает
        row = self.session.query(self.Dishes).filter(
            self.Dishes.name == name).first()
        return row
    
    def __is_dish_exists(self, name: int) -> bool:
        answer = self.get_dish(name)
        return answer is not None
    
    def add_dish(self, data: dict) -> str:
        if self.__is_dish_exists(data['name']):
            return "Такое блюдо уже существует"
        
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

        return "Блюдо добавлено успешно"
    
    def edit_dish(self, data: dict) -> None:
        row = self.get_dish(data['name'])

        updated_values = {
            self.Dishes.name: data['name'],
            self.Dishes.calories: data['calories'],
            self.Dishes.proteins: data['proteins'],
            self.Dishes.fats: data['fats'],
            self.Dishes.carbohydrates: data['carbohydrates']
        }

        row.update(updated_values, synchronize_session=False)
    
    def get_all_dishes(self) -> list:
        return [name for name in self.session.query(self.Dishes.name)]
