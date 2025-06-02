# ✅ Чек-лист: Создание кастомного пользователя в Django (Custom User Model)

---

## 📌 Когда использовать кастомную модель пользователя?

**Создавай кастомную модель пользователя, если:**
- Ты хочешь использовать `email` вместо `username`.
- Нужно добавить дополнительные поля (например, `age`, `country`, `phone`).
- Требуется изменить логику аутентификации/регистрации.
- Проект будет масштабироваться (лучше создать сразу, чем потом менять).

---

## 🧩 Шаг 1: Создание кастомной модели пользователя

```python
# models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

class CustomerUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomerUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomerUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
```

---

## ⚙️ Шаг 2: Настройка Django

### `settings.py`

```python
# указываем кастомную модель
AUTH_USER_MODEL = 'yourapp.CustomerUser'

# указываем backend, если логиним по email
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
```

---

## 🛠 Шаг 3: Создание формы регистрации

```python
# forms.py
from django import forms
from .models import CustomerUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomerUser
        fields = ('email', 'first_name', 'last_name', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
```

---

## 🌐 Шаг 4: Вью регистрации с login()

```python
# views.py
from django.contrib.auth import login
from django.views.generic.edit import FormView
from .forms import RegistrationForm

class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('catalog')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
```

---

## 🧪 Шаг 5: Сделать миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ⚠️ Важно: всё выше должно быть сделано **до первой миграции**, иначе потом будет сложно менять модель пользователя.