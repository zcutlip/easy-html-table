import re


class EasyHtmlTable:
    def __init__(self, table, skip_header=False):
        self.bs_table = table

        self._skip_header = skip_header
        self.table = self._parse_table(table, skip_header=skip_header)

    @property
    def headers(self):
        _headers = None
        if not self._skip_header:
            hrow = self.contents[0]
            _headers = [x["text"] for x in hrow]

        return _headers

    def _preprocess_table(self, _table, skip_header=False):
        """preprocess table to generate
        <table size> grid of rowspan,colspan metadata
        """
        table = []
        col_count = 0
        line_count = 0

        _find = "td" if skip_header else re.compile(r'(td|th)')

        rows = _table.find_all("tr")
        for rownum, row in enumerate(rows):
            cell_list = row.find_all(_find)
            if not cell_list or len(cell_list) < 1:
                continue
            line_count += 1
            table.append([])
            for cell in cell_list:
                colspan = int(cell.get('colspan', 1))
                if colspan < 1:
                    colspan = 1
                rowspan = int(cell.get('rowspan', 1))
                if rowspan < 1:
                    rowspan = 1
                cell_info = {'colspan': colspan,
                             'rowspan': rowspan, 'cell': cell}
                table[-1].append(cell_info)
            if len(cell_list) > col_count:
                col_count = len(cell_list)

        return (col_count, line_count, table)

    def _parse_table(self, _table, skip_header=False):
        col_count, line_count, table = self._preprocess_table(
            _table, skip_header=skip_header)

        colnum = 0

        while colnum < col_count:
            linenum = 0
            while linenum < line_count:
                # repair table
                # some rows could be short
                while colnum >= len(table[linenum]):
                    table[linenum].append('')
                cell = table[linenum][colnum]

                if not isinstance(cell, dict):
                    # we've already fixed this cell up
                    linenum += 1
                    continue

                for i_colspan in range(colnum, colnum + cell['colspan']):
                    # iterate over each column from colnum to colnum+colspan
                    # eg. if a cell on column 2 has a colspan of 3
                    # we iterate over columns 2, 3, and 4
                    for i_rowspan in range(linenum, linenum + cell['rowspan']):
                        # same sort of iteration but for rows
                        # so if, e.g., a cell spanned a fat, 2x2 square
                        # we'd iterate over all four of that cell's "cells"
                        if i_colspan == colnum and i_rowspan == linenum:
                            # we're at the origin cell where the colspan and/or rowspan was declared
                            # nothing to do here
                            continue
                        col_count, line_count = self._add_cell(
                            table, i_rowspan, i_colspan, cell['cell'], col_count, line_count)
                # replace cell metadata dict
                # with the actual cell object
                table[linenum][colnum] = cell['cell']
                linenum += 1

            colnum += 1
        return table

    def _add_cell(self, table, linenum, colnum, cell, col_count, line_count):
        # we're filling out the table to account for colspans & rowspans
        # we might be adding cells to rows that haven't been visited yet
        while len(table) <= linenum:
            # e.g., if a rowspan extends down past the last <tr>
            # we need to add a new row
            table.append([])
            line_count += 1
        while len(table[linenum]) < colnum:
            table[linenum].append('')
        table[linenum].insert(colnum, cell)
        if len(table[linenum]) > col_count:
            # did we grow the current line beyond the known
            # maximum columns?
            col_count = len(table[linenum])

        return col_count, line_count

    @property
    def contents(self):
        if hasattr(self, "_contents"):
            return self._contents
        _contents = []

        for y in range(len(self.table)):
            row = self.table[y]
            content_row = []
            for x in range(len(row)):
                celltext = ''
                cell = row[x]
                try:
                    celltext = cell.text.strip()
                except AttributeError:
                    pass
                # try to convert to string but some unicode will fail
                try:
                    celltext = str(celltext)
                except Exception:
                    pass
                if not celltext:
                    continue
                cellcontents = {}
                cellcontents["text"] = celltext
                try:
                    links = cell.find_all("a")
                except AttributeError:
                    links = []

                cellcontents["links"] = links
                content_row.append(cellcontents)
            _contents.append(content_row)

        self._contents = _contents
        return self._contents
