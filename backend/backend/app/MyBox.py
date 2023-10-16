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
from transitions import Machine
from threading import Thread
from threading import Timer 


class MyBox(Machine):
    """
        Модель камеры хранения на основе класса Machine.

        :param TIMEOUT: Время условного перехода в сек.
        :param my_states: Список состояний системы.
        :param my_transitions: Триггеры переходов.
        :param add_transition: Добавление условного перехода
    """   
    TIMEOUT = 10.0 # задержка таймера
  
    def f(self):
        """
            Функция автоматического перехода в состояние 'Закройте дверь'
        """
        if self.state == 'Дверь открыта':
            self.timeout()
        else:
            exit    
    
    def on_delay(self, delay_time):
        """
            Целевая функция для self.on_timeout()

            :param delay_time: время задержки в секундах
        """
        timer = Timer(delay_time, self.f) 
        timer.start()


    def on_timeout(self):
        """
            Функция таймера в отдельном потоке
            
        """
        self.state = 'Дверь открыта'
        box_open = Thread(target=self.on_delay, args=(self.TIMEOUT,))
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
            { 'trigger': 'close', 'source': ['Дверь открыта', 'Закройте дверь'], 'dest': 'Введите пароль' },
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
   """
    Функция создания экземпляра класса MyBox
   """  
   machine=MyBox()
   return machine   


if __name__ == "__main__":
    main()