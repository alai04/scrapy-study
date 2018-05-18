class BookFeed:
    def __init__(self):
        self.books = {}

    def feed(self, item):
        if not item['book'] in self.books:
            self.books[item['book']] = []
        self.books[item['book']].append((int(item['sn']), item['chap'], item['lines']))

    def getBook(self, name):
        if self.books[name]:
            book = self.books[name]
            book.sort()
            fn = '%s.txt' % name
            with open(fn, 'w') as f:
                for chap in book:
                    print('======== %s ========' % chap[1], file=f)
                    for line in chap[2]:
                        print(line, file=f)
            return fn

    def getBookMarkdown(self, name):
        if self.books[name]:
            book = self.books[name]
            book.sort()
            fn = '%s.md' % name
            with open(fn, 'w') as f:
                for chap in book:
                    print(chap[1], file=f)
                    print('=' * len(chap[1]), file=f)
                    for line in chap[2]:
                        print(line, file=f)
                        print(file=f)
            return fn

    def getBookHTML(self, name):
        fn = self.getBookMarkdown(name)
        if fn:
            import markdown2

            fnOut = '%s.html' % name
            with open(fnOut, 'w') as f:
                f.write(markdown2.markdown_path(fn))
            return fnOut

    def getBookPDF(self, name):
        fn = self.getBookHTML(name)
        if fn:
            from weasyprint import HTML, CSS
            from weasyprint.fonts import FontConfiguration

            html = HTML(fn)
            css = CSS(string='body { font-family: "Microsoft YaHei" }')
            fnOut = '%s.pdf' % name
            html.write_pdf(fnOut, stylesheets=[css])
            return fnOut

    def getAllBooks(self):
        for name in self.books.keys():
            self.getBookHTML(name)
