def evaluate_bpnet(image_path, heatmap, paf, save_as):
    import matplotlib.pyplot as plt
    import cv2 as cv
    org = cv.imread(image_path)
    org = cv.cvtColor(org, cv.COLOR_BGR2RGB)
    plt.imshow(org)
    plt.imshow(heatmap[:,:, 1], alpha=0.5)
    plt.savefig(save_as)


    
