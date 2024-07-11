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
