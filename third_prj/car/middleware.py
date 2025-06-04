# myapp/middleware.py
from django.http import HttpResponse


class MyCustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # сохраняем ссылку на следующий уровень (view или следующий middleware)

    def __call__(self, request):
        print(f"[Middleware] {request.method} {request.path}")
        response = self.get_response(request)  # вызываем view (или следующий middleware)
        return response

    def process_request(self, request):
        print("→ process_request")
        return None  # или HttpResponse("Заблокировано")

    def process_view(self, request, view_func, view_args, view_kwargs):
        print(f"→ process_view: будет вызвана {view_func.__name__}")
        return None

    def process_template_response(self, request, response):
        print("→ process_template_response")
        response.context_data['extra'] = 'доп.данные'
        return response

    def process_response(self, request, response):
        print("→ process_response")
        return response

    # def process_exception(self, request, exception):
    #     print(f"→ Ошибка: {exception}")
    #     return HttpResponse("Произошла ошибка на сервере")

# → process_request
# → process_view
# → view
#     → (если ошибка) process_exception
#     → (если TemplateResponse) process_template_response
# → process_response

