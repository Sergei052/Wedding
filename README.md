# Свадебное приглашение

Сайт-приглашение с RSVP-формой. Гость вводит имя и отвечает, придёт ли он. Если придёт, указывает, будет ли с ним сопровождающий. Ответы сохраняются в базу и видны в админке Django. Страница рассчитана на телефоны.



## Возможности

- Одна страница-приглашение: фото в арке, фон, даты, место (ссылка на Яндекс.Карты), дресс-код.
- Обратный отсчёт дней до свадьбы (JavaScript в `invitation.html`, часовой пояс +03:00).
- Форма ответа: имя, «придёт / не придёт», «будет ли сопровождающий».
- Вопрос про сопровождающего показывается только тем, кто придёт. Если гость выбрал «не смогу», сервер всё равно сохраняет `has_companion = False`.
- Имя уникально без учёта регистра и лишних пробелов: повторно ответить с тем же именем нельзя.
- После отправки показывается страница благодарности (разная для «да» и «нет»).
- Все ответы доступны в админке `/admin/`: поиск по имени, фильтры по ответу и сопровождающему.

## Стек

Python, Django 6.1, WhiteNoise (статика), Gunicorn (сервер), python-dotenv (настройки из `.env`), dj-database-url (подключение к базе). База: SQLite по умолчанию, PostgreSQL через `DATABASE_URL`. Шрифты (Cormorant, Manrope) подгружаются с Google Fonts.

## Структура

```
config/                  настройки проекта (settings, urls, wsgi, asgi)
rsvp/                    приложение: модель, форма, view, админка, миграции
rsvp/static/rsvp/        photo.jpg (фото в арке) и background.jpg (фон)
rsvp/templates/rsvp/     invitation.html (страница приглашения)
manage.py                управление проектом
Procfile                 команда запуска для PaaS (gunicorn)
requirements.txt         зависимости
.env                     секреты и настройки (в git не попадает)
```

## Настройки (файл .env)

Настройки читаются из файла `.env` в корне проекта (рядом с `manage.py`). Без `DJANGO_SECRET_KEY` проект не запустится.

| Переменная | Назначение | По умолчанию |
|---|---|---|
| `DJANGO_SECRET_KEY` | секретный ключ (обязательно) | — |
| `DJANGO_DEBUG` | `1` — режим разработки, `0` — боевой | `0` |
| `DJANGO_ALLOWED_HOSTS` | допустимые адреса через запятую | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | адреса сайта с `https://` через запятую | пусто |
| `DJANGO_HTTPS` | `1` — включить https-защиту (редирект, secure cookies, HSTS) | `0` |
| `DATABASE_URL` | адрес базы, например `postgres://user:pass@host:5432/dbname` | SQLite-файл `db.sqlite3` |

Сгенерировать секретный ключ:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

Для сервера и для компьютера используйте разные ключи.

## Запуск на компьютере

1. Создайте окружение и установите зависимости:

```bash
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install -r requirements.txt
```

2. Создайте файл `.env` рядом с `manage.py`:

```
DJANGO_SECRET_KEY=сюда-вставьте-длинную-случайную-строку
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

3. Подготовьте базу, создайте админа и запустите:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/
Админка с ответами: http://127.0.0.1:8000/admin/

## Проверка на телефоне

Компьютер и телефон должны быть в одной Wi-Fi сети.

1. Узнайте IP компьютера в сети: `ipconfig` в Windows, `ifconfig` или `ip a` в macOS/Linux (адрес вида `192.168.0.15`).
2. Добавьте его в `.env`:

```
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,192.168.0.15
```

3. Запустите сервер так, чтобы он был виден в сети:

```bash
python manage.py runserver 0.0.0.0:8000
```

4. Откройте на телефоне `http://192.168.0.15:8000/` (подставьте свой IP).

Если страница не открывается, проверьте, что брандмауэр пропускает порт 8000.

## Как поменять текст, дату, фото или фон

**Тексты, дата, место, дресс-код** лежат в `rsvp/templates/rsvp/invitation.html`. Дата обратного отсчёта задана в скрипте внизу файла (`new Date('2027-08-30T00:00:00+03:00')`). При смене даты поменяйте её и в тексте страницы.

**Фото и фон:**

1. Замените файлы `rsvp/static/rsvp/photo.jpg` или `rsvp/static/rsvp/background.jpg`. Имя и расширение `.jpg` должны остаться прежними.
2. Фон лучше брать вертикальный, от 1080×1920, до 1 МБ.
3. В `invitation.html` в адресе фона есть `?v=2`. После замены картинки увеличьте число (`?v=3` и так далее), иначе телефон может показать старую картинку из кэша.
4. Закоммитьте и запушьте изменения, затем обновите сервер (см. «Обновление сайта»).

## Деплой на сервер (Ubuntu, VPS)

Что понадобится: сервер с Ubuntu 22.04 или 24.04, домен, A-запись домена на IP сервера (DNS обновляется от нескольких минут до суток), репозиторий на GitHub. Ниже вместо `example.com` подставьте свой домен.

### 1. Подготовка сервера

Подключитесь по SSH (`ssh root@IP_СЕРВЕРА`) и выполните:

```bash
apt update && apt upgrade -y
apt install -y python3-venv python3-pip git nginx certbot python3-certbot-nginx ufw

ufw allow OpenSSH
ufw allow "Nginx Full"
ufw --force enable

adduser --disabled-password --gecos "" wedding
mkdir -p /srv/wedding
chown wedding:wedding /srv/wedding
```

### 2. Код и окружение

```bash
sudo -u wedding -i
cd /srv/wedding
git clone ССЫЛКА_НА_ВАШ_РЕПОЗИТОРИЙ app
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Если репозиторий приватный, git попросит логин и токен GitHub (Settings → Developer settings → Personal access tokens) или настройте deploy key.

### 3. Файл .env на сервере

```bash
nano /srv/wedding/app/.env
```

Для первого запуска (пока нет https):

```
DJANGO_SECRET_KEY=новый-длинный-ключ-только-для-сервера
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=example.com,www.example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
DJANGO_HTTPS=0
```

Сохранить в nano: `Ctrl+O`, `Enter`, выйти: `Ctrl+X`.

### 4. База, админ и статика

```bash
cd /srv/wedding/app
source .venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
exit
```

Команда `exit` возвращает вас в root.

### 5. Автозапуск сайта (systemd)

Создайте файл `/etc/systemd/system/wedding.service`:

```
[Unit]
Description=Wedding RSVP (gunicorn)
After=network.target

[Service]
User=wedding
Group=wedding
WorkingDirectory=/srv/wedding/app
ExecStart=/srv/wedding/app/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

Запустите:

```bash
systemctl daemon-reload
systemctl enable --now wedding
systemctl status wedding
```

В статусе должно быть `active (running)`. Если нет, смотрите ошибки: `journalctl -u wedding -n 50`.

### 6. nginx

Создайте файл `/etc/nginx/sites-available/wedding`:

```
server {
    listen 80;
    server_name example.com www.example.com;
    client_max_body_size 1m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Включите сайт:

```bash
ln -s /etc/nginx/sites-available/wedding /etc/nginx/sites-enabled/wedding
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
```

Откройте `http://example.com`: сайт должен работать (пока без https).

### 7. HTTPS

```bash
certbot --nginx -d example.com -d www.example.com
```

Certbot выпустит сертификат, настроит nginx и сам будет его продлевать. Откройте `https://example.com` и проверьте, что сайт работает. После этого в `/srv/wedding/app/.env` поменяйте:

```
DJANGO_HTTPS=1
```

и перезапустите сайт:

```bash
systemctl restart wedding
```

### 8. Проверка

- Откройте сайт на телефоне: фон и фото должны загрузиться.
- Отправьте тестовый ответ и найдите его в `https://example.com/admin/`.
- Удалите тестовый ответ в админке.

## Деплой на PaaS (Heroku-подобные платформы)

В репозитории есть `Procfile` с командой запуска:

```
web: gunicorn config.wsgi:application
```

На платформе задайте переменные окружения из таблицы выше (`DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, `DJANGO_HTTPS=1`) и `DATABASE_URL` с адресом PostgreSQL. Файловая система на таких платформах обычно временная, поэтому SQLite там использовать нельзя: ответы пропадут при перезапуске. После деплоя выполните `python manage.py migrate`, `python manage.py createsuperuser` и `python manage.py collectstatic --noinput` (если платформа не делает это сама).

## Обновление сайта

1. На компьютере внесите изменения и проверьте их локально.
2. Закоммитьте и запушьте:

```bash
git add -A
git commit -m "Что изменили"
git push
```

3. На сервере (под root или с sudo):

```bash
sudo -u wedding -i
cd /srv/wedding/app
git pull
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
exit
systemctl restart wedding
```

| Команда | Зачем |
|---|---|
| `git pull` | забрать новый код |
| `pip install -r requirements.txt` | поставить новые зависимости, если они появились |
| `python manage.py migrate` | применить новые миграции базы |
| `python manage.py collectstatic --noinput` | обновить фото и фон |
| `systemctl restart wedding` | перезапустить сайт, чтобы изменения вступили в силу |

Если меняли фон или фото, не забудьте увеличить число в `?v=2` в `invitation.html`.

Чтобы не вводить всё вручную, создайте файл `/srv/wedding/update.sh`:

```bash
#!/bin/bash
set -e
cd /srv/wedding/app
git pull
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Сделайте его исполняемым один раз: `chmod +x /srv/wedding/update.sh`. Дальше обновление такое:

```bash
sudo -u wedding /srv/wedding/update.sh && sudo systemctl restart wedding
```

### Откат, если после обновления что-то сломалось

```bash
sudo -u wedding -i
cd /srv/wedding/app
git log --oneline -5          # найдите номер рабочего коммита
git checkout НОМЕР_КОММИТА
exit
systemctl restart wedding
```

Чтобы вернуться к последней версии: `git checkout main` и обновление, как выше. Если вместе с кодом применялись миграции базы, базу нельзя просто «откатить» вместе с кодом — сначала разберитесь с миграциями.

## Ответы гостей и резервные копии

- Смотреть ответы: `/admin/`.
- Имя уникально без учёта регистра, поэтому просите гостей писать имя и фамилию.
- Если `DATABASE_URL` не задан, все ответы лежат в файле `db.sqlite3` в корне проекта (на сервере: `/srv/wedding/app/db.sqlite3`). В git он не хранится, поэтому **ни в коем случае не удаляйте его и не перезаписывайте**.

Скачать копию SQLite-базы на компьютер (команда выполняется на вашем компьютере):

```bash
scp root@IP_СЕРВЕРА:/srv/wedding/app/db.sqlite3 ./db-backup.sqlite3
```

Ежедневная копия на самом сервере (`crontab -e` под пользователем `wedding`):

```
0 4 * * * cp /srv/wedding/app/db.sqlite3 /srv/wedding/db-$(date +\%F).sqlite3
```

Раз в несколько недель скачивайте копию к себе: копия на том же сервере не спасёт, если сервер пропадёт.

Если используете PostgreSQL, делайте копии через `pg_dump` или средствами хостинга.

## Если что-то не работает

| Симптом | Причина и решение |
|---|---|
| `RuntimeError: DJANGO_SECRET_KEY не задан` | Нет файла `.env` или в нём нет ключа. |
| Ошибка 400 (Invalid HTTP_HOST) | Домен или IP не добавлен в `DJANGO_ALLOWED_HOSTS`. |
| Ошибка 502 Bad Gateway | Сайт не запущен: `systemctl status wedding` и `journalctl -u wedding -n 50`. |
| Нет фона и фото | Выполните `collectstatic` и перезапустите сайт. Локально поставьте `DJANGO_DEBUG=1`. |
| Показывается старый фон | Увеличьте число в `?v=2` в `invitation.html`, обновите сервер, откройте сайт в приватной вкладке. |
| Страница бесконечно перенаправляется на https | В nginx должен быть заголовок `X-Forwarded-Proto`. Временно поставьте `DJANGO_HTTPS=0` и перезапустите сайт. |
| Ошибка 403 CSRF при отправке формы | Добавьте адрес сайта с `https://` в `DJANGO_CSRF_TRUSTED_ORIGINS`. |
| Сертификат не выпускается | Проверьте, что A-запись домена указывает на IP сервера и порты 80 и 443 открыты. |
| Ошибка подключения к базе (SSL) | В `settings.py` включён `ssl_require=True`: база по `DATABASE_URL` должна принимать SSL-соединения. |

## Тесты

Файл `rsvp/tests.py` пока пустой, тестов в проекте нет. Команда ниже запустится, но проверять нечего:

```bash
python manage.py test
```