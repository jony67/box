# -*- coding: utf-8 -*-
"""
    MyBox(Machine) - класс модели системы автоматической камеры хранения
    на Python (https://github.com/pytransitions/transitions). Камера хранения
    представляет собой шкаф с дверцей, оснащенной электрическим замком.
    В начальном состоянии камера закрыта и необходимо ввести пароль.
    При совпадении пароля с сохраненным в системе дверь камеры хранения
    автоматически открывается. При закрытии двери замок закрывается,
    и система переходит в исходное состояние – ожидание ввода пароля.
    Если дверь не будет закрыта в течение заданного промежутка времени,
    должно быть выведено предупреждение. После закрытия двери предупреждение
    отключается, система переходит в исходное состояние.

    @author: sev
"""

from time import sleep
from transitions import Machine
from threading import Thread


class MyBox(Machine):
    """
        Модель камеры хранения на основе класса Machine.

        :param TIMEOUT: Время условного перехода в сек.
        :param my_states: Список состояний системы.
        :param my_transitions: Триггеры переходов.
        :param add_transition: Добавление условного перехода
    """   
    TIMEOUT = 5.0 # задержка таймера

    def stop(self, delay_time):
        """
            Целевая функция для self.on_timeout()

            :param delay_time: время задержки в секундах
        """
        sleep(delay_time)
        if self.state == 'Дверь открыта':
            self.state = 'Закройте дверь'
        return self.state

    def on_timeout(self): 
        """
            Функция таймера в отдельном потоке
        """
        box_open = Thread(target=self.stop, args=(self.TIMEOUT,))
        box_open.start()
        box_open.join()

    # Конструктор
    def __init__(self):
        # Состояния
        self.my_states = [
            'Введите пароль',
            'Дверь открыта',
            'Закройте дверь',
            'Неверный пароль'
        ]
        # Переходы:       
        self.my_transitions = [
            { 'trigger': 'good_password', 'source': 'Введите пароль', 'dest': 'Дверь открыта', 'after': 'on_timeout' },
            { 'trigger': 'closed', 'source': ['Дверь открыта', 'Закройте дверь'], 'dest': 'Введите пароль' },
            { 'trigger': 'timeout', 'source': 'Дверь открыта', 'dest': 'Закройте дверь' },    
            { 'trigger': 'bad_password', 'source': 'Введите пароль', 'dest': 'Неверный пароль' },
            { 'trigger': 'repeat', 'source': 'Неверный пароль', 'dest': 'Введите пароль' }
            ]
               
        Machine.__init__(
            self,
            states=self.my_states,
            transitions=self.my_transitions,
            initial = 'Введите пароль'
            )


        
    def __str__(self):
        s = f"\tСоздается экземпляр класса Transitions для состояний:\n\
        {self.my_states} \n\n\tс переходами: \n {self.my_transitions}"
        return print(s) 



def main():
   return MyBox() 

def test():
   """
    Функция для тестирования работы класса
   """  
   machine = MyBox()
   def ft1(): 
    machine.good_password()

   def ft2(t):
    sleep(t)
    if (machine.state == 'Дверь открыта'):
        machine.timeout()  

   print(machine.state) # исходное состояние
   t1 = Thread(target=ft1, args=())   
   t2 = Thread(target=ft2, args=(1,))
   t1.start()
   t2.start()
   t1.join()
   t2.join()     
   print(machine.state) # состояние


if __name__ == "__main__":
   test()
   