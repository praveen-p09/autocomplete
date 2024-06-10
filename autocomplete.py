import tkinter as tk
from tkinter import StringVar, Listbox, Entry, END
import Levenshtein

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def autocomplete(self, prefix):
        def dfs(node, prefix):
            if node.is_end_of_word:
                results.append(prefix)
            for char, next_node in node.children.items():
                dfs(next_node, prefix + char)

        node = self.root
        results = []
        for char in prefix:
            if char not in node.children:
                return results
            node = node.children[char]
        dfs(node, prefix)
        return results

    def get_all_words(self):
        def dfs(node, prefix):
            if node.is_end_of_word:
                results.append(prefix)
            for char, next_node in node.children.items():
                dfs(next_node, prefix + char)

        results = []
        dfs(self.root, "")
        return results

def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

def get_suggestions(trie, prefix):
    suggestions = trie.autocomplete(prefix)
    if not suggestions:
        all_words = trie.get_all_words()
        suggestions = sorted(all_words, key=lambda word: Levenshtein.distance(word, prefix))[:10]
    return suggestions

# Read words from file
words = read_words_from_file('./words.txt')
print(f"Read {len(words)} words from file.")
print(f"Sample words: {words[:10]}")  # Print sample words to verify reading

# Insert words into the Trie
trie = Trie()
for word in words:
    trie.insert(word)

# Debug: Verify words are inserted correctly
print("Inserted words into the Trie.")

# GUI Application
def on_entry_change(*args):
    current_text = entry_var.get()
    last_word = current_text.split()[-1] if current_text.split() else ""
    suggestions = get_suggestions(trie, last_word)
    listbox.delete(0, END)
    for suggestion in suggestions:
        listbox.insert(END, suggestion)

def on_listbox_select(event):
    selection = listbox.curselection()
    if selection:
        current_text = entry_var.get()
        last_word = current_text.split()[-1] if current_text.split() else ""
        selected_suggestion = listbox.get(selection[0])
        new_text = current_text[:-len(last_word)] + selected_suggestion
        entry_var.set(new_text)
        entry.icursor(END)

root = tk.Tk()
root.title("Autocomplete and Autocorrect")

entry_var = StringVar()
entry_var.trace("w", on_entry_change)

entry = Entry(root, textvariable=entry_var, width=50)
entry.pack()

listbox = Listbox(root, width=50, height=10)
listbox.pack()
listbox.bind("<<ListboxSelect>>", on_listbox_select)

root.mainloop()
