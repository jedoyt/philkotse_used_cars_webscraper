from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


### WEBDRIVER SETUP ###
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# Get "https://philkotse.com/used-cars-for-sale"
driver.get("https://philkotse.com/used-cars-for-sale")

# INPUT CAR BRAND
choose_brand_dropdown = driver.find_element(By.ID, "comboboxBrandSearchAutoListing_chosen")
choose_brand_dropdown.click()
print("Clicked dropdown")
time.sleep(1)
searchbrand_dropdown_elems = driver.find_elements(By.CLASS_NAME, 'chosen-drop')[0]
list_of_brands = searchbrand_dropdown_elems.text.split('\n')
print("List of brands:",list_of_brands)
chosen_brand = str(input("Choose car brand from list above: "))
#chosen_brand = 'Toyota'
chosenbrand_search_input_elems = driver.find_elements(By.CLASS_NAME, 'chosen-search-input')
chosenbrand_search_input_elems[0].send_keys(chosen_brand, Keys.ENTER)
#print("Search dropdown indices:",[list_of_brands.index(elem) for brand in list_of_brands])
time.sleep(1)

# INPUT CAR MODEL
choose_model_dropwdown = driver.find_element(By.ID, "comboboxModelSearchAutoListing_chosen")
choose_model_dropwdown.click()
print("Clicked dropdown")
time.sleep(1)
searchmodel_dropdown_elems = driver.find_elements(By.CLASS_NAME, 'chosen-drop')[1]
list_of_models = searchmodel_dropdown_elems.text.split('\n')
print("List of models:",list_of_models)
chosen_model = str(input("Choose brand's model from list above: "))
#chosen_model = 'Vios'
chosenmodel_search_input_elems = driver.find_elements(By.CLASS_NAME, 'chosen-search-input')
chosenmodel_search_input_elems[1].send_keys(chosen_model, Keys.ENTER)
time.sleep(1)

# SEARCH
search_btn = driver.find_elements(By.CLASS_NAME, 'btn-button')
search_btn[0].click()
print("Search button clicked!")
time.sleep(5)

# LOAD MORE RESULTS
def load_more_results(driver):
    time.sleep(3)
    loadmore_btn = driver.find_element(By.ID, "btnloadmore")
    loadmore_div = driver.find_element(By.CLASS_NAME, "item-more")
    try:
        loadmore_btn.click()
        print("Loaded more results! (Load More <a>")
        time.sleep(3)
    except:
        loadmore_div.click()
        print("Loaded more results! (Load More <div>")
        time.sleep(3)

#load_more_results(driver)
#load_more_results(driver)

# CREATE RESULT PLACEHOLDER
df_schema = {'Brand':[],'Model':[],'Featured?':[],'Description':[],'Used/New?':[],'YearModel':[],
        'Transmission':[],'Mileage_km':[],'Location':[],'Price_php':[],'URL':[]}

df = pd.DataFrame(df_schema)

# GET SEARCH RESULTS
search_result_container = driver.find_element(By.ID, 'contentList')
search_hits = search_result_container.find_elements(By.CLASS_NAME, 'col-4')
for hit in search_hits:
    #print(hit.text,'\n')
    row_list = hit.text.split('\n')
    print(row_list)

    row_dict = {'Brand':[],'Model':[],'Featured?':[],'Description':[],'Used/New?':[],'YearModel':[],
        'Transmission':[],'Mileage_km':[],'Location':[],'Price_php':[],'URL':[]}

    try:
        row_dict['Brand'].append(chosen_brand)
        row_dict['Model'].append(chosen_model)
        row_dict['Featured?'].append(row_list[0])
        row_dict['Description'].append(row_list[1])
        row_dict['Used/New?'].append(row_list[2])
        row_dict['YearModel'].append(row_list[3])
        if row_list[4] == 'Automatic' or row_list[4] == 'Manual':
            row_dict['Transmission'].append(row_list[4])
            row_dict['Mileage_km'].append(int("".join(row_list[5].split(" ")[0].split(",")))) # Km. unit excluded
            row_dict['Location'].append(row_list[6])
            row_dict['Price_php'].append(int("".join(row_list[7].split("₱")[1].split(",")))) # Currency excluded
            # Get URL
            try:
                hit_link_text = hit.find_elements(By.TAG_NAME, 'a')[0]
                row_dict['URL'].append(hit_link_text.get_attribute("href"))
            except:
                row_dict['URL'].append('')
        else:
            row_dict['Transmission'].append("")
            row_dict['Mileage_km'].append(int("".join(row_list[4].split(" ")[0].split(",")))) # Km. unit excluded
            row_dict['Location'].append(row_list[5])
            row_dict['Price_php'].append(int("".join(row_list[6].split("₱")[1].split(",")))) # Currency excluded
            # Get URL
            try:
                hit_link_text = hit.find_elements(By.TAG_NAME, 'a')[0]
                row_dict['URL'].append(hit_link_text.get_attribute["href"])
            except:
                row_dict['URL'].append('')

        
        df_row = pd.DataFrame(row_dict)
        print(df_row,'\n')
        df = pd.concat([df,df_row],axis=0)
        print(df.tail())
        filename = f"results_({chosen_brand}+{chosen_model}).csv"
        df.to_csv(filename, index=False)
    except IndexError:
        print("List index out of range. Proceed to next loop")
        pass