# Import modules
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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



######################################## Fruityadvice ########################################
# New section with fruit data from Fruityvice API response
## Creating get_fruityvice_data()-function
def get_fruityvice_data(this_fruit_choice):
  ## Loadning data
  fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice)
  ## Normalizing the json-version of the data
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  
  return fruityvice_normalized


## Header to display
streamlit.header('Fruityvice Fruit Advice!')

## Action section
try:
  ## Creating text entry box
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  
  if not fruit_choice:
    ## Catching error and displaying error message
    streamlit.error('Please select a fruit to get information')
  else:
    ## Calling the get-function
    back_from_fruityvice = get_fruityvice_data(fruit_choice)
    ## Displaying the normalized data as a table
    streamlit.dataframe(back_from_fruityvice)

except URLError as e:
  streamlit.error()



streamlit.stop()
# Selecting date from Snowflake
## Creating connection with Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

## Creating a cursor
my_cur = my_cnx.cursor()

## Querying data from database
my_cur.execute("SELECT * FROM fruit_load_list")

## Fetching one (the first) row of the result set
my_data_rows = my_cur.fetchall()

## Creating header to display
streamlit.header("The fruit load list constains:")

## Creating table to display
streamlit.dataframe(my_data_rows)

## Creating text entry box
fruit_to_add = streamlit.text_input('What fruit would you like to add?', 'Kiwi')
streamlit.write('Thank you for adding', fruit_to_add)

## Adding new fruit to the list
my_cur.execute("INSERT INTO fruit_load_list VALUES ('from streamlit');")
