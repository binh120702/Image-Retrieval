import streamlit as st
import os 
from streamlit_cropper import st_cropper
import itertools
from st_clickable_images import clickable_images
import base64
from PIL import Image

st.set_page_config(layout="wide")

DATA_PATH = '../data/oxbuild_images-v1/'
IMAGES_PER_PAGE = 10

st.title('Image retrieval')

def init_image_path():
    imgs_p = []
    for file in os.listdir(DATA_PATH):
        if not file.endswith("jpg"):
            continue
        imgs_p.append(DATA_PATH + file)
    return imgs_p

def show_cropper(path):
    st.sidebar.markdown('# Cropper settings: ')
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
    aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
    aspect_dict = {
        "1:1": (1, 1),
        "16:9": (16, 9),
        "4:3": (4, 3),
        "2:3": (2, 3),
        "Free": None
    }
    aspect_ratio = aspect_dict[aspect_choice]
    img = Image.open(path)
    if not realtime_update:
        st.write("Double click to save crop")
    
    cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                aspect_ratio=aspect_ratio)
    # Manipulate cropped image at will
    st.write("Preview")
    _ = cropped_img.thumbnail((150,150))
    st.image(cropped_img)
    return cropped_img

def paginator(label, items):
    st.sidebar.markdown('# Paginator settings: ')

    items_per_page = int(st.sidebar.text_input('Image(s) per page: ', IMAGES_PER_PAGE))
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % (i+1)
    page_number = st.sidebar.selectbox(label, range(n_pages), format_func=page_format_func)

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * (items_per_page)
    max_index = min_index + (items_per_page)
    return itertools.islice(enumerate(items), min_index, max_index)

import random
import copy
def retrieve_image(query, data):
    new_data = copy.deepcopy(data)
    random.shuffle(new_data)
    return new_data

def demonstrate_image_pagination():


    imgs_p = init_image_path()
    image_iterator = paginator("Select an image page", imgs_p)
    indice_on_page, images_on_page = map(list, zip(*image_iterator))

    new_indice_on_page = []
    for i, id in enumerate(indice_on_page):
        new_indice_on_page.append('#' + str(id) + ': ' + images_on_page[i].split('/')[-1].split('.')[0])   

    images_encoded = []
    for file in images_on_page:
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images_encoded.append(f"data:image/jpeg;base64,{encoded}")

    tab1, tab2 = st.tabs(['Select query', 'Results'])
    results = []
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            clicked = clickable_images(paths = images_encoded,     
                #titles=[f"Image #{str(i)}" for i,j in enumerate(images_on_page)],
                titles=new_indice_on_page,
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "300px"},
            )
        with col2:
            st.markdown(f"## Image {new_indice_on_page[clicked]} clicked" if clicked > -1 else "No image clicked")
            cropped = show_cropper(images_on_page[clicked])
            

    with tab2:
        st.image(cropped, caption='query')
        num = int(st.text_input('Input number of retrieved images to show: ', 50))
        if st.button(label='Search'): 
            results = retrieve_image(imgs_p[clicked], imgs_p)
        st.image(results[:num], width=200, caption=[str(i) for i in range(min(num, len(results)))])

if __name__ == '__main__':
    demonstrate_image_pagination()
