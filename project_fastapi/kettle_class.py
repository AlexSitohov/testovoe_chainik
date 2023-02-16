from time import sleep

import redis

"""
Класс описывающий работу чайника. Вода в чайнике вскипает за 10 секунд (из описания ТЗ).
"""


class Kettle:
    __BOIL_TIME = 10
    __BOILING_TEMPERATURE = 100
    __MIN_AMOUNT_OF_WATER = 0
    __MAX_AMOUNT_OF_WATER = 1.0

    def __init__(self, amount_of_water: float | int, water_temperature: int = 0):
        self.__amount_of_water = self.__MIN_AMOUNT_OF_WATER

        if self.__amount_of_water_validator(amount_of_water):
            self.__amount_of_water = amount_of_water

        if self.__water_temperature_validator(water_temperature):
            self.__water_temperature = water_temperature

    def __str__(self):
        return self.__water_temperature

    @classmethod
    def __amount_of_water_validator(cls, amount_of_water: float | int) -> bool:
        if isinstance(amount_of_water,
                      (float, int)) and cls.__MIN_AMOUNT_OF_WATER <= amount_of_water <= cls.__MAX_AMOUNT_OF_WATER:
            return True
        raise TypeError('Количество воды введено не правильно')

    @classmethod
    def __water_temperature_validator(cls, water_temperature):
        if water_temperature <= cls.__BOILING_TEMPERATURE:
            return True
        raise TypeError('Температура воды введена не правильно')

    @property
    def temperature(self):
        return self.__water_temperature

    @temperature.setter
    def temperature(self, value):
        self.__water_temperature = value

    # Метод, который реализует моделирование закипания чайника
    def heat_watter(self):
        # value - это разница температуры через каждую секунду
        value = self.__temperature_every_second(self.__BOILING_TEMPERATURE, self.temperature, self.__BOIL_TIME)

        redis_client = redis.Redis(host='localhost', port=6379)

        # print('ВКЛ')
        redis_client.lpush("zxc", 'ВКЛ')

        # Пока температура воды в чайнике меньше чем температура кипения воды
        while self.temperature < self.__BOILING_TEMPERATURE:
            # print(f'Температура: {round(self.temperature)} градусов')

            redis_client.lpush("zxc", f'Температура: {round(self.temperature)} градусов')
            sleep(1)
            self.temperature += value
        redis_client.lpush("zxc", f'Температура: {round(self.temperature)} градусов')
        redis_client.lpush("zxc", 'Вскипел')
        redis_client.lpush("zxc", 'ВЫКЛ')

    # Статический метод определяющий разницу температуры через каждую секунду
    @staticmethod
    def __temperature_every_second(boiling_temperature, self_temperature, boil_time):
        return (boiling_temperature - self_temperature) / boil_time


kettle = Kettle(1, water_temperature=10)
kettle.heat_watter()
