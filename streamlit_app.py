# Import modules
import streamlit
import pandas
import requests
import snowflake.connector

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

## Creating text entry box
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered:', fruit_choice)

## Loadning data
fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice)

## Displaying it 
# streamlit.text(fruityvice_response.json()) # just writes the data to the screen

## Normalizing the json-version of the data
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

## Displaying the normalized data as a table
streamlit.dataframe(fruityvice_normalized)



# Selecting some Snowflake meta data
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
