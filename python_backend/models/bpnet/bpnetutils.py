def evaluate_bpnet(image_path, heatmap, paf, output_path, filename):
    import matplotlib.pyplot as plt
    import cv2 as cv
    org = cv.imread(image_path)
    org = cv.cvtColor(org, cv.COLOR_BGR2RGB)

    n_cols = [
        "nose",
        "neck",
        "right_shoulder",
        "right_elbow",
        "right_wrist",
        "left_shoulder",
        "left_elbow",
        "left_wrist",
        "right_hip",
        "right_knee",
        "right_ankle",
        "left_hip",
        'left_knee',
        'left_ankle',
        'right_eye',
        'left_eye',
        "right_ear",
        'left_ear']
    
    fig, ax = plt.subplots(3, 3, figsize=(20,10))

    for i in range(3):
        for j in range(3):
            if  i*3+j < 18:
                col_name = n_cols[i*3+j]
                ax[i,j].imshow(org)
                ax[i,j].set_title(col_name)
                ax[i,j].imshow(heatmap[:,:, i*3+j], alpha=0.5)

    plt.savefig(f"{output_path}/heatmap1_{filename}",bbox_inches='tight')

        
    fig, ax = plt.subplots(3, 3, figsize=(20,10))

    for i in range(3):
        for j in range(3):
            if  i*3+j < 18:
                col_name = n_cols[8 + i*3+j]
                ax[i,j].imshow(org)
                ax[i,j].set_title(col_name)
                ax[i,j].imshow(heatmap[:,:, 8 + i*3+j], alpha=0.5)

    plt.savefig(f"{output_path}/heatmap2_{filename}", bbox_inches='tight')

    for i in range(3):
        for j in range(3):
            if  i*3+j < 18:
                col_name = n_cols[8 + i*3+j]
                ax[i,j].imshow(org)
                ax[i,j].imshow(paf[:,:, 8 + i*3+j], alpha=0.5)

    plt.savefig(f"{output_path}/paf2_{filename}", bbox_inches='tight')

    for i in range(3):
        for j in range(3):
            if  i*3+j < 18:
                col_name = n_cols[ i*3+j]
                ax[i,j].imshow(org)
                ax[i,j].imshow(paf[:,:, i*3+j], alpha=0.5)

    plt.savefig(f"{output_path}/paf1_{filename}", bbox_inches='tight')

    return f"{output_path}/heatmap1_{filename}", f"{output_path}/heatmap2_{filename}", f"{output_path}/paf1_{filename}",f"{output_path}/paf2_{filename}"

    

