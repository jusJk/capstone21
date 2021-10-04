# File for functions to do post processing on
from PIL import ImageDraw, Image
import os

def render_image(frame, box, output_image_file, outline_color='yellow', linewidth= 10):
    """Render images with overlain outputs."""
    image = Image.open(frame)
    draw = ImageDraw.Draw(image)
    if (box[2] - box[0]) >= 0 and (box[3] - box[1]) >= 0:
        draw.rectangle(box, outline=outline_color)
        for i in range(linewidth):
            x1 = max(0, box[0] - i)
            y1 = max(0, box[1] - i)
            x2 = min(image.size[0], box[2] + i)
            y2 = min(image.size[1], box[3] + i)
            draw.rectangle(box, outline=outline_color)
    image.save(output_image_file)


def crop_image(frame, box, output_cropped_file):
    """Create crop image """
    image = Image.open(frame)
    if (box[2] - box[0]) >= 0 and (box[3] - box[1]) >= 0:
        image = image.crop((box[0],box[1],box[2],box[3]))
    image.save(output_cropped_file,"JPEG")


def create_directories(model, id, curr_time):
    # Create directories for input and output images
    if not os.path.isdir(f"triton_client/{model}"):
        os.mkdir(f"triton_client/{model}")
        os.mkdir(f"triton_client/{model}/input")
        os.mkdir(f"triton_client/{model}/output")
    
    if not os.path.isdir(f"triton_client/{model}/input/{id}"):
        os.mkdir(f"triton_client/{model}/input/{id}")
        os.mkdir(f"triton_client/{model}/output/{id}")

    if not os.path.isdir(f"triton_client/{model}/input/{id}/{curr_time}"):
        os.mkdir(f"triton_client/{model}/input/{id}/{curr_time}")
        os.mkdir(f"triton_client/{model}/output/{id}/{curr_time}")

    # if os.path.isdir(f"triton_client/{model}"):
    #     os.mkdir(f"triton_client/{model}/input")
    #     os.mkdir(f"triton_client/{model}/input/{id}")
    #     os.mkdir(f"triton_client/{model}/output")
    #     os.mkdir(f"triton_client/{model}/output/{id}")
    #     os.mkdir(f"triton_client/{model}/input/{id}/{curr_time}")
    #     os.mkdir(f"triton_client/{model}/output/{id}/{curr_time}")
    # else