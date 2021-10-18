import json
import os


### Trying to use a lightweight and flexible method of information store and so
### the relevant information of the models is stored in config files
### we will read these config files in to populate information necessary
### for the internal API calls

model_folders = os.listdir('./models/') #list of files in the directory
model_names = [m for m in model_folders if not ('py' in m or '.DS' in m) ] #get list of model names, like lpdnet/lprnet

model_info = {}
for m in model_names:
    model_info[m] = json.load(open(f'./models/{m}/database/{m}.json')) 