## Веб-сайт, который анализирует пул вакансий из ХХ по зарплатам из конкретного региона или по всей России

Используется функция __get_vacancies__, которая отправляет запросы к API HH.ru и получает список вакансий по указанным параметрам (текст поиска, регион и количество страниц).
Ответы от API обрабатываются и сохраняются в список всех вакансий.

### Основные компоненты:

__app.py:__ Основной файл приложения, написанного на Flask. Этот файл содержит все маршруты и логику обработки запросов   
__requirements.txt:__ Файл, содержащий список зависимостей, необходимых для запуска приложения   
__templates:__ Директория с HTML-шаблонами, используемыми для рендеринга веб-страниц   

### Зависимости:

__Flask:__ Фреймворк для разработки веб-приложений на Python    
__requests:__ Библиотека для выполнения HTTP-запросов   
__pandas:__ Библиотека для работы с данными и их анализа   
__matplotlib:__ Библиотека для создания визуализаций данных   

### Инструкция: 

1. В поисковой запрос вводим название вакансии
<img width="406" alt="image" src="https://github.com/sxsatirize/API-job/assets/117602697/33096232-c0e6-4bff-987e-ca4e8073d411">   

2. В регион вводим ID соответствующего региона. Регион Москвы имеет ID 1. Если нужен другой город, то кликаем на знак вопроса и ищем в таблице нужный регион. После поиска возвращаемся обратно в форму и вводим нужный ID
 <img width="1441" alt="image" src="https://github.com/sxsatirize/API-job/assets/117602697/ff0f28e4-670c-44fc-bd84-2f63f3303bae">   

3. После того, как ввели все данные, жмём на кнопку Анализировать и на странице получаем таблицу с выводом распределения зарплат
<img width="1256" alt="image" src="https://github.com/sxsatirize/API-job/assets/117602697/194f08fa-0a02-4363-868b-a1feacccf7d9">   
