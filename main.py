import pygame
import sys
import shutil
import os
import time
import sqlite3
import random
from datetime import datetime

# Пути к данным Chrome
chrome_data = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data')
history_path = os.path.join(chrome_data, 'Default', 'History')

pygame.init()

# Настройки дисплея
WIDTH, HEIGHT = 360, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fuck yandex")

# Цвета (RGB)
BG = (30, 40, 40)
buttons = (70, 70, 90)
hover = (100, 100, 120)
text = (255, 255, 255)
warning = (200, 50, 50)
success = (50, 200, 50)
info = (100, 150, 255)

# Шрифты
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# BUTTons
class Button:
    def __init__(self, x, y, width, height, text, color=buttons, hover_color=hover):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (50, 50, 70), self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, text)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

# Основные кнопки
buttons = [
    Button(WIDTH//2 - 100, 150, 200, 50, "Delete Data"),
    Button(WIDTH//2 - 100, 220, 200, 50, "History Spam"),
    Button(WIDTH//2 - 100, 350, 200, 50, "Quit")
]

# Сюда свйтов навписывай побольше всяких 
SITES_TO_ADD = [
    "https://google.com",
    "https://youtube.com",
    "https://github.com",
    "https://stackoverflow.com",
    "https://python.org"
]

# Функция для отображения сообщений
def show_message(title, message, color=text):
    message_window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title)
    
    lines = []
    words = message.split(' ')
    current_line = ''
    
    for word in words:
        test_line = current_line + word + ' '
        if small_font.size(test_line)[0] < WIDTH - 40:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    if current_line:
        lines.append(current_line)
    
    close_button = Button(WIDTH//2 - 50, HEIGHT - 80, 100, 40, "OK")
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        message_window.fill(BG)
        
        title_surface = font.render(title, True, color)
        message_window.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 30))
        
        for i, line in enumerate(lines):
            line_surface = small_font.render(line, True, text)
            message_window.blit(line_surface, (20, 100 + i * 30))
        
        close_button.check_hover(mouse_pos)
        close_button.draw(message_window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.rect.collidepoint(mouse_pos):
                    running = False
        
        pygame.display.flip()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fuck yandex")

# Функция подтверждения действия
def confirm_action(message):
    confirm_window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Подтверждение")
    
    yes_button = Button(WIDTH//2 - 120, HEIGHT - 150, 100, 40, "Да", warning, (220, 80, 80))
    no_button = Button(WIDTH//2 + 20, HEIGHT - 150, 100, 40, "Нет")
    
    running = True
    result = False
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        confirm_window.fill(BG)
        
        title_surface = font.render("Подтвердите действие", True, warning)
        confirm_window.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 30))
        
        lines = []
        words = message.split(' ')
        current_line = ''
        
        for word in words:
            test_line = current_line + word + ' '
            if small_font.size(test_line)[0] < WIDTH - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        if current_line:
            lines.append(current_line)
        
        for i, line in enumerate(lines):
            line_surface = small_font.render(line, True, text)
            confirm_window.blit(line_surface, (20, 100 + i * 30))
        
        yes_button.check_hover(mouse_pos)
        no_button.check_hover(mouse_pos)
        yes_button.draw(confirm_window)
        no_button.draw(confirm_window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.rect.collidepoint(mouse_pos):
                    result = True
                    running = False
                elif no_button.rect.collidepoint(mouse_pos):
                    result = False
                    running = False
        
        pygame.display.flip()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fuck yandex")
    
    return result

# Функция добавления сайтов в историю
def add_sites_to_history():
    # Настройки случайных промежутков (в минутах)
    min_gap = 5
    max_gap = 180
    
    if not confirm_action(f"Добавить сайты в историю браузера?"):
        return
    
    try:
        # Проверяем, закрыт ли Chrome
        if os.path.exists(history_path + "-wal"):
            show_message("Ошибка", "Закройте Chrome перед изменением истории!")
            return
        
        # Создаем резервную копию
        backup_path = history_path + ".backup_" + time.strftime("%Y%m%d_%H%M%S")
        shutil.copy2(history_path, backup_path)
        
        # Подключаемся к базе данных
        conn = sqlite3.connect(history_path)
        cursor = conn.cursor()
        
        # Получаем максимальные ID
        cursor.execute("SELECT MAX(id) FROM urls")
        max_url_id = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT MAX(id) FROM visits")
        max_visit_id = cursor.fetchone()[0] or 0
        
        # Начальное время
        visit_time = int((datetime.now() - datetime(1601, 1, 1)).total_seconds() * 1000000)
        
        for url in SITES_TO_ADD:
            # Добавляем URL
            max_url_id += 1
            cursor.execute(
                "INSERT INTO urls (id, url, title, visit_count, typed_count, last_visit_time, hidden) "
                "VALUES (?, ?, ?, 1, 0, ?, 0)",
                (max_url_id, url, "", visit_time)
            )
            
            # Добавляем посещение
            max_visit_id += 1
            cursor.execute(
                "INSERT INTO visits (id, url, visit_time, from_visit, transition, segment_id) "
                "VALUES (?, ?, ?, 0, 805306368, 0)",
                (max_visit_id, max_url_id, visit_time)
            )
            
            # Генерируем случайный промежуток и добавляем к времени
            random_gap = random.randint(min_gap, max_gap)
            visit_time += random_gap * 60 * 1000000
        
        conn.commit()
        conn.close()
        
        show_message("Успех", f"Сайты успешно добавлены!", success)
        
    except Exception as e:
        show_message("Ошибка", f"Не удалось изменить историю: {str(e)}")

# Функция удаления данных Chrome
def delete_chrome_data():
    if confirm_action("Вы уверены, что хотите удалить все данные Chrome? Это действие нельзя отменить!"):
        try:
            if os.path.exists(chrome_data):
                shutil.rmtree(chrome_data)
                show_message("Успех", "Данные Chrome были успешно удалены!", success)
            else:
                show_message("Ошибка", "Папка с данными Chrome не найдена.")
        except Exception as e:
            show_message("Ошибка", f"Не удалось удалить данные: {str(e)}")

# Главный цикл
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(BG)
    
    # Заголовок
    title = font.render("BROWSER-HISTORY-SPAM", True, text)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.rect.collidepoint(mouse_pos):
                    if button.text == "Quit":
                        running = False
                    elif button.text == "Delete Data":
                        delete_chrome_data()
                    elif button.text == "History Spam":
                        add_sites_to_history()

    # Отрисовка кнопок
    for button in buttons:
        button.check_hover(mouse_pos)
        button.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
