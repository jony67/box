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
from time import sleep as sleep
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
    TIMEOUT = 10.0 # задержка таймера

    def on_delay(self, delay_time):
        """
            Целевая функция для self.on_timeout()

            :param delay_time: время задержки в секундах
        """
        sleep(delay_time)
        if self.state == 'Дверь открыта':
            self.timeout()
        else:
           exit

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
   return MyBox() 

def test(delay):
   """
    Функция для тестирования работы класса. Если delay < TIMEOUT,
    то имитируем ситуацию, когда пользователь закрыл камеру
    хранения до истечения времени напоминания, если delay > TIMEOUT,
    то имитируем ситуацию, когда система перешла в режим напоминания
    и пользователь закрыл камеру хранения.

    :param delay: Время задержки
   """  
   machine = MyBox()
   def ft1():
    print("1-й поток. Исходное состояние, затем сразу следует ввод пароля: ", machine.state)
    machine.good_password()
    print("1-й поток. Сработал таймер перехода TIMEOUT: ", machine.state)
    if (machine.state == 'Закройте дверь'):
        machine.close()  
        print("1-й поток. Пользователь закрыл камеру хранения: ", machine.state)

   def ft2(t):
    print("2-й поток. Ожидаем команды закрытия от пользователя: ", machine.state)
    sleep(t)
    if (machine.state == 'Дверь открыта'):
        machine.close()  
        print("2-й поток. Пользователь закрыл камеру хранения: ", machine.state)

   t1 = Thread(target=ft1, args=(), daemon=True)   
   t2 = Thread(target=ft2, args=(delay,), daemon=True)
   t1.start()
   t2.start()
   t1.join()
   t2.join()        


if __name__ == "__main__":
   print("Пример 1: пользователь закрыл камеру хранения до напоминания:\n")
   test(5)
   print("\nПример 2: пользователь закрыл камеру хранения после напоминания:\n")
   test(15)
   