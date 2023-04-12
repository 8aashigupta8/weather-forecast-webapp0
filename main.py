import streamlit as st
import plotly.express as px
from backend import get_data
from datetime import date

# Add title, textbox, slider, selectbox and subheader
st.title("Weather Forecast for the Next Days")
place = st.text_input("Place:")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

if place:
    # Get the temperature/sky data
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            # Create a temperature plot
            temperatures = [dict["main"]["temp"]/10 for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature(C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            # Add sky conditions images
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            dates = [dict["dt_txt"] for dict in filtered_data]
            # dates list contain strings like - "2023-04-09 15:00:00"
            img_label = [date(day=int(dates[i][8:10]),
                              month=int(dates[i][5:7]),
                              year=int(dates[i][0:4])).
                         strftime(f'%a, %b %d {dates[i][11:-3]}')
                         for i in range(days * 8)]
            st.image(image_paths, width=115, caption=img_label)

    except KeyError:
        st.write("Sorry, that place does not exist")
