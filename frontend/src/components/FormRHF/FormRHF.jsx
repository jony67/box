import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';

export default function FormRHF() {
  const [state, setState] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const methods = useForm()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = methods; // инициализация хука
 
  // Функция запроса к API
  const fetchData = (method, urlend, postdata) => {
    const url = `http://127.0.0.1:8000/${urlend}/`;
    fetch(url, {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
        body: method==='POST' ? JSON.stringify(postdata) : null 
        })
        .then((res) => {
          if (res.ok) {
            return res.json()
          }
          throw res;
        })
        .then(data => {
          // Обработка полученных данных
          setState(data.state);
          console.log(state);
        })
        .catch(error => {
          console.error("Ошибка получения данных: ", error);
          setError(error);
        })
        .finally(() => {
          setLoading(false);
        })
  } 
  
  useEffect(() => {
    const interval = setInterval(() => fetchData('GET', 'state', null), 1000);
    return () => {
        // Очищаем setInterval после уничтожения компонента
        clearInterval(interval);
        
      }
    }, [state])	
  
      // Функция нажатия кнопки "Открыть"
      const onSubmitOpen = (data) => {
        try {
          console.log(data.json) 
          fetchData('POST', 'open', data);
        }
        catch(err) {
          console.log(err)
        }
      }

      // Функция нажатия кнопки "Закрыть"
      const onSubmitClose = (data) => {
        try {
          console.log(data.json) 
          fetchData("GET", 'close', null);
        }
        catch(err) {
          console.log(err)
        } 
      }

      // Функция нажатия кнопки "Повторить"
      const onSubmitRepeat = (data) => {
        try {
          console.log(data.json) 
          fetchData('GET', 'repeat', null);
        }
        catch(err) {
          console.log(err)
        } 
      }

  // Обработка ошибок
  const onErrors = errors => console.error(errors.password.message);
  // Заставка во время ожидания ответа
  if (loading) return "Подождите...";
  if (error) return "Ошибка! Минимальная длина пароля 5 символов!";

  if (state === "Введите пароль") {
    return (
      <>
        <p>Введите пароль:</p>
        <form onSubmit={handleSubmit(onSubmitOpen, onErrors)}>
          <input type='password' {...register('password', { required: 'Пустой пароль недопустим!' })} />
          {errors.password && <p>Пустой пароль недопустим!</p>}<br />
          <input type='submit' value='Открыть'/>
        </form>
      </>
    );
  }

  if (state === "Дверь открыта") {
    return (
      <>
        <p>Дверь открыта</p>
        <form onSubmit={handleSubmit(onSubmitClose, onErrors)}>  
          <input type='submit' value='Закрыть'/>
        </form>
      </>
    );   
  }

  if (state === "Закройте дверь") {
    return (
      <>
        <p>Закройте дверь</p>
        <form onSubmit={handleSubmit(onSubmitClose, onErrors)}>   
          <input type='submit' value='Закрыть'/>  
        </form>
        </>
        );   


    }

  if (state === "Неверный пароль") {
    return (
      <>
        <p>Неверный пароль</p>
        <form onSubmit={handleSubmit(onSubmitRepeat, onErrors)}>
          <input type='submit' value='Повторить'/>  
        </form>
      </>
    );   
  }
}; 
 