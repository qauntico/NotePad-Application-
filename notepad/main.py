from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from notepad import Ui_MainWindow
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtCore import QFileInfo
import sys


class notepad( QMainWindow, Ui_MainWindow ):
    def __init__(self):
        super().__init__()
        self.setupUi( self )
        self.actionSave.triggered.connect( self.save_file )
        self.actionNew.triggered.connect( self.execute )
        self.actionOpen.triggered.connect( self.open_file )
        self.actionPrint.triggered.connect( self.print_file )
        self.actionPrint_Previiew.triggered.connect( self.print_preview )
        self.actionExport_PDF.triggered.connect(self.export_pdf)

    def save_file(self):
        filename = QFileDialog.getSaveFileName( self, 'Save File', 'PDF Files (.pdf) ;; ')
        if filename[0]:
            with open( filename[0], 'w' ) as f:
                text = self.textEdit.toPlainText()
                f.write( text )
                QMessageBox.about( self, "About saved File", "File saving was a success" )


    def new_file(self):
        if not self.textEdit.document().isModified():
            return True
        reply = QMessageBox.warning( self, "New File", "Do you want to clear \n your text editor ?",
                                     QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel )
        if reply == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif reply == QMessageBox.StandardButton.Discard:
            return True
        else:
            return False

    def execute(self):
        if self.new_file():
            self.textEdit.clear()

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self,"Computer Files")
        if filename[0]:
            with open(filename[0], 'r') as r:
                text = r.read()
                self.textEdit.setPlainText(text)

    def print_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog()
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textEdit.print(printer)

    def print_preview(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.print)
        preview.exec()

    def print(self, printer):
        self.textEdit.print(printer)

    def export_pdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, 'Export PDF')
        if fn != '':
            if QFileInfo(fn).suffix() == '':
                fn += '.pdf'
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print(printer)

app = QApplication(sys.argv)
np = notepad()
np.show()
sys.exit( app.exec() )
