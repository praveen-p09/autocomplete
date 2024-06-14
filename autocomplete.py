import tkinter as tk
from tkinter import StringVar, Listbox, Entry, END
import Levenshtein

class TrieNode:        # Trie Node class
    def __init__(self):
        self.children = {} # Dictionary to store children nodes
        self.is_end_of_word = False # Flag to indicate end of word

class Trie:
    def __init__(self):  # Initialize the Trie with root node
        self.root = TrieNode()

    def insert(self, word):  # Insert a word into the Trie
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word): # Search a word in the Trie
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def autocomplete(self, prefix): # Get all words with the given prefix
        def dfs(node, prefix):  # Depth First Search to get all words with the given prefix
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

    def get_all_words(self):  # Get all words in the Trie
        def dfs(node, prefix): # Depth First Search to get all words in the Trie
            if node.is_end_of_word:
                results.append(prefix)
            for char, next_node in node.children.items():
                dfs(next_node, prefix + char)

        results = []
        dfs(self.root, "")
        return results

def read_words_from_file(file_path):  # Read words from file
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

def get_suggestions(trie, prefix):  # Get suggestions for the given prefix
    suggestions = trie.autocomplete(prefix)
    if not suggestions:
        all_words = trie.get_all_words()
        suggestions = sorted(all_words, key=lambda word: Levenshtein.distance(word, prefix))[:10]  # Get top 10 words with minimum Levenshtein distance
    return suggestions

words = read_words_from_file('./words.txt') # Read words from file
print(f"Read {len(words)} words from file.")
print(f"Sample words: {words[:10]}")  # Print sample words to verify reading

trie = Trie() # Initialize the Trie
for word in words:  
    trie.insert(word)  # Insert words into the Trie
 
print("Inserted words into the Trie.") # Debug: Verify words are inserted correctly

# GUI Application
def on_entry_change(*args):
    current_text = entry_var.get()               # Get current text in the entry
    last_word = current_text.split()[-1] if current_text.split() else "" # Get last word in the text
    suggestions = get_suggestions(trie, last_word)  # Get suggestions for the last word
    listbox.delete(0, END)  # Clear the listbox
    for suggestion in suggestions:  # Insert suggestions into the listbox
        listbox.insert(END, suggestion) 

def on_listbox_select(event): # Select a suggestion from the listbox
    selection = listbox.curselection() 
    if selection:
        current_text = entry_var.get() # Get current text in the entry
        last_word = current_text.split()[-1] if current_text.split() else ""  # Get last word in the text
        selected_suggestion = listbox.get(selection[0]) 
        new_text = current_text[:-len(last_word)] + selected_suggestion # Replace last word with the selected suggestion
        entry_var.set(new_text)
        entry.icursor(END)

root = tk.Tk()  # Create the root window
root.title("Autocomplete and Autocorrect") # Set the title of the window

entry_var = StringVar()
entry_var.trace("w", on_entry_change) # Trace the changes in the entry widget

entry = Entry(root, textvariable=entry_var, width=50)
entry.pack() # Pack the entry widget    

listbox = Listbox(root, width=50, height=10)
listbox.pack() # Pack the listbox widget
listbox.bind("<<ListboxSelect>>", on_listbox_select) # Bind the listbox select event

root.mainloop() # Start the main event loop
