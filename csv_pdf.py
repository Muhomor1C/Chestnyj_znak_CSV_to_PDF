import csv
from fpdf import FPDF
from pystrich.datamatrix import DataMatrixEncoder, DataMatrixRenderer

file = '1.csv'
margin = 12
horizontal_quantity = 4
vertical_quantity = 9
font_size = 6
text = ('Туфли мужские',
        'Артикул S-330-3',
        '_____________',
        'Размер',
        '36 - 41',
        )
# format A4 = 210*297mm
border_length = (210 - margin * 2) / horizontal_quantity
border_weight = (297 - margin * 2) / vertical_quantity
string_weight = font_size / 2


class DTMX(DataMatrixEncoder):
    """
    Метод возвращает объект PIL в виде изображения DataMatrix кода
    """
    def get_image(self, cellsize=2):
        dmtx = DataMatrixRenderer(self.matrix, self.regions).get_pilimage(cellsize)
        return dmtx


def add_frame(textmark, x, y):
    img = DTMX(textmark).get_image()
    dtmx_size = int(border_weight * 2.51 - font_size)  # 2.51 - Перевод в дюймы для PIL
    img = img.resize((dtmx_size, dtmx_size), resample=5)
    '''
    Ограничиваем человекочитаемую часть марки
    31 символом по формату "Честного знака"
    '''
    pdf.text(x + 2, y + border_weight - string_weight, textmark[0:31])

    for i in range(len(text)):
        pdf.text(x + border_weight - string_weight, y + string_weight * (i + 1), text[i])
    pdf.rect(x, y - 1, border_length - 1, border_weight - 1)
    pdf.image(img, x+1, y)


def main():
    with open(file) as f:
        reader = csv.reader(f, delimiter=" ")
        x = margin
        y = margin
        for row in reader:
            if x == margin + border_length * horizontal_quantity:
                x = margin
                y += border_weight
                if y == margin + border_weight * vertical_quantity:
                    y = margin
                    pdf.add_page()
            add_frame(row[0], x, y)
            x += border_length
    pdf.output('ready.pdf')


if __name__ == '__main__':
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSansCondensed.ttf')
    pdf.set_font('DejaVu', size=font_size)
    pdf.set_line_width(0.2)
    pdf.set_draw_color(r=0, g=0, b=0)
    pdf.add_page()
    main()
