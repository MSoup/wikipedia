import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django import forms
from django.http import HttpResponse


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists, it throws an error
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        raise Exception("File exists")
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


class NewPost(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    body = forms.CharField(label='Body', max_length=1000)