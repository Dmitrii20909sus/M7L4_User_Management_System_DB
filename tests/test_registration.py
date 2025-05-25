import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()

def test_add_existing_user(setup_database, connection):
    """Тест добавления пользователя с существующим логином."""
    result_first = add_user('duplicateuser', 'dup1@example.com', 'pass1')
    result_second = add_user('duplicateuser', 'dup2@example.com', 'pass2') 
    assert result_first is False
    assert result_second is False, "Нельзя добавить пользователя с уже существующим логином."

def test_authenticate_success(setup_database, connection):
    """Тест успешной авторизации пользователя."""
    add_user('authuser', 'auth@example.com', 'securepass')
    result = authenticate_user('authuser', 'securepass')
    assert result is True

def test_authenticate_wrong_password(setup_database, connection):
    """Тест авторизации с неправильным паролем."""
    add_user('wrongpassuser', 'wrong@example.com', 'rightpass')
    result = authenticate_user('wrongpassuser', 'wrongpass')
    assert result is False

def test_authenticate_nonexistent_user(setup_database, connection):
    """Тест авторизации несуществующего пользователя."""
    result = authenticate_user('ghost', 'nopass')
    assert result is False

def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""