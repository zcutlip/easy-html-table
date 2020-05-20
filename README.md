# Easy HTML Table

## Description

A package that takes in a Beautiful Soup object representing an HTML table, and parses it into a two-dimensional list representing the cells.

This handles the problem where some HTML table cells may span multiple rows or columns. In this case, each `<span>` is results in duplicated cell contents across the rows and columns as appropriate.

Each cell is a dictionary:
```
cell_contents = {
    "links": [],
    "text": "cell text"
}
```
