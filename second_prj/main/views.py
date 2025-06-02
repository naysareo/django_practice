from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, DetailView, ListView, TemplateView, UpdateView
from .models import Book, Author, Genre
from .forms import BookForm, AuthorForm, TestBookForm, GenresForm
from django.urls import reverse_lazy, reverse
import logging
UserCreationForm


# logger = logging.getLogger("second_prj")
# logger.setLevel(logging.INFO)
#
# formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%d.%m.%Y %H:%M:%S")
#
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
#
# logger.addHandler(console_handler)


def index(request):
    books = Book.objects.select_related('author')

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            form.save()
            return redirect("/")
    else:
        form = BookForm()

    context = {"books": books,
               "form": form}
    return render(request, "main/index.html", context)


# todo добавил image (ImageField) поэтому необходимо указать в form(request.FILES)
class IndexView(ListView):
    model = Book
    template_name = "main/index.html"
    context_object_name = "books"

    def get(self, request, *args, **kwargs):
        if 'test_btn' in request.GET:
            logging.info(f"test_btn: {request.method}")
        else:
            logging.info(f"test_btn: NONE")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = BookForm()
        return context

    def post(self, request, *args, **kwargs):
        logging.info('request_q=%s', request.POST, request.FILES)
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/author')
        return redirect('/genre')



class TestBookView(FormView):
    form_class = TestBookForm
    template_name = "main/test.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            author = form.cleaned_data['author']
            genre = form.cleaned_data['genres']
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            book = Book.objects.create(author=author, title=title, text=text)
            book.genres.set([genre])
            logging.info('author=%s, genre=%s, title=%s, text=%s', author, genre, title, text)


        return HttpResponse("OK")


def detail_view(request, pk):
    book = get_object_or_404(Book, id=pk)

    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            print(f"22222 {form.cleaned_data}")
            Author.objects.create(**form.cleaned_data)
            return redirect('book/')

    else:
        form = AuthorForm()

    if "clicked" in request.GET:
        return HttpResponse("Button works!")
    search_query = request.GET


    logging.info(search_query)
    return render(request, "main/detail.html", {"book": book,
                                                "form": form})



# class DetailViewBook(DetailView):
#     model = Book
#     template_name ="main/detail.html"
#     context_object_name = "book"
#
#     def get(self, request, *args, **kwargs):
#         if "clicked" in request.GET:
#             return HttpResponse("Yes it is")
#         else:
#             return super().get(request, *args, **kwargs)


class AuthorCreateView(FormView):
    template_name = "main/author.html"
    form_class = AuthorForm
    success_url = reverse_lazy("genres")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

@login_required(login_url='book')
def genres_view(request):
    if request.method == 'POST':
        form = GenresForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/book/")
    else:
        form = GenresForm()

    return render(request, 'main/genres.html', {'form': form})


class GenresCreateView(PermissionRequiredMixin, FormView):
    template_name = "main/genres.html"
    form_class = GenresForm
    success_url = reverse_lazy("book")
    login_url = reverse_lazy('book')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "main/index.html"
    context_object_name = "update_book"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        book = form.save(commit=False)
        author = form.cleaned_data["author"]
        genre = form.cleaned_data["genres"]
        title = form.cleaned_data["title"]
        text = form.cleaned_data["text"]

        book.author = author
        book.genre = genre
        book.title = title
        book.text = text
        book.save()
        logging.info(f"Form updating... | {self.kwargs}")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            logging.info("Form is valid!")
        return HttpResponse("Form is valid!")

    def get(self, request, *args, **kwargs):
        if "test_get_btn" in request.GET:
            return HttpResponse("Approve")
        return super().get(request, *args, **kwargs)



def update_book_fbv(request, pk):
    update_book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookForm(request.POST, instance=update_book)
        if form.is_valid():
            form.save()
            return redirect(reverse('book'))
        else:
            return HttpResponse("From invalid!")

    else:
        form = BookForm(instance=update_book)

    if "test_get_btn" in request.GET:
        get_req = request.GET.get("test_get_btn2")
        logging.info(f"ger_req = {get_req}")
        return HttpResponse(f"get_req successfully receive")

    context = {"update_book": update_book,
               "form": form}

    return render(request, "main/index.html", context)



class BaseHTML(TemplateView):
    template_name = "main/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_var"] = my_var = [
            {'name': 'Класс A'},
            {'name': 'Класс B'},
            {'name': 'Класс C'},
        ]
        return context


class NavbarHTML(TemplateView):
    template_name = "main/navbar.html"


class FooterHTML(TemplateView):
    template_name = "main/footer.html"


class HomeHTML(TemplateView):
    template_name = "main/home.html"


class AboutHTML(TemplateView):
    template_name = "main/about.html"
