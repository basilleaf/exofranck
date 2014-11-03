import pdflabels
import csv

def make_labels():
    pdf = pdflabels.PDFLabel('Avery-5160')
    pdf.add_page()

    WIDTH, HEIGHT = 66.675, 25.4
    with open('short_urls.csv') as csvfile:
        reader = csv.reader(csvfile)
        # GRR. I need to shift everything up a little bit.
        delta_y = -1
        for short_url,long_url,count in reader:
            path = long_url.replace('http://exoplanets.seti.org/','')
            pdf.add_label('')
            pdf.set_label_xy()
            pdf.image('qrcodes/%s.png'%path,
                      pdf.x+2, pdf.y+3+delta_y,
                      pdf.height-6, pdf.height-6)

            logo_width = 15
            logo_height = logo_width/1.612
            logo_offset = (HEIGHT-logo_height)/2
            pdf.image('SETI_logo_CMYK.png',
                      pdf.x+WIDTH-logo_width-2, pdf.y+logo_offset+delta_y,
                      logo_width, logo_width/1.612)

            text_top = pdf.y+9.4

            pdf.set_xy(pdf.x+pdf.height-3, text_top+delta_y)
            star_name = path.replace('-',' ')
            pdf.cell(0,0,star_name)

            if count=='1-sans-star':
                label = '1 exoplanet only'
            elif count=='1':
                label = '1 planet'
            else:
                label = '%s planets'%count
            pdf.set_label_xy()
            pdf.set_xy(pdf.x+pdf.height-3, text_top+3.5+delta_y)
            pdf.cell(0,0,label)

            pdf.set_label_xy()
            pdf.set_xy(pdf.x+pdf.height-3, text_top+7+delta_y)
            pdf.cell(0,0,'exoplanets.seti.org')


    pdf.output('exoplanet_qr_codes.pdf','F')

if __name__ == "__main__":
    make_labels()
