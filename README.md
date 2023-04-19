# Проект BLOG

## Автор
Альберт Аберхаев

## Задание
### Цель: 
Реализовать сервис, который принимает и отвечает на HTTP запросы.
### Структура:
> Блог:
> - id
> - title (заголовок)
> - description (описание блога)
> - created_at (дата создания)
> - updated_at (дата обновления - по дате последней публикации в блоге)
> - authors (связь многие ко многим с пользователем)
> - owner (владелец - создатель блога, может добавлять авторов в блог)

> Пост:
> - id
> - author (ссылка на автора)
> - title (заголовок поста)
> - body (тело поста)
> - is_published (true - опубликован, false - не опубликован, черновик)
> - created_at (дата публикации; ставится, только если пост переходит в статус is_published=True)
> - likes (счетчик оценок)
> - views (cчетки просмотров - обновляется при открытии поста)
> - tags (связь многие ко многим)

> Комментарий:
> - id
> - author (автор комментария)
> - body (тело комментария)
> - created_at (дата создания)

> Пользователь (встроенный во фреймворк)

> Теги

### Возможности пользователя:
 - создавать блог
 - добавлять в свой блог авторов (в блог, где пользователь указан как owner)
 - публиковать в блог посты (в те блоги, где пользователь - author или owner)
 - писать комментарии
 - ставить лайки
 - добавлять блоги в "мои подписки"

### Возможности адмиристратора:
- создавать, редактировать и удалять любые сущности

### Страницы (отдельные URL):
- главная - последние N постов со всех блогов
- страница "список блогов" - последние N блогов по дате обновления
- страница "посты блога" - последние N постов по дате публикации
- "мои посты" - опубликованные пользователем
- "мои подписки" - на которые подписан пользователь
- CRUD на блоги и посты, на всех страницах пагинация; сортировка по умолчанию - по дате публикации (для постов), по дате обновления (для блогов)

### Поведение:
- счетчик просмотра увеличивается при открытии поста
- поиск блогов/постов по названию и username автора
- фильтры блогов/постов: по дате (от - до отдельно друг от друга), по тегам
- сортировка блогов/постов: название(в прямом/обратном порядке), дата (в прямом/обратном порядке), лайки(в прямом/обратном порядке), опционально по релевантности/актуальности

# API
- #### Главная страница:  GET /posts/   |  список последних N постов со всех блогов
> curl --location 'http://127.0.0.1:8000/posts'

Возращает HTTP код 200 в случае успешного получения данных и тело ответа. Пример:
 
    {"id": 11,
     "title": "Алеша Попович",
     "body": "История о богатыре",
     "author": { "id": 1,
                 "username": "albert",
                 "subscriptions": [ { "id": 18,
                                      "title": "Days of week" },
                                    { "id": 19,
                                      "title": "Best Films"} ]  },
     "blog_data": { "id": 19,
                    "title": "Best Films",
                    "description": "I present best films ever",
                    "owner_name": "seconduser",
                    "authors": [ 1 ] },
     "is_published": true,
     "likes": [ 3, 1 ],
     "like_count": 2,
     "views": 6,
     "tags": [ 2, 5, 6 ] }

- #### Список блогов:   GET /blogs/   |  последние N блогов по дате обновления
> curl --location 'http://127.0.0.1:8000/blogs'

Возращает HTTP код 200 в случае успешного получения данных и тело ответа. Пример:
    
    { "id": 18,
       "title": "Days of week",
       "description": "I explain every day",
       "owner_name": "albert",
       "authors": [ 3 ] }

- #### Посты блога: GET /posts?blog='id'/ |  последние N постов блога по дате публикации
> curl --location 'http://127.0.0.1:8000/posts?blog=19'

Возращает HTTP код 200 в случае успешного получения данных и тело ответа. Пример:
    
    { "id": 11,
      "title": "Алеша Попович",
      "body": "История о богатыре",
      "author": { "id": 1,
                  "username": "albert",
                  "subscriptions": [ { "id": 18,
                                       "title": "Days of week" },
                    { "id": 19,
                      "title": "Best Films" }] },
      "blog_data": { "id": 19,
                     "title": "Best Films",
                     "description": "I present best films ever",
                     "owner_name": "seconduser",
                     "authors": [],
                     "updated_at": "2023-04-04T23:26:32.182955" },
      "is_published": false,
      "likes": [ 1, 3 ],
      "like_count": 2,
      "views": 6,
      "tags": [] }

#### Мои посты: GET /my_posts/  |  посты, опубликованные пользователем
> curl --location 'http://127.0.0.1:8000/my_posts/'

Возращает HTTP код 200 в случае успешного получения данных и тело ответа. Пример:

    { "id": 13,
      "title": "OK is?",
      "body": "Okey",
      "author": { "id": 3,
                  "username": "seconduser",
                  "subscriptions": [] },
      "blog_data": { "id": 11,
                     "title": "Famous Actors",
                     "description": "Here you can learn a lot about famous actors",
                     "owner_name": "albert",
                     "authors": [ 1, 3 ],
                     "updated_at": "2023-03-30T15:21:05.300945" },
      "is_published": false,
      "likes": [ 3 ],
      "like_count": 1,
      "views": 2,
      "tags": [] }

#### Мои подписки: GET /my_subscriptions/  |  блоги, на которые подписан пользователь
> curl --location 'http://127.0.0.1:8000/my_subscriptions/'

Возращает HTTP код 200 в случае успешного получения данных и тело ответа. Пример:
  
    {  "id": 18,
       "title": "Days of week",
       "description": "I explain every day",
       "owner_name": "albert",
       "authors": [],
       "updated_at": "2023-03-27T22:11:14.458079"  }