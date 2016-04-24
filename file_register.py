import os
import hashlib


class Book(object):
    
    fst1 = "\t\t<dict>\n\t\t\t<key>Inserted-By-iBooks</key>\n\t\t\t<true/>\n\t\t\t<key>Name</key>\n\t\t\t<string>"
    fst2 = "</string>\n\t\t\t<key>Package Hash</key>\n\t\t\t<string>"
    fst3 = "</string>\n\t\t\t<key>Path</key>\n\t\t\t<string>"
    fst4 = "</string>\n\t\t\t<key>importDate</key>\n\t\t\t<date>2016-04-01T07:53:06Z</date>\n"
    lst = "\t\t</dict>\n"
    
    def __init__(self, sttmp):
        self.name = sttmp[:-4]
        self.path = sttmp
        self.get_hash()
    
    def export_xml(self):
        return self.fst1 + self.name + self.fst2 + self.hash + self.fst3 + self.path + self.fst4 + self.lst
    
    def get_hash(self):
        self.hasher = hashlib.md5()
        with open(self.path, 'rb') as f:
            buf = f.read()
            self.hasher.update(buf)
            self.hash = self.hasher.hexdigest().upper()
        

class Manager(object):
    
    header ="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n<plist version=\"1.0\">\n<dict>\n\t<key>Books</key>\n\t<array>\n"
    footer ="\t</array>\n</dict>\n</plist>"
    book_list = []
    
    def __init__(self, plist = "Purchases.plist"):
        self.scan()
        self.export()
        
    def scan(self):
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                sttmp = os.path.join(root, name)[2:]
                if not ".pdf" in sttmp:
                    continue
                self.book_list.append(Book(sttmp))
    
    def export(self):
        with open("Purchases.plist", "w")as f:
            f.write(self.header)
            for book in self.book_list:
                f.write(book.export_xml())
            f.write(self.footer)
Manager()
            
        
