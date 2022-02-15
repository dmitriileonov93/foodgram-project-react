# FOODGRAM

### Описание
FOODGRAM - сервис, с помощью которого можно поделиться рецептом любимого блюда или найти чтото новенькое для себя.
FOODGRAM поможет составить список продуктов для рецептов, добавленных в список покупок.

Проект доступен по адресу: http://51.250.10.185

### Запуск проекта
- Для загрузки введите в командную строку:
```
git clone https://github.com/dmitriileonov93/foodgram-project-react.git
```
- Создайте файл .env для переменных окружения в папке:
```
touch foodgram-project-react/backend/foodgram/foodgram/.env
```
- Добайте в этот файл переменные окруженмя:
```
echo <ПЕРЕМЕННАЯ>=<значение> >> .env
```
- Запуск приложения из дериктории "foodgram-project-react/inftra":
```
docker-compose up -d
```
- Создать суперпользователя:
```
docker exec infra_backend_1 python3 manage.py createsuperuser
```
- Заполнение БД тестовыми данными:
```
docker exec infra_backend_1 python3 manage.py loaddata fixtures.json
```
