import xml.etree.ElementTree as ET

# Fonction création d'une balise coordonnée d'un point)
def createPosTag(parent, x, y, index):
    tag = ET.SubElement(parent, 'pos'+index)
    x_tag = ET.SubElement(tag, 'x')
    y_tag = ET.SubElement(tag, 'y')

    x_tag.text = str(x)
    y_tag.text = str(y)

    return tag

# Création de la structure + écriture du fichier dicom
def createDicomFile(grand_axe, petit_axe, T4):

    OutilsXML = ET.Element('OutilsXML')
    itemOutil = ET.SubElement(OutilsXML, 'itemOutil')
    type = ET.SubElement(itemOutil, 'type')
    type.text = "VHS_2"

    pos1 = createPosTag(itemOutil, grand_axe[0][0], grand_axe[0][1], '1')
    pos2 = createPosTag(itemOutil, grand_axe[1][0], grand_axe[1][1], '2')
    pos3 = createPosTag(itemOutil, petit_axe[0][0], petit_axe[0][1], '3')
    pos4 = createPosTag(itemOutil, petit_axe[1][0], petit_axe[1][1], '4')
    pos5 = createPosTag(itemOutil, T4[0][0], T4[0][1], '5')
    pos6 = createPosTag(itemOutil, T4[1][0], T4[1][1], '6')
    pos7 = createPosTag(itemOutil, 0, 0, '7')
    pos8 = createPosTag(itemOutil, 0, 0, '8')

    title = ET.SubElement(itemOutil, 'title')
    text = ET.SubElement(itemOutil, 'text')

    # encoding = unicode nécessaire pour que cela ne soit pas considéré
    # comme des bytes mais bien des string
    data = ET.tostring(OutilsXML, encoding="unicode")
    file = open("VHS.dcm", "w")
    file.write(data)

if __name__ == "__main__":
    g_axe = [(1062.62, 1172.67), (1597.38, 2139)]
    p_axe = [(1421.99, 1325.7), (668.869, 1736.65)]
    t4 = [(539.909, 913.032), (710.136, 833.937)]

    createDicomFile(g_axe, p_axe, t4)
