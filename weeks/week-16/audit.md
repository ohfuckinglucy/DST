# Security Audit Report: devices-s19

**Student:** s19  
**Group:** 331  
**Project Code:** devices-s19  

## 1. Чек-лист OWASP Top 10

| ID | Уязвимость | Статус | Комментарий |
|----|------------|--------|-------------|
| 1  | **Broken Access Control** | Risk | Необходимо проверять права доступа пользователя к ресурсу `/api/devices`. |
| 2  | **Cryptographic Failures** | Pass | Пароли хэшируются перед сохранением в БД. |
| 3  | **Injection** | Pass | Используется ORM, что защищает от SQL-инъекций. Входные данные валидируются. |
| 4  | **Insecure Design** | Risk | Рекомендуется добавить Rate Limiting для защиты от brute-force. |
| 5  | **Security Misconfiguration** | Risk | Необходимо убедиться, что все секреты вынесены в переменные окружения (.env). |
| 6  | **Vulnerable Components** | Pass | Зависимости регулярно обновляются. |
| 7  | **Authentication Failures** | Risk | JWT токены должны иметь ограниченное время жизни. |
| 8  | **Software & Data Integrity** | Pass | Сборка происходит в изолированном CI/CD окружении. |
| 9  | **Security Logging** | Risk | Необходимо логировать попытки несанкционированного доступа. |
| 10 | **SSRF** | Pass | Функционал загрузки по URL отсутствует. |

## 2. Найденные проблемы и рекомендации

### 1. Риск утечки секретов (Hardcoded Secrets)
**Severity:** High  
**Description:** В учебных целях некоторые конфигурации могут храниться в коде. В продакшене это недопустимо.  
**Remediation:** Использовать переменные окружения (`.env`) для хранения `SECRET_KEY`, `DATABASE_URL` и других чувствительных данных. Добавить `.env` в `.gitignore`.

### 2. Контроль доступа (Broken Access Control)
**Severity:** Medium  
**Description:** Эндпоинты API должны проверять, принадлежит ли запрашиваемый ресурс (`devices`) текущему пользователю.  
**Remediation:** Добавить middleware или проверку в контроллере: `if device.owner_id != current_user.id: raise 403`.

### 3. Отсутствие лимитов запросов (Rate Limiting)
**Severity:** Medium  
**Description:** API открыт для бесконечного числа запросов, что позволяет проводить атаки перебором.  
**Remediation:** Внедрить ограничение на количество запросов с одного IP (например, 100 req/min).