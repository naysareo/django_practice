# Django миграции: добавление, изменение и удаление поля

```python
# -----------------------------
# 1. ДОБАВЛЕНИЕ ПОЛЯ
# -----------------------------

# Исходная модель:
class Profile(models.Model):
    name = models.CharField(max_length=100)

# ШАГ 1: Добавляем новое поле
class Profile(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)  # новое поле

# ШАГ 2: Создаём миграцию
# В терминале:
# python manage.py makemigrations

# Django создаёт файл миграции 0002_add_age_to_profile.py
# Содержимое миграции:
"""
operations = [
    migrations.AddField(
        model_name='profile',
        name='age',
        field=models.IntegerField(default=18),
    ),
]
"""

# ШАГ 3: Применяем миграцию
# В терминале:
# python manage.py migrate

# Что происходит в базе:
# ALTER TABLE Profile ADD COLUMN age INTEGER DEFAULT 18
# Значение 18 заполняется для всех существующих записей

# Результат таблицы после миграции:
# | id | name  | age |
# |----|-------|-----|
# | 1  | Anna  | 18  |
# | 2  | Boris | 18  |


# -----------------------------
# 2. ИЗМЕНЕНИЕ ПОЛЯ
# -----------------------------

# Исходная модель с полем age:
class Profile(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

# ШАГ 1: Меняем тип поля age на FloatField
class Profile(models.Model):
    name = models.CharField(max_length=100)
    age = models.FloatField()  # изменено

# ШАГ 2: Создаём миграцию
# В терминале:
# python manage.py makemigrations

# Django создаёт файл миграции 0003_alter_age_field.py
# Содержимое миграции:
"""
operations = [
    migrations.AlterField(
        model_name='profile',
        name='age',
        field=models.FloatField(),
    ),
]
"""

# ШАГ 3: Применяем миграцию
# В терминале:
# python manage.py migrate

# Что происходит в базе:
# В PostgreSQL: ALTER TABLE изменяет тип колонки age на float
# В SQLite: создаётся временная таблица, данные копируются

# Результат таблицы:
# | id | name  | age  |
# |----|-------|------|
# | 1  | Anna  | 18.0 |
# | 2  | Boris | 25.0 |


# -----------------------------
# 3. УДАЛЕНИЕ ПОЛЯ
# -----------------------------

# Исходная модель:
class Profile(models.Model):
    name = models.CharField(max_length=100)
    age = models.FloatField()

# ШАГ 1: Удаляем поле age из модели
class Profile(models.Model):
    name = models.CharField(max_length=100)
    # age удалено

# ШАГ 2: Создаём миграцию
# В терминале:
# python manage.py makemigrations

# Django создаёт файл миграции 0004_remove_age_from_profile.py
# Содержимое миграции:
"""
operations = [
    migrations.RemoveField(
        model_name='profile',
        name='age',
    ),
]
"""

# ШАГ 3: Применяем миграцию
# В терминале:
# python manage.py migrate

# Что происходит в базе:
# ALTER TABLE Profile DROP COLUMN age
# Колонка и все данные в ней удаляются навсегда

# Результат таблицы:
# | id | name  |
# |----|-------|
# | 1  | Anna  |
# | 2  | Boris |

