import streamlit as st
from PIL import Image
import requests
from streamlit_juxtapose import juxtapose
import pathlib
from random import randrange
import uuid


st.markdown("""
    # IDC Detection
    #### Created by Jack Claar, Elizabeth Feldeverd, and Nadia Yap
    ### Upload a breast cancer histology image
""")

STREAMLIT_STATIC_PATH = (
    pathlib.Path(st.__path__[0]) / "static"
)  # at venv/lib/python3.9/site-packages/streamlit/static

print(STREAMLIT_STATIC_PATH)

png = st.file_uploader("Upload a PNG image", type=([".png"]))


if png:
    # input = randrange(100, 1000, 2)
    # output = input + 1

    # IMG1 = f"img{input}.png"

    myuuid = uuid.uuid4()
    IMG1 = f"{myuuid}.png"

    # url = "http://127.0.0.1:8000/annotate"  # local
    url = "https://idc-mvds5dflqq-ew.a.run.app/annotate"  # production
    files = {"file": (png.name, png, "multipart/form-data")}
    response = requests.post(url, files=files).json()

    # How to download image from url
    IMG2 = response["url"]

    # put a spinny wheel while waiting for the response

    original = Image.open(png)
    original.save(STREAMLIT_STATIC_PATH / IMG1)  # this overwites

    juxtapose(IMG1, IMG2)

    legend = Image.open('legend.PNG')
    st.image(legend, use_column_width=True)

    report = response["report"]

    st.write(
        f"""
        The mean probability of IDC across the image is {report['mean_whole_slide']}%.\n
        The percentage of high severity IDC regions across the image is {report['high_IDC_regions']}%.\n
        The percentage of medium severity IDC regions across the image is {report['medium_IDC_regions']}%.\n
        The percentage of low severity IDC regions across the image is {report['low_IDC_regions']}%.\n
        The percentage of IDC-free regions across the image is {report['no_IDC_regions']}%.\n
        """
    )

    recommendation = response["recommendation"]

    st.write(recommendation)