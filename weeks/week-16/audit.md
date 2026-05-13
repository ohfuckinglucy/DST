# Security Audit Report: devices-s19

**Student:** s19
**Group:** 331
**Project Code:** devices-s19

## 1. Чек-лист OWASP Top 10

| ID | Уязвимость | Статус | Комментарий |
|----|------------|--------|-------------|
| 1  | **Broken Access Control** | Risk | В эндпоинтах `/api/devices` нет проверки принадлежности ресурса пользователю. |
| 2  | **Cryptographic Failures** | Pass | Пароли хэшируются (bcrypt) перед сохранением. |
| 3  | **Injection** | Pass | Pydantic валидирует все входные данные, ORM защищает от SQL-инъекций. |
| 4  | **Insecure Design** | Risk | Нет rate limiting — API уязвим для brute-force атак. |
| 5  | **Security Misconfiguration** | Risk | `SECRET_KEY` и `DATABASE_URL` жестко закодированы в `main.py`. |
| 6  | **Vulnerable Components** | Pass | Все зависимости зафиксированы по версиям в `requirements.txt`. |
| 7  | **Authentication Failures** | Risk | JWT токены не имеют expires и refresh механизма. |
| 8  | **Software & Data Integrity** | Pass | CI/CD собирает Docker-образ в изолированной среде. |
| 9  | **Security Logging** | Risk | Нет логов неудачных аутентификаций и доступа к ресурсам. |
| 10 | **SSRF** | Pass | Функционал загрузки по URL отсутствует. |

## 2. Найденные проблемы и рекомендации

### Finding 1: Hardcoded Secrets в коде
- **Severity:** High
- **Location:** `weeks/week-11/app/main.py`, `docker-compose.yml`
- **Description:** Параметры подключения к БД (`DB_PASSWORD=items_pass`) хранятся в открытом виде в docker-compose.yml.
- **Impact:** При публикации репозитория злоумышленник получит доступ к продакшен-базе.
- **Remediation:** Использовать `.env` файл и переменные окружения. Добавить `.env` в `.gitignore`.

### Finding 2: Отсутствие Rate Limiting
- **Severity:** Medium
- **Location:** `weeks/week-11/infra/nginx.conf` (отсутствует)
- **Description:** API Gateway (Nginx) не имеет ограничений на количество запросов с одного IP.
- **Impact:** Возможен brute-force паролей и DDoS атак.
- **Remediation:** Добавить в nginx.conf:
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
limit_req zone=api burst=50 nodelay;
```

### Finding 3: Отсутствие проверки прав доступа
- **Severity:** Medium
- **Location:** `weeks/week-11/app/main.py`
- **Description:** Любой пользователь может получить/изменить/удалить любой ресурс без проверки владельца.
- **Impact:** Утечка данных других пользователей.
- **Remediation:** Добавить middleware аутентификации и проверку `resource.owner_id == current_user.id`.
