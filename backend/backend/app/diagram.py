# -*- coding: utf-8 -*-
"""
    Графическая модель конечного автомата на Python
    (https://github.com/pytransitions/transitions)

    @author: sev
"""

import os, sys, inspect, io

cmd_folder = os.path.realpath(
    os.path.dirname(
        os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])))

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
    
from transitions.extensions import GraphMachine
from IPython.display import Image, display
from MyBox import MyBox


class Model():
    
    # Графический объект создается машиной состояний
    def show_graph(self, **kwargs):
        stream = io.BytesIO()
        self.get_graph(**kwargs).draw(stream, prog='dot', format='png')
        display(Image(stream.getvalue()))

        
class Box(Model):
    def alert(self):
        pass
    
    def resume(self):
        pass
    
    def notify(self):
        pass
    
    def is_valid(self):
        return True
    
    def is_not_valid(self):
        return False
    
    def is_also_valid(self):
        return True
   

def show_model(my_model):
    model = Box()
    # Инициализация и настройка своей модели
    extra_args = dict(initial=my_model.initial, title='Модель камеры хранения',
                  show_conditions=True, show_state_attributes=True)
    
    # Строим графическую модель
    GraphMachine(model=model, states=my_model.my_states, transitions=my_model.my_transitions, 
                       show_auto_transitions=False, **extra_args)
    
    # Выводим график
    model.show_graph()
    
    
if __name__ == '__main__':
   show_model(MyBox())
       
    
    
    
    