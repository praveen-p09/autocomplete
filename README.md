# Autocomplete and Autocorrect GUI Application

This project implements an autocomplete and autocorrect feature using a Trie data structure. It leverages the Levenshtein distance algorithm to provide suggestions for misspelled words. The application is built with a graphical user interface (GUI) using the `tkinter` library in Python.

## Features

- **Autocomplete**: Suggests completions for a given prefix.
- **Autocorrect**: Suggests corrections for misspelled words using the Levenshtein distance.
- **GUI**: Simple and interactive interface for typing and selecting suggestions.

## Prerequisites

- Python 3.x
- `tkinter` library (comes with standard Python installation)
- `python-Levenshtein` library for calculating Levenshtein distance

## Installation

1. Install `python-Levenshtein`:
```bash
pip install python-Levenshtein
```
2. Clone the repository and navigate to the project directory.
3. Ensure you have a file named words.txt in the same directory as the script. This file should contain a list of words, one per line.

## Usage

Run the script using python 
```bash
python autocomplete.py
```
