#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Зупинка та видалення контейнера VAmPI...${NC}"

# Вимикаємо сервіси і видаляємо volumes (-v), щоб очистити стан БД
docker-compose down -v

echo -e "${GREEN}Тестове середовище успішно вимкнено та очищено!${NC}"