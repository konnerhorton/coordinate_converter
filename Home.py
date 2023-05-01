import streamlit as st
from pyproj import CRS
from pyproj import Transformer
import pandas as pd
import simplekml

col1, col2 = st.columns(2)

with col1:
    northing = st.number_input("Input northing")

with col2:
    easting = st.number_input("Input easting")


crs_geo = CRS.from_epsg(4326)
crs_proj = CRS.from_epsg(26917)
transformer = Transformer.from_crs(crs_proj, crs_geo)

latitude, longitude = transformer.transform(easting, northing)

st.write(f"Latitude:{latitude}")

data = st.file_uploader("Upload .csv")

df = pd.read_csv(data)

for i in df.index:
    northing = df.at[i, df.columns[1]]
    easting = df.at[i, df.columns[2]]
    df.at[i, "Latitude"], df.at[i, "Longitude"] = transformer.transform(
        easting, northing
    )


def write_bh_to_kml(df, output_name, id="bore", lat="lat", lon="lon"):
    kml = simplekml.Kml()

    for i in df.index:
        bh_id = df.at[i, id]
        bh_lon = df.at[i, lon]
        bh_lat = df.at[i, lat]
        bh = kml.newpoint()
        bh.name = bh_id
        bh.coords = [(bh_lon, bh_lat)]
    kml.save(output_name)


kml_output_name = "kml_output.kml"

output_kml = write_bh_to_kml(
    df, kml_output_name, id=df.columns[0], lat=df.columns[3], lon=df.columns[4]
)

with open("output.kml", "rb") as f:
    btn = st.download_button(label="Download .kml", data=f, file_name=kml_output_name)


# @st.cache_data
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv(index=False).encode("utf-8")


# st.download_button(
#     "Download .csv",
#     data=df,
#     file_name=f"Lat/Long from UTM.csv",
#     mime="text/csv",
# )
# st.download_button("Download .kml")
st.dataframe(data=df)
