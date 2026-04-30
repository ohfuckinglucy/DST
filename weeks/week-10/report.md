# Отчет по Docker

В этом месте вам необходимо:
- Размер образа
- Количество слоёв
- Команды сборки/запуска
```
week10-app   heavy     cdc6d7abb921   18 seconds ago   1.11GB ## Тяжелый образ 18 слоев (docker history week10-app:heavy)

week10-app   latest    16a3a3c4ed01   6 seconds ago   125MB ## 18 очень легкий образ

docker build -t week10-app:heavy .

docker run -p 8278:8278 week10-app:heavy
```

## Информация о слоях (Layers)
В данном образе получилось 18 слоев. 
- Основные слои формируются базовым образом python-slim и Debian.
- Новые слои в нашем Dockerfile создают команды WORKDIR, COPY и RUN.
- Использование Multi-stage сборки позволяет объединить результаты работы промежуточных слоев, не перенося лишний мусор в финальный образ.
