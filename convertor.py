import sys
import os

in_file = "test.docx"
out_file = "temp.pdf"

if sys.platform.startswith('linux'):
    print("Running on Linux")
    import subprocess
    try:
        subprocess.call(['soffice',
                         '--headless',
                         '--convert-to', 'pdf', '--outdir', os.getcwd(), in_file])
    except Exception as e:
        print("Error:", e)

elif sys.platform.startswith('win'):
    print("Running on Windows")
    import comtypes.client

    wdFormatPDF = 17

    try:
        word = comtypes.client.CreateObject('Word.Application')
        doc = word.Documents.Open(os.path.join(os.getcwd(), in_file))
        doc.SaveAs(os.path.join(os.getcwd(), out_file), FileFormat=wdFormatPDF)
        doc.Close()
        word.Quit()
        print("Converted successfully")
    except Exception as e:
        print("Error:", e)
else:
    print("Unsupported operating system")