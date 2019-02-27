import PyPDF2

with open('pdf2txt_demo.pdf', 'rb') as pdfFileObj:
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    for i in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        print(pageObj.extractText())


