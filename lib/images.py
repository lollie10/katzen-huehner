
import glob
import os.path

'''
Collect images from a folder
'''

def filter(data):
    data['source_images'] = []
    n = 1
    for i in glob.glob(data['images']):
        filename = os.path.basename(i)
        base, ext = os.path.splitext(filename)
        data['source_images'].append({
            'img': base,
            'n': f'{n:02}',
        })
        n += 1
        if n > 24:
            break
    
    return data
