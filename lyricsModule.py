import string, module, random, os
from PIL import Image

def create(missingwords_list):
    removes, adds = set(), set()
    specials = [str(i) for i in list(string.punctuation) if i!= '-' and i != "'"]
    for i in specials:
        for el in range(0,len(missingwords_list)):
            if i in missingwords_list[el]:
                if not missingwords_list[el].endswith("in'"):
                    missingwords_list[el] = missingwords_list[el].replace(i,'')
    for i in range(len(missingwords_list)):
        if missingwords_list[i].endswith("in'"):
            missingwords_list[i] = missingwords_list[i].replace("in'","ing")

    for i in missingwords_list:
        if '-' in i:
            removes.add(i)
            k = i.replace('-',' ')
            l = k.split()
            adds = adds.union(l)
    

    missingwords_list = [i for i in missingwords_list if i not in removes]
    missingwords_list = list(adds.union(missingwords_list))
    
    return missingwords_list
    
def compute_average_image_color(img):
    width, height = img.size

    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x,y))
            r_total += r
            g_total += g
            b_total += b
            count += 1

    return '#%02x%02x%02x' % (int(r_total/count), int(g_total/count), int(b_total/count))

def convert_images(List):
    """Convert jpeg images to png for lyricsGame.
Default directory: '../lyrics game/album images/'"""
    for i in List:
        directory = '../lyrics game/album images/'
        directory2 = "/home/serena/Nextcloud/python/lyrics game/album images/"
        try: img = Image.open(directory + i + ".jpeg")
        except: img = Image.open(directory2 + i + ".jpeg")
        img.save(directory + i + ".png")
        os.remove(directory + i + ".jpeg")
