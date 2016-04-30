from PIL import Image
from math import log

intStr = [str(i) for i in range(10)]
lShift = ['~','!','@','#','$','%','^','Q','W','E','R','T','A','S','D','F','G','Z','X','C','V']
rShift = ['&','*','(',')','_','+','{','}','|',':','"','<','>','?','Y','U','I','O','P','H','J','K','L','B','N','M']

def getKey(ch):
    global intStr
    if ch in intStr:
        return 'Numpad' + ch
    elif ch == ' ':
        return 'Space'
    elif ch == '\n':
        return 'Return'
    elif ch == '<' or ch == ',':
        return 'Oem_Comma'
    elif ch == '>' or ch == '.':
        return 'Oem_Period'
    elif ch == '!':
        return '1'
    elif ch == '@':
        return '2'
    elif ch == '#':
        return '3'
    elif ch == '$':
        return '4'
    elif ch == '%':
        return '5'
    elif ch == '^':
        return '6'
    elif ch == '&':
        return '7'
    elif ch == '*':
        return '8'
    elif ch == '(':
        return '9'
    elif ch == ')':
        return '0'
    elif ch == '-' or ch == '_':
        return 'Oem_Minus'
    elif ch == '+' or ch == '=':
        return 'Oem_Plus'
    elif ch == '/' or ch == '?':
        return 'Oem_2'
    elif ch == '*':
        return 'Multiply'
    elif ch == '`' or ch == '~':
        return 'Oem_3'
    elif ch == '[' or ch == '{':
        return 'Oem_4'
    elif ch == ']' or ch == '}':
        return 'Oem_6'
    elif ch == '|' or ch == '\\':
        return 'Oem_5'
    elif ch == ';' or ch == ':':
        return 'Oem_1'
    elif ch == '\'' or ch == '"':
        return 'Oem_7'
    return ch

# http://jayd.sauce.do/07/04/python-keyboard-heatmapper
def createKeyBoardHeatMap(sentence):
    key_location = {"Escape": (13, 10, 0), "F1": (78, 10, 0), "F2": (116, 10, 0), "F3": (154, 10, 0), "F4": (193, 10, 0), "F5": (253, 10, 0), "F6": (291, 10, 0), "F7": (329, 10, 0), "F8": (367, 10, 0), "F9": (428, 10, 0), "F10": (466, 10, 0), "F11": (504, 10, 0), "F12": (542, 10, 0), "Snapshot": (601, 10, 0), "Scroll`": (639, 10, 0), "Pause": (677, 10, 0), "Oem_3": (13, 82, 0), "1": (52, 83, 0), "2": (89, 82, 0), "3": (127, 82, 0), "4": (165, 82, 0), "5": (203, 82, 0), "6": (242, 82, 0), "7": (280, 82, 0), "8": (318, 82, 0), "9": (356, 82, 0), "0": (394, 82, 0), "Oem_Minus": (432, 82, 0), "Oem_Plus": (470, 82, 0), "Back": (508, 82, 1), "Insert": (603, 82, 0), "Home": (641, 82, 0), "Prior": (679, 82, 0), "NumLock": (738, 82, 0), "Divide-": (776, 82, 0), "Multiply*": (814, 82, 0), "Subtract": (852, 82, 0), "Tab": (13, 122, 2), "Q": (69, 122, 0), "W": (107, 122, 0), "E": (146, 122, 0), "R": (184, 122, 0), "T": (222, 122, 0), "Y": (260, 122, 0), "U": (297, 122, 0), "I": (336, 122, 0), "O": (374, 122, 0), "P": (412, 122, 0), "Oem_4": (449, 122, 0), "Oem_6": (487, 122, 0), "Oem_5": (526, 122, 3), "Delete": (602, 122, 0), "End": (640, 122, 0), "Next": (678, 122, 0), "Numpad7": (737, 122, 0), "Numpad8": (775, 122, 0), "Numpad9": (813, 122, 0), "Add": (852, 122, 4), "Capital": (13, 161, 5), "A": (79, 161, 0), "S": (117, 161, 0), "D": (156, 161, 0), "F": (194, 161, 0), "G": (232, 161, 0), "H": (270, 161, 0), "J": (308, 161, 0), "K": (346, 161, 0), "L": (384, 161, 0), "Oem_1": (422, 161, 0), "Oem_7": (461, 161, 0), "Return": (499, 161, 6), "Numpad4": (737, 161, 0), "Numpad5": (776, 161, 0), "Numpad6": (814, 161, 0), "Lshift": (13, 200, 7), "Z": (106, 200, 0), "X": (145, 200, 0), "C": (183, 200, 0), "V": (222, 200, 0), "B": (260, 200, 0), "N": (298, 200, 0), "M": (336, 200, 0), "Oem_Comma": (374, 200, 0), "Oem_Period": (413, 200, 0), "Oem_2": (451, 200, 0), "Rshift": (489, 200, 8), "Up": (641, 200, 0), "Numpad1": (738, 201, 0), "Numpad2": (775, 201, 0), "Numpad3": (814, 201, 0), "NumpadReturn": (851, 201, 9), "Lcontrol": (13, 240, 10), "Lwin": (69, 240, 11), "Lmenu": (119, 240, 11), "Space": (169, 240, 12), "Rmenu": (377, 240, 11), "Rwin": (427, 240, 11), "Apps": (476, 240, 11), "Rcontrol": (525, 240, 10), "Left": (603, 240, 0), "Down": (641, 240, 0), "Right": (679, 240, 0), "Numpad0": (738, 240, 13), "Decimal": (814, 240, 0)}
    t = {}
    for j in sentence:
        i = j.upper() if j.upper() in key_location and j not in intStr else getKey(j)
        if i in t:
            t[i] = t[i] + 1.0
        else:
            t[i] = 1.0
        if j in lShift:
            if 'Lshift' in t:
                t['Lshift'] = t['Lshift'] + 1
            else:
                t['Lshift'] = 1
        if j in rShift:
            if 'Rshift' in t:
                t['Rshift'] = t['Rshift'] + 1
            else:
                t['Rshift'] = 1

    for k in t.keys():
        t[k] = log(t[k])

    biggest = max(v for k, v in t.items())

    heatmap = Image.open("heat_gradient.png")

    im = Image.open("keyboard.png")
    for k, v in t.items():
        if(k not in key_location):
            print(k)
            continue
        heatbox = ((int((v / biggest) * 1000) - 1), 0, int((v / biggest) * 1000), 1)
        heatRegion = heatmap.crop(heatbox)
        heatColorInfo = heatRegion.getcolors()[0][1]

        if(key_location[k][2] == 0):
            img_w = 31
            img_h = 35
        elif(key_location[k][2] == 1):
            img_w = 65
            img_h = 35
        elif(key_location[k][2] == 2):
            img_w = 48
            img_h = 35
        elif(key_location[k][2] == 3):
            img_w = 47
            img_h = 35
        elif(key_location[k][2] == 4):
            img_w = 35
            img_h = 76
        elif(key_location[k][2] == 5):
            img_w = 59
            img_h = 35
        elif(key_location[k][2] == 6):
            img_w = 74
            img_h = 35
        elif(key_location[k][2] == 7):
            img_w = 85
            img_h = 35
        elif(key_location[k][2] == 8):
            img_w = 85
            img_h = 35
        elif(key_location[k][2] == 9):
            img_w = 35
            img_h = 76
        elif(key_location[k][2] == 10):
            img_w = 49
            img_h = 35
        elif(key_location[k][2] == 11):
            img_w = 40
            img_h = 35
        elif(key_location[k][2] == 12):
            img_w = 200
            img_h = 35
        elif(key_location[k][2] == 13):
            img_w = 68
            img_h = 35
        else:
            img_w = 31
            img_h = 35


        newImg = Image.new('RGB', (img_w, img_h), heatColorInfo)
        box = (key_location[k][0], key_location[k][1], key_location[k][0] + img_w, key_location[k][1] + img_h)
        region = im.crop(box)
        region = Image.blend(region, newImg, .5)
        im.paste(region, box)
    #im.save('keyboard_heatmap.jpg')
    #im.show()
    kb_legend = Image.open("keyboard_legend.png")
    result = Image.new('RGB', (max(im.width,kb_legend.width), im.height+kb_legend.height))
    result.paste(im=im,box=(0,0))
    result.paste(im=kb_legend,box=(0,im.height))
    return result

#def main():
#    sent = "This is supposed to be a good example"
#    createKeyBoardHeatMap(sent).save("xx.png")
#    pass

#if __name__ == "__main__":
#    main()