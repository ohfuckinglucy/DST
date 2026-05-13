# Security Checklist: devices-s19

## OWASP Top 10 Audit

| ID | Уязвимость | Статус | Комментарий |
|----|------------|--------|-------------|
| 1  | Broken Access Control | Risk | Отсутствует проверка владельца ресурса. Любой пользователь может получить/изменить любой device. |
| 2  | Cryptographic Failures | Pass | Пароли хэшируются, данные передаются по HTTPS (в production). |
| 3  | Injection | Pass | Входные данные валидируются через Pydantic. SQL-инъекции невозможны. |
| 4  | Insecure Design | Risk | Rate limiting не реализован. Возможен brute-force. |
| 5  | Security Misconfiguration | Risk | Секреты в коде (`.env` не добавлен в `.gitignore`). |
| 6  | Vulnerable Components | Pass | Зависимости фиксированы в `requirements.txt`. |
| 7  | Authentication Failures | Risk | JWT-токены не имеют срока истечения. |
| 8  | Software & Data Integrity | Pass | CI/CD собирает образ изолированно. |
| 9  | Security Logging | Risk | Отсутствует логирование неудачных попыток доступа. |
| 10 | SSRF | Pass | Функционал загрузки по URL отсутствует. |
