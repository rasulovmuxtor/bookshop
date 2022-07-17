from xlwt import Workbook, easyxf


class BaseWorkbook(Workbook):
    h_bold_center = easyxf(
        "align: vert centre, horiz centre;font: bold 1,height 280;")
    bold_center = easyxf("align: vert centre, horiz centre;font: bold 1;")
    bold_left = easyxf("align: vert centre, horiz left;font: bold 1;")
    bold = easyxf("font: bold 1;")
    middle_width = 256 * 20
    short_width = 256 * 5
    long_width = 256 * 43
    tall_height = 600
