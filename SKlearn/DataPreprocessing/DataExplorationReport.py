from fpdf import FPDF, HTMLMixin
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import shutil


title = 'Data exploration report'


class PDF(FPDF, HTMLMixin):


    def header(self):
        # font
        self.set_font('helvetica', 'B', 15)
        # Calculate width of title and position
        title_w = self.get_string_width(title) + 6
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)
        # colors of frame, background, and text
        self.set_draw_color(0, 80, 180)  # border = blue
        self.set_fill_color(0, 80, 180)  # background = yellow
        self.set_text_color(255, 255, 255)  # text = red
        # Thickness of frame (border)
        self.set_line_width(1)
        # Title
        self.cell(title_w, 10, title, border=1, ln=1, align='C', fill=1)
        # Line break
        self.ln(10)

    # Page footer
    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # set font
        self.set_font('helvetica', 'I', 8)
        # Set font color grey
        self.set_text_color(169, 169, 169)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    # Adding chapter title to start of each chapter
    def chapter_title(self, ch_num, ch_title, link):
        # Set link location
        self.set_link(link)
        # set font
        self.set_font('helvetica', '', 20)
        # background color
        self.set_fill_color(192, 192, 192)
        # Chapter title
        chapter_title = f'Chapter {ch_num} : {ch_title}'
        self.cell(0, 10, chapter_title, ln=1, fill=1)
        # line break
        self.ln()

    # Chapter content
    def chapter_body(self, name):
        # read text file
        #         with open(name, 'rb') as fh:
        #             txt = fh.read().decode('latin-1')
        #         # set font
        self.set_font('times', '', 12)
        # insert text
        self.multi_cell(0, 5, name)
        # line break
        self.ln()
        # end each chapter
        self.set_font('times', 'I', 12)

    #         self.cell(0, 5, 'END OF CHAPTER')

    def print_chapter(self, ch_num, ch_title, name, link):
        self.add_page()
        self.chapter_title(ch_num, ch_title, link)
        self.chapter_body(name)

    def fill_outliers_images(self, df,filename,pdf):
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
        foldernamePath = f"{filename}" + date_time
        print(f"outliers/{foldernamePath}")
        os.makedirs(f"outliers/{foldernamePath}")
        for column, coltype in df.dtypes.iteritems():
            #             print(coltype)
            if coltype != "object":
                fig, ax = plt.subplots()
                sns.boxplot(data=df, x=df[column].values, ax=ax)
                imagePath = 'outliers/' + f'{foldernamePath}' + '/' + f'{column}.png'
                pdf.write_html(f"""<h2>{column} Column Box PLOT Diagram</h2>""")
                plt.savefig(imagePath)
                #  pdf.image(imagePath, x = -0.5, w = pdf.w + 1)
                pdf.image(imagePath, h=75, w=170)
                plt.clf()
                os.remove(imagePath)
        shutil.rmtree('outliers/' + f'{foldernamePath}', ignore_errors=False, onerror=None)

    def fill_histogram_images(self, df,filename,pdf):
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
        foldernamePath = f"{filename}" + date_time
        os.makedirs(f"histogram/{foldernamePath}")
        for column, coltype in df.dtypes.iteritems():
            #             print(coltype)
            if coltype != "object":
                fig, ax = plt.subplots()
                plt.hist(df[column])
                imagePath = 'histogram/' + f'{foldernamePath}' + '/' + f'{column}.png'
                pdf.write_html(f"""<h3>{column} Column Histogram Diagram</h3>""")
                plt.savefig(imagePath)
                #  pdf.image(imagePath, x = -0.5, w = pdf.w + 1)
                pdf.image(imagePath, h=85, w=170)
                plt.clf()
                os.remove(imagePath)
        shutil.rmtree('histogram/' + f'{foldernamePath}', ignore_errors=False, onerror=None)


class PDFCreation():
    def __init__(self,path):
        self.path = path
        pdf = PDF('P', 'mm', 'Letter')
        self.pdf =pdf
    def startUp(self):
        self.df = pd.read_csv(self.path)
        print("path",self.path)
        x = self.path.split(".")[1] .split("\\")
        # print("x ", x )
        self.filename = x[len(x) - 1]
        print("self.filename", self.filename)
        filename = self.filename

        # metadata
        self.pdf.set_title(title)
        self.pdf.set_author('Data scince')

        # Create Links
        ch1_link = self.pdf.add_link()
        ch2_link = self.pdf.add_link()
        ch3_link = self.pdf.add_link()
        ch4_link = self.pdf.add_link()

        # Set auto page break
        self.pdf.set_auto_page_break(auto=True, margin=15)

        # Add Page
        self.pdf.add_page()
        dirname = os.path.dirname(__file__)
        self.pdf.image(dirname+'/background_image.jpg', x=-0.5, w=self.pdf.w + 1)

        # Attach Links
        self.pdf.cell(0, 10, 'Chapter 1 : Data Information', ln=1, link=ch1_link)
        self.pdf.cell(0, 10, 'Chapter 2 : Missing Values', ln=1, link=ch2_link)
        self.pdf.cell(0, 10, 'Chapter 3 : Columns outliers visualization', ln=1, link=ch3_link)
        self.pdf.cell(0, 10, 'Chapter 4 : Columns Histogram visualization', ln=1, link=ch4_link)
        column_data = ""
        missingColumn_data = ""
        self.pdf.print_chapter(1, 'Data Information', '', ch1_link)
        for colname, coltype in self.df.dtypes.iteritems():
            data = f"<tr> <td>{colname}</td><td>{self.df[colname].notnull().sum()}</td><td>{coltype}</td></tr>"
            missingColumn_data += f"<tr> <td>{colname}</td><td>{self.df[colname].isnull().sum()}</td></tr>"
            column_data = column_data + data
            # print(column_data)
        print("column_data")
        self.pdf.write_html("<h1>Data Information Table</h1> ")
        self.pdf.write_html("""<h1>Data Information Table</h1> <section> <table width="100%"> <thead>
            <tr><th align="left" width="40%">Column Name</th>
              <th align="left" width="30%">Count</th> <th align="left" width="30%">Data type</th>
            </tr></thead><tbody>""" + column_data + """ </tbody></table></section>""")
        self.pdf.print_chapter(2, 'Missing Values', '', ch2_link)
        self.pdf.write_html("""<h1>Missing Values Table</h1><section><table width="100%"> <thead> <tr>
          <th align="left" width="50%">Column Name</th> <th align="left" width="50%">Null Count</th>
        </tr></thead> <tbody>""" + missingColumn_data + """ </tbody> </table> </section> """)
        self.pdf.print_chapter(3, 'Columns outliers visualization', '', ch3_link)
        self.pdf.fill_outliers_images(self.df,filename,self.pdf)
        self.pdf.print_chapter(4, 'Columns Histogram visualization', '', ch4_link)
        self.pdf.fill_histogram_images(self.df,filename,self.pdf)
        dirname = os.path.dirname(__file__)
        finalOutputFilePath = f'{dirname}/downloadedFiles/'
        self.pdf.output(f'{finalOutputFilePath}/{self.filename}.pdf')
        return f'{finalOutputFilePath}{self.filename}.pdf'