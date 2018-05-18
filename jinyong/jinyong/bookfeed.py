import markdown2
from weasyprint import HTML, CSS
from .settings import BOT_NAME


class BookFeed:
    def __init__(self):
        self.books = {}

    def feed(self, item):
        self.books.setdefault(item['book'], []).append((int(item['sn']), item['chap'], item['lines']))

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
                    print('# %s' % chap[1], file=f)
                    for line in chap[2]:
                        print(line, file=f)
                        print(file=f)
            return fn

    def getBookHTML(self, name):
        fn = self.getBookMarkdown(name)
        if fn:
            fnOut = '%s.html' % name
            with open(fnOut, 'w') as f:
                f.write('<html>\n<head>\n<title>%s</title>\n</head>\n<body>\n' % name)
                f.write(markdown2.markdown_path(fn))
                f.write('</body>\n</html>\n')
            return fnOut

    def getBookPDF(self, name):
        fn = self.getBookHTML(name)
        if fn:
            html = HTML(fn, encoding='utf8')
            css = CSS(string='body { font-family: "Microsoft YaHei" }')
            fnOut = '%s.pdf' % name
            html.write_pdf(fnOut, stylesheets=[css])
            return fnOut

    def getAllBooks(self):
        for name in self.books.keys():
            self.getBook(name)

    def getAllBooks1Markdown(self):
        fn = '%s.md' % BOT_NAME
        with open(fn, 'w') as f:
            for name in self.books.keys():
                print('# %s' % name, file=f)
                for chap in sorted(self.books[name]):
                    print('## %s' % chap[1], file=f)
                    for line in chap[2]:
                        print(line, file=f)
                        print(file=f)
        return fn

    def getAllBooks1HTML(self):
        fn = self.getAllBooks1Markdown()
        if fn:
            fnOut = '%s.html' % BOT_NAME
            with open(fnOut, 'w') as f:
                f.write('<html>\n<head>\n<title>%s</title>\n</head>\n<body>\n' % BOT_NAME)
                f.write(markdown2.markdown_path(fn))
                f.write('</body>\n</html>\n')
            return fnOut

    def getAllBooks1PDF(self):
        fn = self.getAllBooks1HTML()
        if fn:
            html = HTML(fn, encoding='utf8')
            css = CSS(string='body { font-family: "Microsoft YaHei" }')
            fnOut = '%s.pdf' % BOT_NAME
            html.write_pdf(fnOut, stylesheets=[css])
            return fnOut
