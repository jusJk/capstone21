import json
import os


### Trying to use a lightweight and flexible method of information store and so
### the relevant information of the models is stored in config files
### we will read these config files in to populate information necessary
### for the internal API calls -- and possibly to define the external API calls
### programmatically (to be discussed)

model_files = os.listdir('./database/') #list of files in the directory
model_names = [m.split('.')[0] for m in model_files] #get list of model names, like lpdnet/lprnet

model_info = {}
for m in model_names:
    model_info[m] = json.load(open(f'./database/{m}/{m}.json'))