#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Очищення попередніх запусків VAmPI...${NC}"
docker-compose down -v

echo -e "${YELLOW}Запуск VAmPI у фоновому режимі...${NC}"
docker-compose up -d

echo -e "${YELLOW}Очікування ініціалізації API...${NC}"

ATTEMPTS=0
MAX_ATTEMPTS=20
IS_HEALTHY=false

# Чекаємо, поки Docker healthcheck не скаже, що API піднялося
while [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    STATUS=$(docker inspect --format='{{json .State.Health.Status}}' vampi_target 2>/dev/null)
    
    # Видаляємо лапки з результату для коректного порівняння
    STATUS=$(echo "$STATUS" | tr -d '"')
    
    if [ "$STATUS" == "healthy" ]; then
        IS_HEALTHY=true
        break
    fi
    
    sleep 2
    ATTEMPTS=$((ATTEMPTS+1))
done

if [ "$IS_HEALTHY" = true ]; then
    echo -e "${GREEN}Контейнер готовий. Ініціалізація бази даних через API...${NC}"
    
    # Робимо запит до ендпоінту createdb і записуємо HTTP статус-код
    # Використовуємо curl, який зазвичай є на будь-якому Linux
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/createdb)
    
    # VAmPI зазвичай повертає 200 OK при успішному створенні
    if [ "$HTTP_STATUS" -eq 200 ] || [ "$HTTP_STATUS" -eq 302 ] || [ "$HTTP_STATUS" -eq 301 ]; then
        echo -e "${GREEN}Базу даних успішно ініціалізовано! (HTTP $HTTP_STATUS)${NC}"
        echo -e "API доступне за адресою: ${GREEN}http://localhost:5000${NC}"
        exit 0
    else
        echo -e "${RED}Помилка під час звернення до /createdb. Код відповіді: $HTTP_STATUS${NC}"
        exit 1
    fi
else
    echo -e "${RED}Помилка: VAmPI не зміг успішно запуститися (status: $STATUS).${NC}"
    docker logs vampi_target
    exit 1
fi