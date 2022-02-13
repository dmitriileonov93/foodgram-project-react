FOODGRAM - сервис, с помощью которого можно поделиться рецептом любимого блюда или найти чтото новенькое для себя.
FOODGRAM поможет составить список продуктов для рецептов, добавленных в список покупок.

Прект доступен по адресу: http://51.250.10.185

Как запустить проект на своем сервере:
1. Для загрузки введите в командную строку: "git clone https://github.com/dmitriileonov93/foodgram-project-react.git"
2. Создайте файл .env для переменных окружения в папке "foodgram-project-react/backend/foodgram/foodgram/" : "touch .env"
3. Добайте в этот файл переменные окруженмя: "echo <ПЕРЕМЕННАЯ>=<значение> >> .env"
4. Запуск приложения из дериктории "foodgram-project-react/inftra": терминале выполнить команду "docker-compose up -d"
5. Создать суперпользователя: "docker exec infra_backend_1 python3 manage.py createsuperuser"
6. Заполнение БД тестовыми данными: "docker exec infra_backend_1 python3 manage.py loaddata fixtures.json"