from django.shortcuts import render, redirect, get_object_or_404 
from .models import Book, Comment
from django.views import  View
from .forms import CommentForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def books(request):
    books = Book.objects.all()
    query = request.GET.get('q')
    if query:
        books = books.filter(title__icontains=query)
    context = {'books': books}
    return render(request=request, template_name='books.html', context=context)


@login_required
def book_detail(request, id):
    book = Book.objects.get(id=id)
    form = CommentForm()
    context = {'book': book, 'form': form}
    return render(request, 'book_detail.html', context)


@login_required
def book_comments(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        user = request.user
        book = Book.objects.get(id=id)
        if form.is_valid():
            Comment.objects.create(
                user=user,
                book=book,
                text=form.cleaned_data['text'],
                star=form.cleaned_data['star'],
            )
            messages.success(request, 'Comment added successfully')
            return redirect('book_detail', id=id)
        return render(request, 'book_detail', context={'book': book, 'form': form})


@login_required
def book_delete(request, book_id, comment_id):
    book = get_object_or_404(Book , id=book_id)
    comment = get_object_or_404(Comment, id=comment_id, book=book)
    comment.delete()
    messages.success(request, 'Comment deleted successfully')
    return redirect('book_detail', id=book_id)


@login_required
def comment_edit(request, book_id, comment_id):
    book = get_object_or_404(Book, pk=book_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('book_detail' ,id=book.id)  # Replace with your success URL

    return render(request, 'comment_edit.html', {'form': form, 'book': book, 'comment': comment})


@login_required
def book_edit(request, book_id):
    # Your editing logic here
    # ...

    # Redirect to the detail view of the edited book
    return redirect('book-detail', pk=book_id)

# @login_required
# def search_book(request):
#     books = Book.objects.all()
#     query = request.GET.get('q')
#     if query:
#         books = books.filter(title__icontains=query)
#     return render(request, 'books.html', {'books': books})


from django.db import models

# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     cover_pic = models.ImageField(upload_to='book_covers/')
    
#     def __str__(self):
#         return self.title

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from .models import Book  # Ensure this import does not cause a circular dependency

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('books')  
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})
@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('books')
    return render(request, 'delete_book.html', {'book': book})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})
