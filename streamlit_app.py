# Import modules
import streamlit
import pandas
import requests

# Streamlit title
streamlit.title('Mel\'s Parents\' Healthy Diner')

# Creating breakfast menu
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

# Creating smoothie building section
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Loadning data
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Creating a pick list 
fuits_selected = streamlit.multiselect('Pick same fruits: ', 
                                       list(my_fruit_list.index), 
                                       ['Avocado', 'Strawberries'])

# Selecting the user selected fruits from the dataframe
fruits_to_show = my_fruit_list.loc[fuits_selected]

# Display dataframe in the app
streamlit.dataframe(fruits_to_show)


# New section with fruit data from Fruityvice API response
## Header
streamlit.header('Fruityvice Fruit Advice!')
## Loadning data
fruityvice_response = requests.get('https://fruityvice.com/api/fruit/watermelon')
## Displaying it 
streamlit.text(fruityvice_response.json())
