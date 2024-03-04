
Инструкция по запуску

# Запуск через докеры
Установить docker
```sh
sudo apt install docker.io docker-compose
```
Необходимо ввести команду
```
sudo docker-compose up --build -d
```

# Запуск без использования докеров
## Настройка postgresql
Необходимо скопировать скрипты из папки BD в общедоступное место, а затем выполнить
Открыть консоль пострес
```sh
sudo -u postgresql psql
```
Создать базу данных
```psql
\i {path_to_file}\Create.sql
```
Переключиться на неё
```psql
\c ForkLog
```
Создать таблицу
```psql
\i {path_to_file}\Table.sql
```
Создать функцию
```psql
\i {path_to_file}\Function.sql
```
`Все предыдущие действия выполнены для моих скриптов, однако можно создать свою таблицу в базе данных, главное потом добавить новые значения в config.ini`
## Запуск бота
Активация виртуального окружения
```sh
python -m venv venv
```
Windows
```ps
.\.venv\Scripts\Activate.ps1
```
Linux
```bash
source venv/bin/activate
```
Установка библиотек
```sh
pip install -r requirements.txt
```
Запуск бота
```sh
python main.py
```
