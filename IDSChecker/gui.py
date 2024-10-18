import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Label
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import webbrowser
import IDSChecker.checker
from IDSChecker.checker import AversioHtml
import ifcopenshell
import ifctester as tst
from ifctester import ids, reporter
from ifctester.ids import Specification, Ids
from ifcopenshell.util.file import IfcHeaderExtractor


class CheckerGUI(tk.Tk):
     def __init__(self):
        super().__init__()
        self.title("AVERSIO IFC Checker")
        self.geometry("600x300")
        self.iconbitmap(".\\IDSChecker\\bimchecker.ico")
        self.resizable(True, True)
        self.grid()
        self.ifc_path=tk.StringVar()
        self.ids_path=tk.StringVar()
        self.report_path=tk.StringVar()
        self.reporttemplate_path = tk.StringVar()
        self.report_open=tk.StringVar()
        self.create_funcs()
        self.runchecks()
        self.showresults()


     def select_ifcfile(self):
        filetypes = (
            ('IFC files', '*.ifc'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='./IFC examples',
            filetypes=filetypes)
        return filename

     def update_ifc_path(self):
        filepath = self.select_ifcfile()
        if filepath:
            self.ifc_path.set(filepath)

     def select_idsfile(self):
        filetypes = (
            ('IDS files', '*.ids'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='./IDS examples',
            filetypes=filetypes)
        return filename

     def update_ids_path(self):
        filepath = self.select_idsfile()
        if filepath:
            self.ids_path.set(filepath)

     def select_reporttemp(self):
        filetypes = (
            ('HTML files', '*.html'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='./Report templates',
            filetypes=filetypes)
        return filename

     def update_reporttemplate_path(self):
        filepath = self.select_reporttemp()
        if filepath:
            self.reporttemplate_path.set(filepath)

     def select_report(self):
        filetypes = (
            ('HTML files', '*.html'),
            ('All files', '*.*')
        )
        filename = fd.asksaveasfilename(
            title='Create or overwrite a file',
            defaultextension=".html",
            initialdir=os.path.join(os.path.expanduser("~"), "Documents"),
            filetypes=filetypes)
        return filename

     def update_report_path(self):
        filepath = self.select_report()
        if filepath:
            self.report_path.set(filepath)

     def checkids(self,ifc_file,ids_file,report_file,reptemplatepath):
        my_ifc = ifcopenshell.open(ifc_file)
        my_idss = ids.open(ids_file)
        my_idss.validate(my_ifc)
        engine = AversioHtml(my_idss)
        engine.report()
        extractor = IfcHeaderExtractor(ifc_file)
        header_info = extractor.extract()
        engine.results["ifcdescription"]=header_info.get("description")
        engine.results["ifcname"]=header_info.get("name")
        engine.results["ifctimestamp"]=header_info.get("time_stamp")
        engine.results["ifcfilepath"]=ifc_file
        engine.sortby_status()
        engine.to_file(report_file, reptemplatepath)
        # Assign your output to the OUT variable.
        # reporter.Console(my_idss).report()
        return(reporter.Console(my_idss).report())


     def create_funcs(self):
        self.ifcfile = tk.Button(self, text='IFC ke kontrole', command=self.update_ifc_path, anchor="w")
        self.ifcfile.grid(row =2, column =1, padx=5, pady=5,sticky='nesw')
        self.ifcfilename_label = tk.Label(self, textvariable=self.ifc_path)
        self.ifcfilename_label.grid(row=2,column=2,sticky=tk.W, padx=5, pady=5)
        self.idsfile = tk.Button(self, text='Kontrolní IDS', command=self.update_ids_path, anchor="w")
        self.idsfile.grid(row=3, column=1, padx=5, pady=5,sticky='nesw')
        self.idsfilename_label = ttk.Label(self, textvariable=self.ids_path)
        self.idsfilename_label.grid(row=3,column=2,sticky=tk.W, padx=5, pady=5)
        self.reporttemplate = tk.Button(self, text='Šablona výstupu kontroly', command=self.update_reporttemplate_path, anchor="w")
        self.reporttemplate.grid(row=4,column=1, padx=5, pady=5,sticky='nesw')
        self.reporttemplate_label = ttk.Label(self, textvariable=self.reporttemplate_path)
        self.reporttemplate_label.grid(row=4,column=2,sticky=tk.W, padx=5, pady=5)
        self.reportfile = tk.Button(self, text='Soubor reportu', command=self.update_report_path, anchor="w")
        self.reportfile.grid(row=5,column=1, padx=5, pady=5,sticky='nesw')
        self.report_label = tk.Label(self, textvariable=self.report_path)
        self.report_label.grid(row=5,column=2,sticky=tk.W, padx=5, pady=5)
        langu = ['Czech','English','Slovak','German']
        self.lango=tk.StringVar()
        self.lango.set(langu[0])
        self.language = tk.OptionMenu(self,self.lango,*langu)
        self.language.grid(row=1,column=1, padx=5, pady=5,sticky='nesw')
        self.languag = tk.Button(self, text="Změna na vybraný jazyk", command=self.update_lang, anchor="w" )
        self.languag.grid(row=1,column=2, padx=5, pady=5,sticky='nesw')

     def runchecks(self):
        self.runcheck = tk.Button(self,activebackground = "green",height=3, text='Spustit kontrolu', command=lambda: self.checkids(self.ifc_path.get(),self.ids_path.get(),self.report_path.get(),self.reporttemplate_path.get()))
        self.runcheck.grid(row=6,rowspan=2,column=1, padx=5, pady=50,sticky='nesw')

     def showresults(self):
        self.showres = tk.Button(self, text='Zobrazit protokol',height=3, command=lambda:webbrowser.open('file://'+self.report_path.get(),new=2))
        self.showres.grid (row=6, rowspan=2, column=2, padx=5, pady=50,sticky='nesw')

     def update_lang(self):
        self.lang = self.lango.get()
        if self.lang == 'Czech':
           self.ifcfile.config(text='IFC ke kontrole')
           self.idsfile.config(text='Kontrolní IDS')
           self.reporttemplate.config(text='Šablona výstupu kontroly')
           self.reportfile.config(text='Soubor reportu')
           self.languag.config(text='Nastavit jazyk')
           self.runcheck.config(text='Spustit kontrolu')
           self.showres.config(text='Zobrazit protokol')
        elif self.lang == 'English':
           self.ifcfile.config(text='IFC File')
           self.idsfile.config(text='IDS File')
           self.reporttemplate.config(text='Report template')
           self.reportfile.config(text='Report file')
           self.languag.config(text='Set language')
           self.runcheck.config(text='Run check')
           self.showres.config(text='Show report')
        elif self.lang == 'Slovak':
           self.ifcfile.config(text='IFC súbor')
           self.idsfile.config(text='IDS súbor')
           self.reporttemplate.config(text='Šablóna kontrolné správy')
           self.reportfile.config(text='Súbor kontrolné správy')
           self.languag.config(text='Nastaviť jazyk')
           self.runcheck.config(text='Spustiť kontrolu')
           self.showres.config(text='Zobraziť správu')
        elif self.lang == 'German':
           self.ifcfile.config(text='IFC Datei')
           self.idsfile.config(text='IDS Datei')
           self.reporttemplate.config(text='Berichtsvorlage')
           self.reportfile.config(text='Berichtsdatei')
           self.languag.config(text='Sprache einstellen')
           self.runcheck.config(text='Prüfung starten')
           self.showres.config(text='Bericht anzeigen')                         


