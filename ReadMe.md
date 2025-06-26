# Wildberries Parser - Анализатор товаров

Программа для анализа товаров Wildberries с визуализацией данных в виде таблиц и графиков.

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/FedorSmorodskii/wb_parser_project
```

2. Установите зависимости для фронтенда:
```bash
cd frontend
npm install
```

3. Установите зависимости для бэкенда:
```bash
cd ../backend
pip install -r requirements.txt
```

## Запуск

1. Запустите бэкенд (Django):
```bash
cd backend
python manage.py runserver
```

2. Запустите фронтенд (React):
```bash
cd ../frontend
npm start
```

Приложение будет доступно по адресу:
http://localhost:3000


Пример команды:
python manage.py parse_wildberries "ноутбук"
