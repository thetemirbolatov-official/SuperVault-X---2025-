"""
SUPER VAULT X - Мегашифрователь файлов с паролями из 10000 строк
Версия: 5.0 MEGA ULTRA PRO
Автор: thetemirbolatov © 2025
Лицензия: MIT
GitHub: https://github.com/ftoop17
"""

import os
import sys
import json
import base64
import time
import random
import string
import hashlib
import secrets
from datetime import datetime
from pathlib import Path
import threading
import webbrowser
import subprocess
import zipfile

# Криптография
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# Графический интерфейс (опционально)
GUI_AVAILABLE = False
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    GUI_AVAILABLE = True
except ImportError:
    pass

# ============================================================================
# ЯДРО ШИФРОВАНИЯ MEGA-PRO
# ============================================================================

class SuperVaultX:
    """
    Супер-шифровальщик файлов с паролями из 10000 строк
    Использует AES-256 + PBKDF2 + HMAC
    """
    
    VERSION = "5.0.0"
    AUTHOR = "thetemirbolatov"
    YEAR = 2025
    
    def __init__(self, mega_password_lines=10000):
        """
        Инициализация супер-шифровальщика
        
        Args:
            mega_password_lines: Количество строк в мега-пароле (по умолчанию 10000)
        """
        self.MAGIC_HEADER = b"SUPER_VAULT_X_V5\x00"
        self.HEADER_SIZE = 2048  # Большой заголовок для метаданных
        self.PASSWORD_LINES = mega_password_lines
        self.ENCRYPTION_ALGO = "AES-256-CBC-PBKDF2-HMAC"
        self.MIN_USER_WORDS = 1
        
        # Словари для генерации пароля
        self.DICTIONARIES = {
            "tech_words": [
                "квантовый", "шифр", "алгоритм", "протокол", "нейронный",
                "биометрический", "защита", "безопасность", "крипто",
                "хэш", "блокчейн", "энтропия", "шифрование", "дешифровка",
                "аутентификация", "авторизация", "инкапсуляция", "полиморфизм"
            ],
            "nature_words": [
                "огонь", "вода", "земля", "воздух", "металл",
                "дерево", "звезда", "планета", "галактика", "космос",
                "океан", "вулкан", "тайфун", "торнадо", "землетрясение"
            ],
            "power_words": [
                "сила", "мощь", "энергия", "поток", "заряд",
                "импульс", "волна", "вибрация", "резонанс", "гравитация",
                "магнетизм", "электричество", "плазма", "сингулярность"
            ],
            "secure_words": [
                "тайна", "секрет", "пароль", "ключ", "замок",
                "сейф", "хранилище", "убежище", "крепость", "бункер",
                "броня", "щит", "доспех", "лабиринт", "головоломка"
            ],
            "mythology_words": [
                "дракон", "феникс", "единорог", "грифон", "кентавр",
                "пегас", "сатир", "циклоп", "гарпия", "минотавр",
                "сирена", "василиск", "гидра", "химера", "левиафан"
            ],
            "science_words": [
                "атом", "молекула", "ген", "клетка", "вирус",
                "бактерия", "фермент", "гормон", "нейрон", "синапс",
                "кварк", "бозон", "фермион", "лептон", "глюон"
            ]
        }
        
        # Спецсимволы для усиления пароля
        self.SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        
        # Логирование
        self.log_messages = []
        self.operation_start_time = None
        
    def log(self, message, level="INFO"):
        """Логирование операций"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.log_messages.append(log_entry)
        print(log_entry)
        
    def create_mega_password(self, user_words, user_dates=None, personal_info=None, 
                            use_dictionaries=True, add_timestamps=True):
        """
        Создание мега-пароля из N строк
        
        Args:
            user_words: Список слов от пользователя
            user_dates: Список дат от пользователя
            personal_info: Словарь с персональной информацией
            use_dictionaries: Использовать встроенные словари
            add_timestamps: Добавлять временные метки
            
        Returns:
            Кортеж (пароль_текст, хэш_пароля, статистика)
        """
        self.log(f"Создание мега-пароля из {self.PASSWORD_LINES} строк...")
        
        if not user_words or len(user_words) < self.MIN_USER_WORDS:
            raise ValueError(f"Нужно минимум {self.MIN_USER_WORDS} слово от пользователя")
        
        user_words = [str(w).strip() for w in user_words if str(w).strip()]
        if user_dates:
            user_dates = [str(d).strip() for d in user_dates if str(d).strip()]
        
        password_lines = []
        stats = {
            "total_lines": self.PASSWORD_LINES,
            "user_words": len(user_words),
            "user_dates": len(user_dates) if user_dates else 0,
            "dictionary_words_used": 0,
            "special_chars_used": 0,
            "timestamps_added": 0
        }
        
        # Генерация пароля
        for i in range(self.PASSWORD_LINES):
            line_parts = []
            
            # 1. Слово пользователя (циклически)
            word_idx = i % len(user_words)
            line_parts.append(user_words[word_idx])
            
            # 2. Дата пользователя (каждые 3 строки)
            if user_dates and i % 3 == 0:
                date_idx = i % len(user_dates)
                line_parts.append(user_dates[date_idx])
                stats["user_dates"] = len(user_dates)
            
            # 3. Слова из словарей (случайно)
            if use_dictionaries:
                for dict_name, words in self.DICTIONARIES.items():
                    if random.random() > 0.6:  # 40% вероятность
                        line_parts.append(random.choice(words))
                        stats["dictionary_words_used"] += 1
            
            # 4. Персональная информация
            if personal_info:
                for key, value in personal_info.items():
                    if random.random() > 0.8:  # 20% вероятность
                        line_parts.append(f"{key}_{value}")
            
            # 5. Случайная строка (8-32 символа)
            random_len = random.randint(12, 32)
            random_part = ''.join(
                random.choice(string.ascii_letters + string.digits + self.SPECIAL_CHARS)
                for _ in range(random_len)
            )
            line_parts.append(random_part)
            stats["special_chars_used"] += 1
            
            # 6. Математические выражения (иногда)
            if random.random() > 0.7:
                math_ops = ["+", "-", "*", "/", "=", "≈", "≠", ">", "<"]
                num1 = random.randint(1, 9999)
                num2 = random.randint(1, 9999)
                op = random.choice(math_ops)
                math_expr = f"{num1}{op}{num2}"
                line_parts.append(math_expr)
            
            # 7. Шестнадцатеричные числа
            if random.random() > 0.5:
                hex_num = secrets.token_hex(random.randint(2, 8))
                line_parts.append(f"0x{hex_num}")
            
            # Сборка строки
            separator = random.choice(["_", "-", ".", "|", ":", "#", "~", "•", "→", "⇨"])
            line = separator.join(line_parts)
            
            # Добавление номера строки и временной метки
            if add_timestamps:
                timestamp = int(time.time() * 1000000) + i  # Микросекунды
                nano_time = secrets.randbits(64)
                full_line = f"L{i+1:06d}_T{timestamp}_N{nano_time}_{line}"
                stats["timestamps_added"] += 1
            else:
                full_line = f"L{i+1:06d}_{line}"
            
            password_lines.append(full_line)
            
            # Прогресс
            if (i + 1) % 1000 == 0:
                self.log(f"Сгенерировано строк: {i + 1}/{self.PASSWORD_LINES}")
        
        password_text = "\n".join(password_lines)
        
        # Мульти-хэширование для безопасности
        sha512_hash = hashlib.sha512(password_text.encode('utf-8')).hexdigest()
        blake2b_hash = hashlib.blake2b(password_text.encode('utf-8')).hexdigest()
        
        # Комбинированный хэш
        combined_hash = hashlib.sha3_512(
            (sha512_hash + blake2b_hash).encode('utf-8')
        ).hexdigest()
        
        self.log(f"Мега-пароль создан! Всего символов: {len(password_text):,}")
        self.log(f"Статистика: {stats}")
        
        return password_text, combined_hash, stats
    
    def read_password_from_file(self, password_file):
        """
        Чтение пароля из файла
        
        Args:
            password_file: Путь к файлу с паролем
            
        Returns:
            Текст пароля или None в случае ошибки
        """
        try:
            if not os.path.exists(password_file):
                self.log(f"Файл пароля не существует: {password_file}", "ERROR")
                return None
            
            with open(password_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Упрощенный парсинг
            lines = content.split('\n')
            
            # Ищем маркер начала пароля
            password_lines = []
            found_marker = False
            
            for line in lines:
                # Ищем маркер начала пароля
                if "🚀 START OF PASSWORD" in line or "START OF PASSWORD" in line:
                    found_marker = True
                    continue
                
                # Если нашли маркер, собираем строки
                if found_marker:
                    # Пропускаем разделители и пустые строки в начале
                    if line.strip() and not line.startswith("=" * 20):
                        # Проверяем, не является ли это концом пароля
                        if "END OF PASSWORD" in line:
                            break
                        password_lines.append(line)
            
            # Если не нашли маркер, пробуем другой подход
            if not password_lines:
                # Ищем строки, похожие на пароль (содержат L000001_T и т.д.)
                for line in lines:
                    if "L000001_" in line and len(line) > 20:
                        password_lines.append(line)
            
            # Если все еще нет, берем все строки после определенной точки
            if not password_lines:
                # Ищем любые строки, которые выглядят как пароль
                for i, line in enumerate(lines):
                    if len(line) > 10 and not line.startswith("File:") and not line.startswith("Size:") and not line.startswith("Created:"):
                        # Проверяем, содержит ли строка типичные элементы пароля
                        if any(marker in line for marker in ["_T", "_N", "L0", "|", ":", "#"]):
                            password_lines = lines[i:]
                            break
            
            # Объединяем строки
            password = '\n'.join(password_lines).strip()
            
            # Убираем конечные разделители
            while password.endswith("=" * 80):
                password = password[:-(80)].strip()
            
            if not password:
                self.log("Не удалось найти пароль в файле", "ERROR")
                return None
            
            # Проверяем количество строк
            line_count = len(password.split('\n'))
            self.log(f"Прочитан пароль из {line_count} строк")
            
            if line_count < 100:
                self.log(f"Внимание: пароль содержит только {line_count} строк (ожидается 10000)", "WARNING")
            
            return password
            
        except Exception as e:
            self.log(f"Ошибка чтения пароля: {str(e)}", "ERROR")
            return None
    
    def save_password_to_file(self, password_text, original_filename, stats=None):
        """
        Сохранение пароля в файл
        
        Args:
            password_text: Текст пароля
            original_filename: Исходный файл
            stats: Статистика генерации
            
        Returns:
            Путь к сохраненному файлу
        """
        original_path = Path(original_filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")  # С микросекундами
        
        # Имя файла с паролем
        password_filename = f"SUPER_PASSWORD_{original_path.stem}_{timestamp}.txt"
        password_path = original_path.parent / password_filename
        
        # Метаданные
        file_size = os.path.getsize(original_filename) if os.path.exists(original_filename) else 0
        
        with open(password_path, 'w', encoding='utf-8') as f:
            # Более простой формат без рамок, чтобы легче было читать
            f.write("=" * 80 + "\n")
            f.write("SUPER PASSWORD FILE\n")
            f.write("=" * 80 + "\n")
            f.write(f"File: {original_path.name}\n")
            f.write(f"Size: {file_size:,} bytes\n")
            f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}\n")
            f.write(f"Author: {self.AUTHOR} © {self.YEAR}\n")
            f.write(f"Version: {self.VERSION}\n")
            f.write("=" * 80 + "\n")
            
            # Предупреждения
            f.write("\n⚠️ IMPORTANT WARNINGS:\n")
            warnings = [
                "1. SAVE THIS FILE IN A SECURE PLACE!",
                "2. Without this file, recovery is IMPOSSIBLE!",
                "3. Never store the password with the encrypted file!",
                "4. Make multiple copies on different media!",
                "5. Password consists of 10000 unique lines!",
                "6. Each line contains a timestamp and unique ID!",
                "",
                "🚨 LOST PASSWORD = LOST DATA 🚨"
            ]
            
            for warning in warnings:
                f.write(f"{warning}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            
            # Статистика
            if stats:
                f.write("\n📊 PASSWORD GENERATION STATISTICS:\n")
                for key, value in stats.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n" + "=" * 80 + "\n")
            
            # Маркер начала пароля
            f.write("\n🚀 START OF PASSWORD 🚀\n")
            f.write("=" * 80 + "\n\n")
            
            # Сам пароль - ВАЖНО: без дополнительных символов!
            f.write(password_text)
            
            # Конец файла
            f.write(f"\n\n{'=' * 80}\n")
            f.write(f"🎯 END OF PASSWORD - {self.PASSWORD_LINES} LINES GENERATED 🎯\n")
            f.write(f"{'=' * 80}\n")
        
        self.log(f"Файл с паролем сохранен: {password_path}")
        return str(password_path)
    
    def calculate_file_hash(self, filepath, algorithm='sha3_512'):
        """Расчет хэша файла"""
        if not os.path.exists(filepath):
            return "FILE_NOT_FOUND"
        
        hasher = hashlib.new(algorithm)
        try:
            with open(filepath, 'rb') as f:
                # Читаем большими блоками для больших файлов
                for chunk in iter(lambda: f.read(65536), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return f"ERROR_{str(e)}"
    
    def encrypt_file(self, input_file, password_text, delete_original=True, 
                    secure_delete_passes=7, compress_before_encrypt=True):
        """
        Шифрование файла
        
        Args:
            input_file: Путь к файлу для шифрования
            password_text: Мега-пароль (текст)
            delete_original: Удалить оригинал после шифрования
            secure_delete_passes: Количество проходов безопасного удаления
            compress_before_encrypt: Сжать перед шифрованием
            
        Returns:
            Словарь с результатами
        """
        self.operation_start_time = time.time()
        self.log(f"НАЧАЛО ШИФРОВАНИЯ: {input_file}")
        
        try:
            # Проверки
            if not CRYPTO_AVAILABLE:
                return {
                    'success': False,
                    'error': 'Криптографические библиотеки не установлены. Установите: pip install pycryptodome'
                }
            
            if not os.path.exists(input_file):
                return {'success': False, 'error': 'Файл не существует'}
            
            # Чтение исходного файла
            with open(input_file, 'rb') as f:
                original_data = f.read()
            
            original_size = len(original_data)
            self.log(f"Размер файла: {original_size:,} байт")
            
            if original_size == 0:
                return {'success': False, 'error': 'Файл пустой'}
            
            # Сжатие (опционально)
            if compress_before_encrypt and original_size > 1024:
                try:
                    import zlib
                    compressed_data = zlib.compress(original_data, level=9)
                    compression_ratio = len(compressed_data) / original_size if original_size > 0 else 1
                    self.log(f"Сжатие: {original_size:,} → {len(compressed_data):,} байт ({compression_ratio:.2%})")
                    data_to_encrypt = compressed_data
                    was_compressed = True
                except:
                    data_to_encrypt = original_data
                    was_compressed = False
                    compression_ratio = 1.0
            else:
                data_to_encrypt = original_data
                was_compressed = False
                compression_ratio = 1.0
            
            # Генерация криптографических параметров
            salt = secrets.token_bytes(32)  # 256 бит соли
            iv = get_random_bytes(16)       # 128 бит IV
            
            # Создание ключа через PBKDF2
            key = hashlib.pbkdf2_hmac(
                'sha512',
                password_text.encode('utf-8'),
                salt,
                100000,  # Много итераций для безопасности
                dklen=32  # 256 бит
            )
            
            # Шифрование AES-256 CBC
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_data = pad(data_to_encrypt, AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            
            # HMAC для аутентификации
            hmac_tag = hashlib.sha256(
                encrypted_data + salt + iv + key
            ).digest()
            
            # Создание заголовка
            header = {
                'magic': self.MAGIC_HEADER.hex(),
                'version': self.VERSION,
                'algorithm': self.ENCRYPTION_ALGO,
                'original_size': original_size,
                'encrypted_size': len(encrypted_data),
                'salt': base64.b64encode(salt).decode('ascii'),
                'iv': base64.b64encode(iv).decode('ascii'),
                'hmac_tag': base64.b64encode(hmac_tag).decode('ascii'),
                'password_hash': hashlib.sha3_512(password_text.encode('utf-8')).hexdigest(),
                'timestamp': datetime.now().isoformat(),
                'original_name': Path(input_file).name,
                'original_path': str(Path(input_file).absolute()),
                'original_hash': self.calculate_file_hash(input_file),
                'was_compressed': was_compressed,
                'compression_ratio': compression_ratio if was_compressed else 1.0,
                'secure_delete_passes': secure_delete_passes,
                'author': self.AUTHOR,
                'year': self.YEAR
            }
            
            # Сериализация заголовка
            header_json = json.dumps(header, ensure_ascii=False, indent=2)
            header_encoded = header_json.encode('utf-8')
            
            # Проверка размера заголовка
            if len(header_encoded) > self.HEADER_SIZE:
                return {'success': False, 'error': 'Заголовок слишком большой'}
            
            # Дополнение заголовка
            padded_header = header_encoded.ljust(self.HEADER_SIZE, b'\x00')
            
            # Сборка финального файла
            final_data = padded_header + hmac_tag + encrypted_data
            
            # Сохранение зашифрованного файла
            original_path = Path(input_file)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            encrypted_filename = f"ENCRYPTED_{original_path.stem}_{timestamp}.svx"
            encrypted_path = original_path.parent / encrypted_filename
            
            with open(encrypted_path, 'wb') as f:
                f.write(final_data)
            
            encrypted_size = len(final_data)
            encryption_ratio = encrypted_size / original_size if original_size > 0 else 1
            
            self.log(f"Файл зашифрован: {encrypted_path}")
            self.log(f"Итоговый размер: {encrypted_size:,} байт (x{encryption_ratio:.2f})")
            
            # Безопасное удаление оригинала
            if delete_original:
                self.log(f"Безопасное удаление оригинала ({secure_delete_passes} проходов)...")
                self.secure_delete_file(input_file, passes=secure_delete_passes)
            
            # Расчет времени
            elapsed_time = time.time() - self.operation_start_time
            
            result = {
                'success': True,
                'encrypted_file': str(encrypted_path),
                'password_file': None,  # Будет заполнено позже
                'original_size': original_size,
                'encrypted_size': encrypted_size,
                'compression_ratio': compression_ratio if was_compressed else 1.0,
                'encryption_ratio': encryption_ratio,
                'was_compressed': was_compressed,
                'elapsed_time': elapsed_time,
                'speed_mbps': (original_size / elapsed_time / 1024 / 1024) if elapsed_time > 0 else 0,
                'header_info': {
                    'algorithm': header['algorithm'],
                    'timestamp': header['timestamp'],
                    'hash': header['password_hash'][:32] + '...'
                }
            }
            
            self.log(f"Шифрование завершено за {elapsed_time:.2f} секунд")
            return result
            
        except Exception as e:
            self.log(f"Ошибка шифрования: {str(e)}", "ERROR")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Ошибка шифрования: {str(e)}'
            }
    
    def decrypt_file(self, encrypted_file, password_text, verify_integrity=True):
        """
        Дешифрование файла
        
        Args:
            encrypted_file: Зашифрованный файл (.svx)
            password_text: Мега-пароль
            verify_integrity: Проверять целостность
            
        Returns:
            Словарь с результатами
        """
        self.operation_start_time = time.time()
        self.log(f"НАЧАЛО ДЕШИФРОВАНИЯ: {encrypted_file}")
        
        try:
            if not CRYPTO_AVAILABLE:
                return {
                    'success': False,
                    'error': 'Криптографические библиотеки не установлены'
                }
            
            if not os.path.exists(encrypted_file):
                return {'success': False, 'error': 'Файл не существует'}
            
            # Чтение зашифрованного файла
            with open(encrypted_file, 'rb') as f:
                file_data = f.read()
            
            if len(file_data) < self.HEADER_SIZE + 32 + 16:
                return {'success': False, 'error': 'Файл поврежден или не является .svx файлом'}
            
            # Извлечение заголовка
            header_data = file_data[:self.HEADER_SIZE]
            null_pos = header_data.find(b'\x00')
            if null_pos == -1:
                null_pos = len(header_data)
            
            header_json = header_data[:null_pos]
            
            try:
                header = json.loads(header_json.decode('utf-8'))
            except json.JSONDecodeError as e:
                return {'success': False, 'error': f'Неверный формат заголовка: {str(e)}'}
            
            # Проверка магического числа
            if 'magic' not in header or header.get('magic') != self.MAGIC_HEADER.hex():
                return {'success': False, 'error': 'Неверный формат файла .svx'}
            
            # Проверка хэша пароля
            password_hash = hashlib.sha3_512(password_text.encode('utf-8')).hexdigest()
            if header.get('password_hash') != password_hash:
                return {'success': False, 'error': 'Неверный пароль'}
            
            # Извлечение параметров
            salt = base64.b64decode(header['salt'])
            iv = base64.b64decode(header['iv'])
            stored_hmac = base64.b64decode(header['hmac_tag'])
            original_size = header['original_size']
            was_compressed = header.get('was_compressed', False)
            
            # Извлечение зашифрованных данных
            encrypted_data = file_data[self.HEADER_SIZE + 32:]  # Пропускаем HMAC
            
            # Проверка HMAC
            if verify_integrity:
                # Создание ключа для проверки
                key = hashlib.pbkdf2_hmac(
                    'sha512',
                    password_text.encode('utf-8'),
                    salt,
                    100000,
                    dklen=32
                )
                
                calculated_hmac = hashlib.sha256(
                    encrypted_data + salt + iv + key
                ).digest()
                
                if stored_hmac != calculated_hmac:
                    return {'success': False, 'error': 'Нарушена целостность файла'}
            
            # Дешифрование
            key = hashlib.pbkdf2_hmac(
                'sha512',
                password_text.encode('utf-8'),
                salt,
                100000,
                dklen=32
            )
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(encrypted_data)
            
            try:
                decrypted_data = unpad(decrypted_padded, AES.block_size)
            except ValueError as e:
                return {'success': False, 'error': f'Ошибка удаления padding: {str(e)}'}
            
            # Распаковка если нужно
            if was_compressed:
                try:
                    import zlib
                    decompressed_data = zlib.decompress(decrypted_data)
                    self.log(f"Данные распакованы: {len(decrypted_data):,} → {len(decompressed_data):,} байт")
                    decrypted_data = decompressed_data
                except Exception as e:
                    self.log(f"Ошибка распаковки: {str(e)}", "WARNING")
            
            # Проверка размера
            if len(decrypted_data) != original_size:
                self.log(f"Предупреждение: размер не совпадает ({len(decrypted_data)} != {original_size})", "WARNING")
            
            # Восстановление имени файла
            original_name = header.get('original_name', 'decrypted_file')
            original_path = Path(encrypted_file)
            
            # Создание имени для дешифрованного файла
            if 'ENCRYPTED_' in original_path.stem:
                base_name = original_path.stem.replace('ENCRYPTED_', 'DECRYPTED_')
            else:
                base_name = f"DECRYPTED_{original_path.stem}"
            
            # Добавление расширения если нужно
            if '.' not in base_name and '.' in original_name:
                ext = original_name.split('.')[-1]
                decrypted_filename = f"{base_name}.{ext}"
            else:
                decrypted_filename = base_name
            
            decrypted_path = original_path.parent / decrypted_filename
            
            # Сохранение дешифрованного файла
            with open(decrypted_path, 'wb') as f:
                f.write(decrypted_data)
            
            # Проверка хэша
            decrypted_hash = self.calculate_file_hash(str(decrypted_path))
            original_hash = header.get('original_hash', '')
            
            if original_hash and decrypted_hash != original_hash:
                self.log(f"Внимание: хэши не совпадают! Файл может быть поврежден.", "WARNING")
            
            elapsed_time = time.time() - self.operation_start_time
            
            result = {
                'success': True,
                'decrypted_file': str(decrypted_path),
                'original_size': original_size,
                'decrypted_size': len(decrypted_data),
                'hash_match': decrypted_hash == original_hash if original_hash else None,
                'original_hash': original_hash,
                'decrypted_hash': decrypted_hash,
                'elapsed_time': elapsed_time,
                'was_compressed': was_compressed,
                'header_info': {
                    'original_name': header.get('original_name'),
                    'timestamp': header.get('timestamp'),
                    'algorithm': header.get('algorithm')
                }
            }
            
            self.log(f"Дешифрование завершено за {elapsed_time:.2f} секунд")
            return result
            
        except Exception as e:
            self.log(f"Ошибка дешифрования: {str(e)}", "ERROR")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Ошибка дешифрования: {str(e)}'
            }
    
    def secure_delete_file(self, filepath, passes=7):
        """
        Безопасное удаление файла с перезаписью
        
        Args:
            filepath: Путь к файлу
            passes: Количество проходов перезаписи
        """
        if not os.path.exists(filepath):
            return
        
        file_size = os.path.getsize(filepath)
        
        patterns = [
            b'\x00' * file_size,  # Нули
            b'\xFF' * file_size,  # Единицы
            b'\xAA' * file_size,  # 10101010
            b'\x55' * file_size,  # 01010101
            secrets.token_bytes(file_size),  # Случайные данные
            b'\x00' * file_size,  # Еще нули
            secrets.token_bytes(file_size),  # Еще случайные данные
        ]
        
        try:
            for i in range(min(passes, len(patterns))):
                self.log(f"Проход безопасного удаления {i+1}/{passes}")
                
                with open(filepath, 'wb') as f:
                    if i < len(patterns):
                        f.write(patterns[i])
                    else:
                        f.write(secrets.token_bytes(file_size))
                
                f.flush()
                os.fsync(f.fileno())
            
            # Финальное удаление
            os.remove(filepath)
            self.log(f"Файл безопасно удален: {filepath}")
            
        except Exception as e:
            self.log(f"Ошибка безопасного удаления: {str(e)}", "WARNING")
            # Пробуем обычное удаление
            try:
                os.remove(filepath)
            except:
                pass
    
    def encrypt_directory(self, directory_path, password_text, 
                         include_subdirs=True, create_single_archive=True):
        """
        Шифрование всей директории
        
        Args:
            directory_path: Путь к директории
            password_text: Мега-пароль
            include_subdirs: Включать поддиректории
            create_single_archive: Создать единый архив
        
        Returns:
            Словарь с результатами
        """
        if not os.path.isdir(directory_path):
            return {'success': False, 'error': 'Не является директорией'}
        
        self.log(f"Шифрование директории: {directory_path}")
        
        # Создание архива если нужно
        if create_single_archive:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"ARCHIVE_{Path(directory_path).name}_{timestamp}"
            archive_path = Path(directory_path).parent / f"{archive_name}.zip"
            
            try:
                # Создание ZIP архива
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(directory_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, directory_path)
                            zipf.write(file_path, arcname)
                
                # Шифрование архива
                result = self.encrypt_file(str(archive_path), password_text)
                
                # Удаление временного архива
                if os.path.exists(archive_path):
                    os.remove(archive_path)
                
                return result
                
            except Exception as e:
                self.log(f"Ошибка создания архива: {str(e)}", "ERROR")
                return {'success': False, 'error': str(e)}
        
        else:
            # Шифрование каждого файла отдельно
            results = []
            total_size = 0
            
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    try:
                        result = self.encrypt_file(file_path, password_text)
                        results.append(result)
                        
                        if result['success']:
                            total_size += result.get('original_size', 0)
                        
                        self.log(f"Зашифрован: {file}")
                        
                    except Exception as e:
                        self.log(f"Ошибка шифрования {file}: {str(e)}", "ERROR")
            
            return {
                'success': True,
                'total_files': len(results),
                'successful': sum(1 for r in results if r.get('success')),
                'failed': sum(1 for r in results if not r.get('success')),
                'total_size': total_size,
                'individual_results': results
            }
    
    def verify_integrity(self, encrypted_file, password_text):
        """
        Проверка целостности зашифрованного файла
        
        Args:
            encrypted_file: Зашифрованный файл
            password_text: Пароль
        
        Returns:
            Словарь с результатами проверки
        """
        try:
            if not os.path.exists(encrypted_file):
                return {'valid': False, 'error': 'Файл не существует'}
            
            with open(encrypted_file, 'rb') as f:
                header_data = f.read(self.HEADER_SIZE)
            
            null_pos = header_data.find(b'\x00')
            if null_pos == -1:
                return {'valid': False, 'error': 'Неверный заголовок'}
            
            try:
                header = json.loads(header_data[:null_pos].decode('utf-8'))
            except:
                return {'valid': False, 'error': 'Неверный формат заголовка'}
            
            # Проверка магического числа
            if header.get('magic') != self.MAGIC_HEADER.hex():
                return {'valid': False, 'error': 'Неверный формат файла'}
            
            # Проверка хэша пароля
            password_hash = hashlib.sha3_512(password_text.encode('utf-8')).hexdigest()
            if header.get('password_hash') != password_hash:
                return {'valid': False, 'error': 'Неверный пароль'}
            
            # Проверка HMAC
            salt = base64.b64decode(header['salt'])
            iv = base64.b64decode(header['iv'])
            stored_hmac = base64.b64decode(header['hmac_tag'])
            
            with open(encrypted_file, 'rb') as f:
                f.seek(self.HEADER_SIZE + 32)  # Пропускаем HMAC
                encrypted_data = f.read()
            
            # Создание ключа для проверки
            key = hashlib.pbkdf2_hmac(
                'sha512',
                password_text.encode('utf-8'),
                salt,
                100000,
                dklen=32
            )
            
            calculated_hmac = hashlib.sha256(
                encrypted_data + salt + iv + key
            ).digest()
            
            hmac_valid = calculated_hmac == stored_hmac
            
            return {
                'valid': hmac_valid,
                'integrity_check': 'PASSED' if hmac_valid else 'FAILED',
                'file_info': {
                    'original_name': header.get('original_name'),
                    'original_size': header.get('original_size'),
                    'encrypted_size': os.path.getsize(encrypted_file),
                    'algorithm': header.get('algorithm'),
                    'timestamp': header.get('timestamp'),
                    'was_compressed': header.get('was_compressed', False)
                },
                'password_hash_match': True
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Ошибка проверки: {str(e)}'
            }

# ============================================================================
# ГРАФИЧЕСКИЙ ИНТЕРФЕЙС
# ============================================================================

if GUI_AVAILABLE:
    class SuperVaultGUI:
        """Графический интерфейс Super Vault X"""
        
        def __init__(self):
            self.root = tk.Tk()
            self.vault = SuperVaultX()
            
            # Цветовая схема
            self.COLORS = {
                'bg_dark': '#121212',
                'bg_darker': '#0a0a0a',
                'bg_panel': '#1e1e1e',
                'accent_green': '#4CAF50',
                'accent_blue': '#2196F3',
                'accent_red': '#f44336',
                'accent_orange': '#FF9800',
                'accent_purple': '#9C27B0',
                'text_primary': '#ffffff',
                'text_secondary': '#aaaaaa',
                'text_muted': '#666666',
                'border': '#444444'
            }
            
            self.setup_window()
            
            # Переменные
            self.current_file = tk.StringVar()
            self.user_words = []
            self.user_dates = []
            self.personal_info = {}
            
            self.create_ui()
            self.center_window()
            
            # Проверка зависимостей
            self.check_dependencies()
            
        def setup_window(self):
            """Настройка окна"""
            self.root.title(f"🚀 SUPER VAULT X v{self.vault.VERSION}")
            self.root.geometry("1200x900")
            self.root.configure(bg=self.COLORS['bg_dark'])
            
            # Иконка
            try:
                if os.path.exists("logo.ico"):
                    self.root.iconbitmap("logo.ico")
            except:
                pass
            
            # Сделать окно разворачиваемым
            self.root.minsize(1000, 700)
            
        def center_window(self):
            """Центрирование окна"""
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            
        def check_dependencies(self):
            """Проверка криптографических библиотек"""
            if not CRYPTO_AVAILABLE:
                response = messagebox.askyesno(
                    "Требуется установка",
                    "Для работы Super Vault X требуется библиотека pycryptodome.\n\n"
                    "Установить сейчас? (требуется интернет соединение)"
                )
                
                if response:
                    try:
                        result = subprocess.run(
                            [sys.executable, "-m", "pip", "install", "pycryptodome"],
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                        
                        if result.returncode == 0:
                            messagebox.showinfo(
                                "Успех!",
                                "Библиотека успешно установлена!\n\n"
                                "Перезапустите программу для начала работы."
                            )
                            self.root.destroy()
                            sys.exit(0)
                        else:
                            messagebox.showerror(
                                "Ошибка установки",
                                f"Не удалось установить библиотеку:\n\n"
                                f"{result.stderr}\n\n"
                                f"Установите вручную:\n"
                                f"pip install pycryptodome"
                            )
                    except Exception as e:
                        messagebox.showerror(
                            "Ошибка",
                            f"Не удалось запустить установку:\n{str(e)}\n\n"
                            f"Установите вручную:\n"
                            f"pip install pycryptodome"
                        )
        
        def create_ui(self):
            """Создание интерфейса"""
            # Создание стилей
            self.create_styles()
            
            # Главный контейнер
            main_container = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
            main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # === ЗАГОЛОВОК ===
            self.create_header(main_container)
            
            # === ПАНЕЛЬ ФАЙЛОВ ===
            self.create_file_panel(main_container)
            
            # === ПАНЕЛЬ ПАРОЛЯ ===
            self.create_password_panel(main_container)
            
            # === ПАНЕЛЬ ДЕЙСТВИЙ ===
            self.create_action_panel(main_container)
            
            # === ПАНЕЛЬ СТАТУСА ===
            self.create_status_panel(main_container)
            
            # === ПАНЕЛЬ АВТОРА ===
            self.create_author_panel(main_container)
            
        def create_styles(self):
            """Создание стилей Ttk"""
            style = ttk.Style()
            style.theme_use('clam')
            
            # Кастомные стили
            style.configure('SuperTitle.TLabel',
                          background=self.COLORS['bg_dark'],
                          foreground=self.COLORS['accent_green'],
                          font=('Arial', 26, 'bold'))
            
            style.configure('SuperFrame.TLabelframe',
                          background=self.COLORS['bg_panel'],
                          foreground=self.COLORS['text_primary'],
                          bordercolor=self.COLORS['border'],
                          relief='solid',
                          borderwidth=1)
            
            style.configure('SuperFrame.TLabelframe.Label',
                          background=self.COLORS['bg_panel'],
                          foreground=self.COLORS['accent_blue'],
                          font=('Arial', 11, 'bold'))
            
            style.configure('SuperButton.TButton',
                          background=self.COLORS['accent_green'],
                          foreground='white',
                          font=('Arial', 11, 'bold'),
                          borderwidth=0,
                          padding=10)
            
            style.map('SuperButton.TButton',
                     background=[('active', '#45a049'), ('disabled', '#666666')])
            
            style.configure('SuperButtonRed.TButton',
                          background=self.COLORS['accent_red'],
                          foreground='white',
                          font=('Arial', 11, 'bold'))
            
            style.configure('SuperButtonBlue.TButton',
                          background=self.COLORS['accent_blue'],
                          foreground='white',
                          font=('Arial', 11, 'bold'))
            
        def create_header(self, parent):
            """Создание заголовка"""
            header_frame = tk.Frame(parent, bg=self.COLORS['bg_dark'])
            header_frame.pack(fill=tk.X, pady=(0, 20))
            
            # Логотип и название
            logo_text = tk.Label(header_frame,
                               text="🔐",
                               font=('Arial', 48),
                               bg=self.COLORS['bg_dark'],
                               fg=self.COLORS['accent_green'])
            logo_text.pack(side=tk.LEFT, padx=(0, 15))
            
            title_frame = tk.Frame(header_frame, bg=self.COLORS['bg_dark'])
            title_frame.pack(side=tk.LEFT)
            
            tk.Label(title_frame,
                   text="SUPER VAULT X PRO",
                   font=('Arial', 28, 'bold'),
                   bg=self.COLORS['bg_dark'],
                   fg=self.COLORS['accent_green']).pack(anchor='w')
            
            tk.Label(title_frame,
                   text="Мегашифрование файлов с паролями из 10000 строк",
                   font=('Arial', 12),
                   bg=self.COLORS['bg_dark'],
                   fg=self.COLORS['text_secondary']).pack(anchor='w')
            
            tk.Label(title_frame,
                   text=f"Автор: {self.vault.AUTHOR} © {self.vault.YEAR} | Версия: {self.vault.VERSION}",
                   font=('Arial', 9),
                   bg=self.COLORS['bg_dark'],
                   fg=self.COLORS['text_muted']).pack(anchor='w', pady=(5, 0))
            
            # Разделитель
            ttk.Separator(parent, orient='horizontal').pack(fill=tk.X, pady=10)
            
        def create_file_panel(self, parent):
            """Панель выбора файла"""
            file_frame = ttk.LabelFrame(parent,
                                      text=" 1. ВЫБЕРИТЕ ФАЙЛ ИЛИ ПАПКУ ",
                                      style='SuperFrame.TLabelframe')
            file_frame.pack(fill=tk.X, pady=(0, 15))
            
            inner_frame = tk.Frame(file_frame, bg=self.COLORS['bg_panel'])
            inner_frame.pack(padx=15, pady=15, fill=tk.X)
            
            # Кнопки выбора
            button_frame = tk.Frame(inner_frame, bg=self.COLORS['bg_panel'])
            button_frame.pack(fill=tk.X, pady=(0, 10))
            
            ttk.Button(button_frame,
                      text="📁 ВЫБРАТЬ ФАЙЛ",
                      command=self.select_file,
                      style='SuperButton.TButton',
                      width=20).pack(side=tk.LEFT, padx=(0, 10))
            
            ttk.Button(button_frame,
                      text="📂 ВЫБРАТЬ ПАПКУ",
                      command=self.select_directory,
                      style='SuperButtonBlue.TButton',
                      width=20).pack(side=tk.LEFT)
            
            # Поле с путем
            path_frame = tk.Frame(inner_frame, bg=self.COLORS['bg_panel'])
            path_frame.pack(fill=tk.X)
            
            tk.Label(path_frame,
                   text="Путь:",
                   bg=self.COLORS['bg_panel'],
                   fg=self.COLORS['text_secondary'],
                   font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 10))
            
            self.file_entry = tk.Entry(path_frame,
                                     textvariable=self.current_file,
                                     font=('Consolas', 10),
                                     bg='#2d2d30',
                                     fg='white',
                                     insertbackground='white',
                                     relief=tk.FLAT,
                                     state='readonly',
                                     width=80)
            self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
        def create_password_panel(self, parent):
            """Панель создания пароля"""
            password_frame = ttk.LabelFrame(parent,
                                          text=" 2. СОЗДАНИЕ МЕГА-ПАРОЛЯ (10000 строк) ",
                                          style='SuperFrame.TLabelframe')
            password_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            
            # Ноутбук с вкладками
            notebook = ttk.Notebook(password_frame)
            notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            # Вкладка 1: Слова
            words_tab = tk.Frame(notebook, bg=self.COLORS['bg_panel'])
            notebook.add(words_tab, text="📝 Ваши слова")
            
            tk.Label(words_tab,
                   text="Введите слова, фразы, имена, понятия (каждое с новой строки):",
                   bg=self.COLORS['bg_panel'],
                   fg=self.COLORS['text_secondary'],
                   font=('Arial', 9)).pack(anchor='w', padx=10, pady=(10, 5))
            
            self.words_text = scrolledtext.ScrolledText(
                words_tab,
                height=10,
                font=('Consolas', 10),
                bg='#252526',
                fg='white',
                insertbackground='white',
                wrap=tk.WORD
            )
            self.words_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            
            # Вкладка 2: Даты
            dates_tab = tk.Frame(notebook, bg=self.COLORS['bg_panel'])
            notebook.add(dates_tab, text="📅 Ваши даты")
            
            tk.Label(dates_tab,
                   text="Введите важные даты (дни рождения, годовщины, события):",
                   bg=self.COLORS['bg_panel'],
                   fg=self.COLORS['text_secondary'],
                   font=('Arial', 9)).pack(anchor='w', padx=10, pady=(10, 5))
            
            self.dates_text = scrolledtext.ScrolledText(
                dates_tab,
                height=6,
                font=('Consolas', 10),
                bg='#252526',
                fg='white',
                insertbackground='white',
                wrap=tk.WORD
            )
            self.dates_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            
            # Вкладка 3: Персональная информация
            info_tab = tk.Frame(notebook, bg=self.COLORS['bg_panel'])
            notebook.add(info_tab, text="👤 Персональные данные")
            
            tk.Label(info_tab,
                   text="Введите дополнительную информацию (ключ=значение):",
                   bg=self.COLORS['bg_panel'],
                   fg=self.COLORS['text_secondary'],
                   font=('Arial', 9)).pack(anchor='w', padx=10, pady=(10, 5))
            
            self.info_text = scrolledtext.ScrolledText(
                info_tab,
                height=8,
                font=('Consolas', 10),
                bg='#252526',
                fg='white',
                insertbackground='white',
                wrap=tk.WORD
            )
            self.info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            self.info_text.insert('1.0', "город=ВашГород\nимя=ВашеИмя\nхобби=ВашеХобби\n")
            
        def create_action_panel(self, parent):
            """Панель действий"""
            action_frame = ttk.LabelFrame(parent,
                                        text=" 3. ДЕЙСТВИЯ ",
                                        style='SuperFrame.TLabelframe')
            action_frame.pack(fill=tk.X, pady=(0, 15))
            
            inner_frame = tk.Frame(action_frame, bg=self.COLORS['bg_panel'])
            inner_frame.pack(padx=15, pady=15)
            
            # Основные кнопки
            self.encrypt_btn = ttk.Button(
                inner_frame,
                text="🚀 ЗАШИФРОВАТЬ",
                command=self.start_encryption,
                style='SuperButton.TButton',
                width=25
            )
            self.encrypt_btn.grid(row=0, column=0, padx=5, pady=5)
            
            self.decrypt_btn = ttk.Button(
                inner_frame,
                text="🔓 ДЕШИФРОВАТЬ",
                command=self.start_decryption,
                style='SuperButtonBlue.TButton',
                width=25
            )
            self.decrypt_btn.grid(row=0, column=1, padx=5, pady=5)
            
            # Дополнительные кнопки
            ttk.Button(
                inner_frame,
                text="🧹 ОЧИСТИТЬ ВСЁ",
                command=self.clear_all,
                width=20
            ).grid(row=1, column=0, padx=5, pady=5)
            
            ttk.Button(
                inner_frame,
                text="❓ ПОМОЩЬ",
                command=self.show_help,
                width=20
            ).grid(row=1, column=1, padx=5, pady=5)
            
            ttk.Button(
                inner_frame,
                text="🔍 ПРОВЕРИТЬ ЦЕЛОСТНОСТЬ",
                command=self.check_integrity,
                width=25
            ).grid(row=2, column=0, columnspan=2, padx=5, pady=10)
            
        def create_status_panel(self, parent):
            """Панель статуса"""
            status_frame = ttk.LabelFrame(parent,
                                        text=" 📊 СТАТУС И ЛОГИ ",
                                        style='SuperFrame.TLabelframe')
            status_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            
            self.status_text = scrolledtext.ScrolledText(
                status_frame,
                height=15,
                font=('Consolas', 9),
                bg='#0d0d0d',
                fg='#00ff00',
                state='disabled',
                wrap=tk.WORD
            )
            self.status_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            # Теги для цветного текста
            self.status_text.tag_config("success", foreground=self.COLORS['accent_green'])
            self.status_text.tag_config("error", foreground=self.COLORS['accent_red'])
            self.status_text.tag_config("warning", foreground=self.COLORS['accent_orange'])
            self.status_text.tag_config("info", foreground=self.COLORS['accent_blue'])
            self.status_text.tag_config("muted", foreground=self.COLORS['text_muted'])
            
        def create_author_panel(self, parent):
            """Панель автора и соцсетей"""
            author_frame = tk.Frame(parent, bg=self.COLORS['bg_dark'])
            author_frame.pack(fill=tk.X, pady=(10, 0))
            
            # Автор
            tk.Label(author_frame,
                   text=f"© {self.vault.YEAR} {self.vault.AUTHOR}",
                   bg=self.COLORS['bg_dark'],
                   fg=self.COLORS['text_muted'],
                   font=('Arial', 9)).pack(side=tk.LEFT)
            
            # Соцсети
            socials_frame = tk.Frame(author_frame, bg=self.COLORS['bg_dark'])
            socials_frame.pack(side=tk.RIGHT)
            
            tk.Label(socials_frame,
                   text="Соцсети автора:",
                   bg=self.COLORS['bg_dark'],
                   fg=self.COLORS['text_secondary'],
                   font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 10))
            
            socials = [
                ("💻 GitHub", "https://github.com/ftoop17"),
                ("📱 Telegram", "https://t.me/thetemirbolatov"),
                ("👥 VK", "https://vk.com/thetemirbolatov"),
                ("📸 Instagram", "https://instagram.com/thetemirbolatov")
            ]
            
            for icon_text, url in socials:
                btn = tk.Button(
                    socials_frame,
                    text=icon_text,
                    command=lambda u=url: webbrowser.open(u),
                    font=('Arial', 9),
                    bg='#333333',
                    fg='white',
                    relief=tk.FLAT,
                    padx=10,
                    pady=2,
                    cursor='hand2'
                )
                btn.pack(side=tk.LEFT, padx=2)
        
        def log(self, message, tag="info"):
            """Логирование в интерфейс"""
            self.status_text.config(state='normal')
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.status_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
            self.status_text.see(tk.END)
            self.status_text.config(state='disabled')
            self.root.update()
        
        def select_file(self):
            """Выбор файла"""
            filename = filedialog.askopenfilename(
                title="Выберите файл для шифрования",
                filetypes=[
                    ("Все файлы", "*.*"),
                    ("Документы", "*.pdf *.doc *.docx *.xls *.xlsx *.ppt *.pptx *.txt *.rtf"),
                    ("Изображения", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp *.svg"),
                    ("Архивы", "*.zip *.rar *.7z *.tar *.gz *.bz2"),
                    ("Видео", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
                    ("Аудио", "*.mp3 *.wav *.flac *.ogg *.m4a"),
                    ("Базы данных", "*.db *.sqlite *.sql *.mdb"),
                    ("Исполняемые файлы", "*.exe *.msi *.bat *.sh *.py *.jar")
                ]
            )
            
            if filename:
                try:
                    file_size = os.path.getsize(filename)
                    self.current_file.set(filename)
                    self.log(f"Выбран файл: {os.path.basename(filename)} ({file_size:,} байт)")
                except Exception as e:
                    self.log(f"Ошибка получения информации о файле: {str(e)}", "error")
        
        def select_directory(self):
            """Выбор директории"""
            directory = filedialog.askdirectory(title="Выберите папку для шифрования")
            if directory:
                self.current_file.set(directory)
                self.log(f"Выбрана папка: {directory}")
        
        def get_user_input(self):
            """Получение данных от пользователя"""
            # Слова
            words_input = self.words_text.get("1.0", tk.END).strip()
            self.user_words = [w.strip() for w in words_input.split('\n') if w.strip()]
            
            if len(self.user_words) < self.vault.MIN_USER_WORDS:
                messagebox.showwarning(
                    "Недостаточно слов",
                    f"Пожалуйста, введите минимум {self.vault.MIN_USER_WORDS} слово для создания мега-пароля.\n\n"
                    f"Примеры: ваш город, имя, любимая книга, хобби и т.д."
                )
                return False
            
            # Даты
            dates_input = self.dates_text.get("1.0", tk.END).strip()
            self.user_dates = [d.strip() for d in dates_input.split('\n') if d.strip()]
            
            # Персональная информация
            info_input = self.info_text.get("1.0", tk.END).strip()
            self.personal_info = {}
            for line in info_input.split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    self.personal_info[key.strip()] = value.strip()
            
            return True
        
        def start_encryption(self):
            """Начало шифрования"""
            if not self.current_file.get():
                messagebox.showwarning("Внимание", "Сначала выберите файл или папку!")
                return
            
            if not os.path.exists(self.current_file.get()):
                messagebox.showerror("Ошибка", "Выбранный файл/папка не существует!")
                return
            
            if not self.get_user_input():
                return
            
            if not CRYPTO_AVAILABLE:
                messagebox.showerror(
                    "Ошибка",
                    "Библиотека pycryptodome не установлена!\n\n"
                    "Установите её командой:\n"
                    "pip install pycryptodome"
                )
                return
            
            # Подтверждение
            is_file = os.path.isfile(self.current_file.get())
            target_name = os.path.basename(self.current_file.get())
            
            if is_file:
                target_size = os.path.getsize(self.current_file.get())
                size_text = f"{target_size:,} байт"
            else:
                size_text = "папка"
            
            response = messagebox.askyesno(
                "Подтверждение шифрования",
                f"Вы уверены, что хотите зашифровать?\n\n"
                f"Объект: {target_name}\n"
                f"Тип: {'Файл' if is_file else 'Папка'}\n"
                f"Размер: {size_text}\n\n"
                f"⚠️  После шифрования оригинал будет БЕЗВОЗВРАТНО УДАЛЕН!\n"
                f"⚠️  Файл с паролем будет сохранен рядом.\n"
                f"⚠️  БЕЗ файла пароля восстановление НЕВОЗМОЖНО!\n\n"
                f"Продолжить?"
            )
            
            if not response:
                return
            
            # Запуск в отдельном потоке
            thread = threading.Thread(target=self.encryption_thread, 
                                    args=(is_file,))
            thread.daemon = True
            thread.start()
        
        def encryption_thread(self, is_file):
            """Поток шифрования"""
            self.root.config(cursor="wait")
            self.encrypt_btn.config(state='disabled')
            self.decrypt_btn.config(state='disabled')
            
            try:
                self.log("=" * 70, "info")
                self.log("🚀 НАЧАЛО ШИФРОВАНИЯ", "info")
                self.log("=" * 70, "info")
                
                target_path = self.current_file.get()
                target_name = os.path.basename(target_path)
                
                self.log(f"Объект: {target_name}")
                self.log(f"Слов для пароля: {len(self.user_words)}")
                self.log(f"Дат для пароля: {len(self.user_dates)}")
                
                # Создание мега-пароля
                self.log("⚡ Создаю мега-пароль из 10000 строк...", "info")
                
                password, password_hash, stats = self.vault.create_mega_password(
                    self.user_words,
                    self.user_dates,
                    self.personal_info,
                    use_dictionaries=True,
                    add_timestamps=True
                )
                
                self.log("✅ Мега-пароль создан успешно!", "success")
                
                # Шифрование
                if is_file:
                    self.log("🔒 Начинаю шифрование файла...", "info")
                    result = self.vault.encrypt_file(
                        target_path,
                        password,
                        delete_original=True,
                        secure_delete_passes=7,
                        compress_before_encrypt=True
                    )
                else:
                    self.log("📁 Начинаю шифрование папки...", "info")
                    result = self.vault.encrypt_directory(
                        target_path,
                        password,
                        include_subdirs=True,
                        create_single_archive=True
                    )
                
                if result['success']:
                    # Сохранение пароля в файл
                    password_file = self.vault.save_password_to_file(
                        password,
                        target_path,
                        stats
                    )
                    
                    result['password_file'] = password_file
                    
                    self.log("=" * 70, "success")
                    self.log("✅ ШИФРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО!", "success")
                    self.log("=" * 70, "success")
                    
                    # Вывод результатов
                    if is_file:
                        self.log(f"📁 Зашифрованный файл: {os.path.basename(result['encrypted_file'])}", "success")
                        self.log(f"🔑 Файл с паролем: {os.path.basename(password_file)}", "success")
                        self.log(f"📊 Размер: {result['original_size']:,} → {result['encrypted_size']:,} байт", "info")
                        self.log(f"⏱️  Время: {result['elapsed_time']:.2f} секунд", "info")
                        self.log(f"📈 Коэффициент: {result.get('encryption_ratio', 1):.2f}x", "info")
                    else:
                        self.log(f"📁 Зашифрованный архив создан", "success")
                        self.log(f"🔑 Файл с паролем: {os.path.basename(password_file)}", "success")
                    
                    # Сообщение пользователю
                    messagebox.showinfo(
                        "✅ УСПЕХ!",
                        f"Шифрование завершено успешно!\n\n"
                        f"📁 Зашифрованный файл:\n{os.path.basename(result.get('encrypted_file', 'архив'))}\n\n"
                        f"🔑 Файл с паролем:\n{os.path.basename(password_file)}\n\n"
                        f"⚠️ ⚠️ ⚠️ ВАЖНО ⚠️ ⚠️ ⚠️\n"
                        f"1. Сохраните файл с паролем в БЕЗОПАСНОМ месте!\n"
                        f"2. Без этого файла восстановление НЕВОЗМОЖНО!\n"
                        f"3. Оригинал был безопасно удален.\n\n"
                        f"⏱️  Время: {result.get('elapsed_time', 0):.2f} сек"
                    )
                    
                    # Открытие папки с результатами
                    output_dir = os.path.dirname(result.get('encrypted_file', password_file))
                    self.open_folder(output_dir)
                    
                else:
                    self.log("❌ ОШИБКА ШИФРОВАНИЯ", "error")
                    self.log(f"Причина: {result.get('error', 'Неизвестная ошибка')}", "error")
                    
                    messagebox.showerror(
                        "❌ ОШИБКА",
                        f"Не удалось зашифровать:\n\n"
                        f"{result['error']}\n\n"
                        f"Проверьте:\n"
                        f"1. Доступ к файлу\n"
                        f"2. Достаточно ли места на диске\n"
                        f"3. Не поврежден ли файл"
                    )
                    
            except Exception as e:
                self.log(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {str(e)}", "error")
                messagebox.showerror(
                    "❌ КРИТИЧЕСКАЯ ОШИБКА",
                    f"Произошла критическая ошибка:\n\n{str(e)}"
                )
                
            finally:
                self.root.config(cursor="")
                self.encrypt_btn.config(state='normal')
                self.decrypt_btn.config(state='normal')
        
        def start_decryption(self):
            """Начало дешифрования"""
            # Выбор зашифрованного файла
            encrypted_file = filedialog.askopenfilename(
                title="Выберите зашифрованный файл (.svx)",
                filetypes=[
                    ("SVX файлы", "*.svx"),
                    ("Все файлы", "*.*")
                ]
            )
            
            if not encrypted_file:
                return
            
            # Проверка расширения
            if not encrypted_file.endswith('.svx'):
                response = messagebox.askyesno(
                    "Предупреждение",
                    f"Выбранный файл не имеет расширения .svx:\n"
                    f"{os.path.basename(encrypted_file)}\n\n"
                    f"Продолжить в любом случае?"
                )
                if not response:
                    return
            
            # Выбор файла с паролем
            password_file = filedialog.askopenfilename(
                title="Выберите файл с паролем (.txt)",
                filetypes=[
                    ("Текстовые файлы", "*.txt"),
                    ("Все файлы", "*.*")
                ]
            )
            
            if not password_file:
                return
            
            if not CRYPTO_AVAILABLE:
                messagebox.showerror(
                    "Ошибка",
                    "Библиотека pycryptodome не установлена!"
                )
                return
            
            # Используем новую функцию для чтения пароля
            self.log("📖 Читаю пароль из файла...", "info")
            password = self.vault.read_password_from_file(password_file)
            
            if not password:
                messagebox.showerror(
                    "Ошибка чтения пароля",
                    "Не удалось прочитать пароль из файла!"
                )
                return
            
            # Проверка длины
            line_count = len(password.split('\n'))
            if line_count < 100:
                response = messagebox.askyesno(
                    "Предупреждение",
                    f"Найденный пароль содержит только {line_count} строк,\n"
                    f"в то время как ожидается 10000 строк.\n\n"
                    f"Это может быть неправильный файл пароля.\n"
                    f"Продолжить в любом случае?"
                )
                if not response:
                    return
            
            # Запуск дешифрования
            thread = threading.Thread(target=self.decryption_thread,
                                    args=(encrypted_file, password))
            thread.daemon = True
            thread.start()
        
        def decryption_thread(self, encrypted_file, password):
            """Поток дешифрования"""
            self.root.config(cursor="wait")
            self.encrypt_btn.config(state='disabled')
            self.decrypt_btn.config(state='disabled')
            
            try:
                self.log("=" * 70, "info")
                self.log("🚀 НАЧАЛО ДЕШИФРОВАНИЯ", "info")
                self.log("=" * 70, "info")
                
                self.log(f"Файл: {os.path.basename(encrypted_file)}", "info")
                self.log(f"Длина пароля: {len(password.split(chr(10)))} строк", "info")
                
                self.log("🔓 Начинаю дешифрование...", "info")
                result = self.vault.decrypt_file(
                    encrypted_file,
                    password,
                    verify_integrity=True
                )
                
                if result['success']:
                    self.log("=" * 70, "success")
                    self.log("✅ ДЕШИФРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО!", "success")
                    self.log("=" * 70, "success")
                    
                    self.log(f"📁 Дешифрованный файл: {os.path.basename(result['decrypted_file'])}", "success")
                    self.log(f"📊 Размер: {result['decrypted_size']:,} байт", "info")
                    self.log(f"⏱️  Время: {result['elapsed_time']:.2f} секунд", "info")
                    
                    if result.get('hash_match') is False:
                        self.log("⚠️ Внимание: хэши не совпадают! Файл может быть поврежден.", "warning")
                    
                    # Сообщение пользователю
                    messagebox.showinfo(
                        "✅ УСПЕХ!",
                        f"Файл успешно дешифрован!\n\n"
                        f"📁 Дешифрованный файл:\n{os.path.basename(result['decrypted_file'])}\n\n"
                        f"📊 Размер: {result['decrypted_size']:,} байт\n"
                        f"⏱️  Время: {result['elapsed_time']:.2f} сек"
                    )
                    
                    # Открытие папки
                    output_dir = os.path.dirname(result['decrypted_file'])
                    self.open_folder(output_dir)
                    
                else:
                    self.log("❌ ОШИБКА ДЕШИФРОВАНИЯ", "error")
                    self.log(f"Причина: {result.get('error', 'Неизвестная ошибка')}", "error")
                    
                    messagebox.showerror(
                        "❌ ОШИБКА",
                        f"Не удалось дешифровать файл:\n\n{result['error']}"
                    )
                    
            except Exception as e:
                self.log(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {str(e)}", "error")
                messagebox.showerror(
                    "❌ КРИТИЧЕСКАЯ ОШИБКА",
                    f"Произошла критическая ошибка:\n\n{str(e)}"
                )
                
            finally:
                self.root.config(cursor="")
                self.encrypt_btn.config(state='normal')
                self.decrypt_btn.config(state='normal')
        
        def check_integrity(self):
            """Проверка целостности файла"""
            encrypted_file = filedialog.askopenfilename(
                title="Выберите зашифрованный файл для проверки",
                filetypes=[("SVX файлы", "*.svx")]
            )
            
            if not encrypted_file:
                return
            
            # Запрос пароля
            password = self.ask_for_password()
            if not password:
                return
            
            # Проверка
            result = self.vault.verify_integrity(encrypted_file, password)
            
            if result['valid']:
                messagebox.showinfo(
                    "✅ ЦЕЛОСТНОСТЬ ПОДТВЕРЖДЕНА",
                    f"Файл прошел проверку целостности!\n\n"
                    f"📁 Файл: {os.path.basename(encrypted_file)}\n"
                    f"📊 Оригинальный размер: {result['file_info']['original_size']:,} байт\n"
                    f"🔒 Алгоритм: {result['file_info']['algorithm']}\n"
                    f"📅 Дата создания: {result['file_info']['timestamp']}\n\n"
                    f"✅ HMAC проверка: {result['integrity_check']}\n"
                    f"✅ Хэш пароля: совпадает"
                )
            else:
                messagebox.showerror(
                    "❌ НАРУШЕНА ЦЕЛОСТНОСТЬ",
                    f"Файл не прошел проверку целостности!\n\n"
                    f"Ошибка: {result.get('error', 'Неизвестная ошибка')}\n\n"
                    f"Возможные причины:\n"
                    f"1. Файл поврежден\n"
                    f"2. Неправильный пароль\n"
                    f"3. Файл был изменен"
                )
        
        def ask_for_password(self):
            """Запрос пароля у пользователя"""
            dialog = tk.Toplevel(self.root)
            dialog.title("Введите пароль")
            dialog.geometry("500x300")
            dialog.configure(bg=self.COLORS['bg_panel'])
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Центрирование
            dialog.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 150
            dialog.geometry(f"+{x}+{y}")
            
            tk.Label(dialog,
                   text="Введите пароль (10000 строк):",
                   bg=self.COLORS['bg_panel'],
                   fg=self.COLORS['text_primary'],
                   font=('Arial', 11)).pack(pady=(20, 10))
            
            password_text = scrolledtext.ScrolledText(
                dialog,
                height=10,
                font=('Consolas', 9),
                bg='#252526',
                fg='white'
            )
            password_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
            
            result = {'password': None}
            
            def on_ok():
                result['password'] = password_text.get("1.0", tk.END).strip()
                dialog.destroy()
            
            def on_cancel():
                dialog.destroy()
            
            button_frame = tk.Frame(dialog, bg=self.COLORS['bg_panel'])
            button_frame.pack(pady=(0, 20))
            
            ttk.Button(button_frame,
                      text="ОК",
                      command=on_ok,
                      style='SuperButton.TButton').pack(side=tk.LEFT, padx=10)
            
            ttk.Button(button_frame,
                      text="ОТМЕНА",
                      command=on_cancel).pack(side=tk.LEFT, padx=10)
            
            dialog.wait_window()
            return result['password']
        
        def open_folder(self, folder_path):
            """Открытие папки в проводнике"""
            try:
                if sys.platform == "win32":
                    os.startfile(folder_path)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", folder_path])
                else:
                    subprocess.Popen(["xdg-open", folder_path])
            except Exception as e:
                self.log(f"Не удалось открыть папку: {str(e)}", "warning")
        
        def clear_all(self):
            """Очистка всех полей"""
            self.current_file.set("")
            self.words_text.delete("1.0", tk.END)
            self.dates_text.delete("1.0", tk.END)
            self.info_text.delete("1.0", tk.END)
            self.info_text.insert("1.0", "город=ВашГород\nимя=ВашеИмя\nхобби=ВашеХобби\n")
            self.status_text.config(state='normal')
            self.status_text.delete("1.0", tk.END)
            self.status_text.config(state='disabled')
            self.log("Все поля очищены", "info")
        
        def show_help(self):
            """Показать справку"""
            help_text = """
╔══════════════════════════════════════════════════════╗
║               SUPER VAULT X PRO - СПРАВКА           ║
╚══════════════════════════════════════════════════════╝

🚀 ОСНОВНЫЕ ВОЗМОЖНОСТИ:

• Шифрование любых файлов и папок
• Мега-пароли из 10000 уникальных строк
• Алгоритм: AES-256 + PBKDF2 + HMAC
• Безопасное удаление оригиналов
• Проверка целостности файлов
• Сжатие перед шифрованием
• Поддержка всех типов файлов

🔐 КАК ШИФРОВАТЬ:

1. Выберите файл или папку
2. Введите слова для пароля (минимум 1 слово)
3. Добавьте даты (опционально)
4. Добавьте персональную информацию (опционально)
5. Нажмите "ЗАШИФРОВАТЬ"
6. Сохраните файл с паролем в БЕЗОПАСНОМ месте!

🔓 КАК ДЕШИФРОВАТЬ:

1. Нажмите "ДЕШИФРОВАТЬ"
2. Выберите файл .svx
3. Выберите файл с паролем .txt
4. Файл будет восстановлен

⚠️ ВАЖНЫЕ ПРЕДУПРЕЖДЕНИЯ:

• БЕЗ ФАЙЛА ПАРОЛЯ ВОССТАНОВЛЕНИЕ НЕВОЗМОЖНО!
• Оригиналы удаляются безвозвратно
• Делайте резервные копии паролей
• Не храните пароли с зашифрованными файлами

📁 ФОРМАТЫ ФАЙЛОВ:

• Зашифрованные: ENCRYPTED_имя_ДАТА.svx
• Пароли: SUPER_PASSWORD_имя_ДАТА_ВРЕМЯ.txt
• Дешифрованные: DECRYPTED_имя

👨‍💻 АВТОР: thetemirbolatov © 2025
🌐 GitHub: https://github.com/thetemirbolatov
            """
            
            help_window = tk.Toplevel(self.root)
            help_window.title("Справка - Super Vault X Pro")
            help_window.geometry("800x600")
            help_window.configure(bg=self.COLORS['bg_dark'])
            
            help_text_widget = scrolledtext.ScrolledText(
                help_window,
                font=('Consolas', 9),
                bg='#0d0d0d',
                fg=self.COLORS['accent_green'],
                wrap=tk.WORD
            )
            help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            help_text_widget.insert('1.0', help_text)
            help_text_widget.config(state='disabled')
            
            # Центрирование
            help_window.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 400
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 300
            help_window.geometry(f"+{x}+{y}")
            
        def run(self):
            """Запуск приложения"""
            self.root.mainloop()

# ============================================================================
# КОМАНДНАЯ СТРОКА
# ============================================================================

def cmd_encrypt():
    """Шифрование через командную строку"""
    if len(sys.argv) < 3:
        print("Использование: python app.py encrypt <путь_к_файлу>")
        return
    
    file_path = sys.argv[2]
    
    if not os.path.exists(file_path):
        print(f"❌ Ошибка: Файл не найден: {file_path}")
        return
    
    print(f"\n{'='*70}")
    print(f"🚀 SUPER VAULT X - Шифрование")
    print(f"{'='*70}")
    print(f"📁 Файл: {os.path.basename(file_path)}")
    print(f"📊 Размер: {os.path.getsize(file_path):,} байт")
    
    print(f"\n📝 Введите слова для пароля (каждое с новой строки).")
    print("Нажмите Enter дважды для завершения ввода:")
    
    words = []
    while True:
        try:
            line = input().strip()
            if line == "":
                if words:
                    break
                continue
            words.append(line)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n❌ Прервано пользователем")
            return
    
    if not words:
        print("❌ Ошибка: Нужно хотя бы одно слово!")
        return
    
    print("\n📅 Введите важные даты (опционально, Enter для завершения):")
    dates = []
    while True:
        try:
            line = input().strip()
            if line == "":
                break
            dates.append(line)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n❌ Прервано пользователем")
            return
    
    print(f"\n⚡ Создаю мега-пароль из 10000 строк...")
    vault = SuperVaultX()
    
    try:
        password, _, stats = vault.create_mega_password(words, dates, {})
    except Exception as e:
        print(f"❌ Ошибка создания пароля: {str(e)}")
        return
    
    print("🔒 Шифрую файл...")
    result = vault.encrypt_file(file_path, password, delete_original=True)
    
    if result['success']:
        password_file = vault.save_password_to_file(password, file_path, stats)
        elapsed = result.get('elapsed_time', 0)
        
        print(f"\n{'='*70}")
        print(f"✅ ШИФРОВАНИЕ УСПЕШНО!")
        print(f"{'='*70}")
        print(f"📁 Зашифрованный файл: {os.path.basename(result['encrypted_file'])}")
        print(f"🔑 Файл с паролем: {os.path.basename(password_file)}")
        print(f"📊 Размер: {result['original_size']:,} → {result['encrypted_size']:,} байт")
        print(f"⏱️  Время: {elapsed:.2f} секунд")
        print(f"📈 Коэффициент: {result.get('encryption_ratio', 1):.2f}x")
        print(f"\n⚠️  СОХРАНИТЕ ФАЙЛ С ПАРОЛЕМ!")
        print(f"⚠️  Без него восстановление НЕВОЗМОЖНО!")
    else:
        print(f"\n❌ Ошибка: {result.get('error')}")

def cmd_decrypt():
    """Дешифрование через командную строку"""
    if len(sys.argv) < 4:
        print("Использование: python app.py decrypt <зашифрованный.svx> <пароль.txt>")
        return
    
    encrypted_file = sys.argv[2]
    password_file = sys.argv[3]
    
    if not os.path.exists(encrypted_file):
        print(f"❌ Ошибка: Файл не найден: {encrypted_file}")
        return
    
    if not os.path.exists(password_file):
        print(f"❌ Ошибка: Файл пароля не найден: {password_file}")
        return
    
    print(f"\n{'='*70}")
    print(f"🔓 SUPER VAULT X - Дешифрование")
    print(f"{'='*70}")
    print(f"📁 Файл: {os.path.basename(encrypted_file)}")
    print(f"🔑 Пароль из: {password_file}")
    
    print(f"\n📖 Читаю пароль из файла...")
    
    # Используем новую функцию для чтения пароля
    vault = SuperVaultX()
    password = vault.read_password_from_file(password_file)
    
    if not password:
        print("❌ Ошибка: Не удалось прочитать пароль из файла!")
        return
    
    line_count = len(password.split('\n'))
    print(f"📊 Найден пароль из {line_count} строк")
    
    if line_count < 100:
        print(f"⚠️  Предупреждение: Мало строк в пароле!")
        response = input("Продолжить? (y/n): ")
        if response.lower() != 'y':
            return
    
    print("🔓 Дешифрую файл...")
    result = vault.decrypt_file(encrypted_file, password)
    
    if result['success']:
        elapsed = result.get('elapsed_time', 0)
        
        print(f"\n{'='*70}")
        print(f"✅ ДЕШИФРОВАНИЕ УСПЕШНО!")
        print(f"{'='*70}")
        print(f"📁 Дешифрованный файл: {os.path.basename(result['decrypted_file'])}")
        print(f"📊 Размер: {result['decrypted_size']:,} байт")
        print(f"⏱️  Время: {elapsed:.2f} секунд")
        
        if result.get('hash_match') is False:
            print(f"⚠️  Внимание: хэши не совпадают! Файл может быть поврежден.")
    else:
        print(f"\n❌ Ошибка: {result.get('error')}")

def cmd_help():
    """Показать справку"""
    help_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                 SUPER VAULT X PRO v{SuperVaultX.VERSION}                  ║
║                 Автор: {SuperVaultX.AUTHOR} © {SuperVaultX.YEAR}                 ║
╚══════════════════════════════════════════════════════════════╝

📦 УСТАНОВКА:
   pip install supervaultx   (скоро на PyPI)
   Или используйте файл app.py

🚀 ИСПОЛЬЗОВАНИЕ:

1. Графический интерфейс:
   python app.py
   Или просто запустите файл

2. Шифрование файла:
   python app.py encrypt <путь_к_файлу>
   
   Пример:
   python app.py encrypt C:\\Users\\Name\\secret.pdf

3. Дешифрование файла:
   python app.py decrypt <файл.svx> <пароль.txt>
   
   Пример:
   python app.py decrypt ENCRYPTED_secret_20251221_120000.svx SUPER_PASSWORD_secret_20251221_120000.txt

4. Проверка целостности:
   python app.py verify <файл.svx>

⚙️ ОСОБЕННОСТИ:

• 🔐 Мега-пароли из 10000 строк
• 🔒 AES-256 + PBKDF2 + HMAC шифрование
• 🗑️  Безопасное удаление оригиналов
• 📊 Сжатие перед шифрованием
• ✅ Проверка целостности
• 📁 Поддержка файлов и папок
• 🌐 UTF-8 кодировка
• 🖥️  GUI и CLI интерфейсы

⚠️  ВАЖНО:
   • БЕЗ ФАЙЛА ПАРОЛЯ ВОССТАНОВЛЕНИЕ НЕВОЗМОЖНО!
   • Сохраняйте файлы паролей в безопасном месте
   • Делайте резервные копии паролей

🌐 СОЦСЕТИ АВТОРА:
   GitHub:    https://github.com/thetemirbolatov
   Telegram:  @thetemirbolatov
   VK:        vk.com/thetemirbolatov
   Instagram: @thetemirbolatov
   YouTube:   @thetemirbolatov
════════════════════════════════════════════════════════════════
    """
    print(help_text)

def cmd_verify():
    """Проверка целостности"""
    if len(sys.argv) < 3:
        print("Использование: python app.py verify <файл.svx>")
        return
    
    encrypted_file = sys.argv[2]
    
    if not os.path.exists(encrypted_file):
        print(f"❌ Ошибка: Файл не найден: {encrypted_file}")
        return
    
    print(f"\n📝 Введите пароль для проверки целостности:")
    print("(Вставьте пароль из 10000 строк и нажмите Enter)")
    print("Нажмите Ctrl+Z (Windows) или Ctrl+D (Linux/Mac) для завершения:")
    
    password_lines = []
    try:
        while True:
            try:
                line = input()
                password_lines.append(line)
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\n❌ Прервано пользователем")
        return
    
    password = '\n'.join(password_lines).strip()
    
    if not password:
        print("❌ Ошибка: Пароль не введен!")
        return
    
    vault = SuperVaultX()
    result = vault.verify_integrity(encrypted_file, password)
    
    if result['valid']:
        print(f"\n✅ ЦЕЛОСТНОСТЬ ПОДТВЕРЖДЕНА!")
        print(f"📁 Файл: {os.path.basename(encrypted_file)}")
        print(f"📊 Оригинальный размер: {result['file_info']['original_size']:,} байт")
        print(f"🔒 Алгоритм: {result['file_info']['algorithm']}")
        print(f"📅 Дата создания: {result['file_info']['timestamp']}")
        print(f"✅ HMAC проверка: {result['integrity_check']}")
    else:
        print(f"\n❌ НАРУШЕНА ЦЕЛОСТНОСТЬ!")
        print(f"Ошибка: {result.get('error')}")

# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """Главная функция"""
    print(f"\n{'='*70}")
    print(f"🚀 SUPER VAULT X PRO v{SuperVaultX.VERSION}")
    print(f"👤 Автор: {SuperVaultX.AUTHOR} © {SuperVaultX.YEAR}")
    print(f"{'='*70}")
    
    if len(sys.argv) == 1:
        # Графический интерфейс
        if GUI_AVAILABLE:
            try:
                app = SuperVaultGUI()
                app.run()
            except Exception as e:
                print(f"❌ Ошибка запуска GUI: {str(e)}")
                print("Запускаю командный режим...")
                cmd_help()
        else:
            print("⚠️  GUI недоступен. Запускаю командный режим...")
            cmd_help()
    
    elif sys.argv[1] == "encrypt" and len(sys.argv) >= 3:
        cmd_encrypt()
    
    elif sys.argv[1] == "decrypt" and len(sys.argv) >= 4:
        cmd_decrypt()
    
    elif sys.argv[1] == "verify" and len(sys.argv) >= 3:
        cmd_verify()
    
    elif sys.argv[1] in ["--help", "-h", "help"]:
        cmd_help()
    
    else:
        print("Неизвестная команда!")
        cmd_help()

# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================

if __name__ == "__main__":
    # Проверка зависимостей
    if not CRYPTO_AVAILABLE:
        print("❌ ВНИМАНИЕ: Библиотека pycryptodome не установлена!")
        print("Установите её командой: pip install pycryptodome")
        print("Или запустите с флагом --help для получения справки")
        
        response = input("Установить сейчас? (y/n): ")
        if response.lower() == 'y':
            try:
                import subprocess
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "pycryptodome"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print("✅ Библиотека установлена! Перезапустите программу.")
                else:
                    print(f"❌ Ошибка установки: {result.stderr}")
            except Exception as e:
                print(f"❌ Ошибка: {str(e)}")
        
        sys.exit(1)
    
    # Запуск
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {str(e)}")
        import traceback
        traceback.print_exc()