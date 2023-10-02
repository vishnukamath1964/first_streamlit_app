import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("Sample Streamlit App")
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list=pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
## adding multiselect information
my_fruit_list=my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")
def get_fruit_vice_data(this_fruit_info):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    #streamlit.dataframe(fruityvice_normalized)
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please provide fruit information")
  else:
    if streamlit.button("Get fruit list"):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        streamlit.text("The fruit load list contains:")
        my_data_rows=insert_fruit_list_data(fruit_choice)
        streamlit.text(my_data_rows)
except URLError as e:
    streamlit.error()
    
def insert_fruit_list_data(fruit_choice):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('from streamlit')")
        return my_cur.fetchall()




