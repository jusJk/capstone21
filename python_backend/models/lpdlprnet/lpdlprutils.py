import cv2 as cv
import numpy as np

def segment_by_color(im_path, n): #
    from skimage.segmentation import slic
    from skimage.util import img_as_float

    org = cv.imread(im_path)
    # org = cv.cvtColor(org, cv.COLOR_BGR2RGB)

    segments = slic(img_as_float(org), n_segments=n, slic_zero=True)

    return segments, org


def chop_image(im_path, n):
    """
    Chop image into n segments
    """
    segments, org = segment_by_color(im_path, n)
    response = []
    for v in np.unique(segments):
        copy = org.copy()
        copy[segments == v] = 0
        response.append(copy)
    return response

def map_confidence_to_chunk(responses, filename):
    conf = {}
    for r in responses:
        key = r['file_name'].replace(filename,'')
        try:
            sc = r['all_bboxes'][0]['confidence_score']
        except:
            sc = 0.01
        conf[key] = sc

    return conf

def color_chunks(original_image_path, conf, save_as, n=2):
    import matplotlib.pyplot as plt

    segments, org = segment_by_color(original_image_path, n)
    im = org.copy()
    response =[]
    coef = get_coefficients(conf)

    norm_coef = (coef)/max(abs(coef))

    for v in np.unique(segments):
        try:
            im[segments == v] = color(norm_coef[v], coef[v])
        except:
            pass

    plt.imshow(org)
    plt.imshow(im, alpha=0.6)
    plt.savefig(save_as)


def draw_confidence_heat_map(responses, filename, save_as, n):
    enforce_png_name = filename.split('/')[-1].split('.')[0] + '.png'
    conf = map_confidence_to_chunk(responses,enforce_png_name)
    color_chunks(filename, conf, save_as, n)


def get_coefficients(conf):
    import pandas as pd
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.linear_model import LinearRegression
    enc = OneHotEncoder()
    df = pd.DataFrame([int(k) for k,v in conf.items() if k.isdigit() ])
    y = [v for k,v in conf.items() if k.isdigit()]
    full_image = [v for k,v in conf.items() if not k.isdigit()][0]
    y.append(full_image)
    X = 1-enc.fit_transform(df).toarray()
    X = np.append(X,[len(X)*[1]], axis=0)
    reg = LinearRegression().fit(X, y)

    return reg.coef_

def color(norm, coef):
    if coef > 0 :
        #red means coefficient is positive. adding it increases conf
        return norm*255, 0, 0
    elif coef <= 0:
        #blue means coefficient is negative, adding it reduces conf
        return 0, 0, norm*255
