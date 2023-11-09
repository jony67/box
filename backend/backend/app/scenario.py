from time import sleep
from threading import Thread
from backend.app.MyBox import MyBox

def test_my_box(t):
   """
    Функция для тестирования работы класса в потоках. Если delay < TIMEOUT,
    то имитируем ситуацию, когда пользователь закрыл камеру
    хранения до истечения времени напоминания, если delay > TIMEOUT,
    то имитируем ситуацию, когда система перешла в режим напоминания
    и пользователь закрыл камеру хранения.

    :param t: Время задержки
   """  
   def ft1(my_machine):
    print("1-й поток. Исходное состояние, затем сразу следует ввод пароля: ", my_machine.state)
    my_machine.good_password()
    print("1-й поток. Таймер автоматического перехода TIMEOUT запущен: ", my_machine.state)
    if (my_machine.state == 'Закройте дверь'):
        my_machine.close()  
        print("1-й поток. Пользователь закрыл камеру хранения: ", my_machine.state)

   def ft2(my_machine,t):
    sleep(t)  
    if (my_machine.state == 'Дверь открыта'):
        my_machine.close()  
        print("2-й поток. Пользователь закрыл камеру хранения: ", my_machine.state)
    else:
        print("2-й поток. Сработал автоматический переход: ", my_machine.state)
        sleep(3)
        my_machine.close()
        print("2-й поток. Пользователь закрыл камеру хранения: ", my_machine.state)
   
   machine = MyBox()
   t1 = Thread(target=ft1, args=(machine,), daemon=True)   
   t2 = Thread(target=ft2, args=(machine,t,), daemon=True)
   t1.start()
   t2.start()
   t1.join()
   t2.join()        

print("Пример 1: пользователь закрыл камеру хранения до напоминания:\n")
test_my_box(5)
sleep(3)
print("\nПример 2: пользователь закрыл камеру хранения после напоминания:\n")
test_my_box(15)
   