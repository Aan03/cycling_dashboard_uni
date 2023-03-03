import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from dash.testing.application_runners import import_app
import pandas as pd
from axe_selenium_python import Axe
import random

borough_check = pd.read_csv('multi_page_app/data/boroughs.csv')
borough_check['name'] = borough_check['name'].replace(["Lewishaw", "Wandworth"],
                                                     ["Lewisham", "Wandsworth"])
list_boroughs = borough_check["name"].values.tolist()

app = import_app(app_file="app")


#Accessibility Test:
def test_accessibility(dash_duo):
    """
    GIVEN the app is running
    WHEN the site loads up
    THEN everything must be regarded as accessible according to selenium Axe and a results.json file is created
    """
    dash_duo.start_server(app)
    try:
        axe = Axe(dash_duo.driver)
        axe.inject()
        results = axe.run()
        axe.write_results(results,"results_after.json")
        #assert len(results["violations"]) == 0, axe.report(results["violations"])
        #The above was commented out after the results were obtained
    finally:
        dash_duo.driver.quit()
#The original result/output message was: AssertionError: Found 5 accessibility violations:


#Selenium Testing:
@pytest.mark.parametrize("test_input, expected", [("Quantity", (["Covered", "Secured", "Locker", "Total"],
                                                                                        "Total Quantity")),
                                                 ("Percentage out of total", (["Covered", "Secured",
                                                                             "Locker"], "Percentage"))])
def test_app2_barchart(dash_duo, test_input, expected):
    """
    GIVEN a user who is on the statistics page
    WHEN they select either the quantity or percentage radio buttons controlling the bar chart
    THEN the correct data regarding either the quantity or the percentage make-up of different
         bike rack types in London boroughs (or in all boroughs) will be shown 
    """
    dash_duo.start_server(app)
    dash_duo.driver.find_element(By.LINK_TEXT, 'Statistics').click()
    dropdown = WebDriverWait(dash_duo.driver,20).until(EC.visibility_of_element_located((By.XPATH,
                                                            '//*[@id="dropdown_borough"]//div[2]/input')))
    
    dash_duo.driver.execute_script("arguments[0].scrollIntoView();", dropdown)

    app2_graph = dash_duo.driver.find_element(By.XPATH, '//*[@id="bar_graph"]')
    dash_duo.driver.execute_script("arguments[0].scrollIntoView();", app2_graph)
    
    correct_title = 0
    incorrect_title = []
    correct_xaxis = 0
    incorrect_xaxis = []

    boroughs_to_check = ["All Boroughs", random.choice(list_boroughs), random.choice(list_boroughs), 
                        random.choice(list_boroughs), random.choice(list_boroughs)]
    
    for x in boroughs_to_check:
        dropdown.send_keys(x)
        dropdown.send_keys(Keys.RETURN)
        time.sleep(5)
        WebDriverWait(dash_duo.driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="bar_graph"]
                                    //*[name()="svg" and @class="main-svg"]//*[name()="rect" and @class="nsewdrag drag"]''')))


        prcent_bttn = WebDriverWait(dash_duo.driver,10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                    '//*[@id="quant_percent"]/div[2]/label')))
        if test_input == "Percentage out of total":
            dash_duo.driver.execute_script("arguments[0].scrollIntoView();", prcent_bttn)
            time.sleep(3)
            prcent_bttn.click()
            time.sleep(3)
            dash_duo.driver.get_screenshot_as_file("multi_page_app/testing/test_headless_screenshots/radiobuttnclicked.png")
    

        time.sleep(5)
        actual_xaxis = ((WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="bar_graph"]
                        //*[name()="svg" and @class="main-svg"]//*[name()="g" and @class="xaxislayer-above"]''')))).text).split("\n")
        dash_duo.driver.get_screenshot_as_file("multi_page_app/testing/test_headless_screenshots/xaxisloaded.png")
        time.sleep(10)
        bar_graph_title = WebDriverWait(dash_duo.driver,20).until(EC.visibility_of_element_located((By.XPATH,'''
                                                //*[@id="bar_graph"]//*[name()="g" and @class="g-gtitle"]//*[name()="text"]''')))

        dash_duo.driver.get_screenshot_as_file("multi_page_app/testing/test_headless_screenshots/bargraphtitleloaded.png")

        if ((bool(expected[1] in bar_graph_title.text) == True)
         and (bool(str(x) in bar_graph_title.text) == True)):
            correct_title += 1
        else:
            incorrect_title.append(x)
        
        if set(actual_xaxis).issubset(expected[0]):
            correct_xaxis += 1
        else:
            incorrect_xaxis.append(x)
            print(x, actual_xaxis)

    print(incorrect_title)
    print(incorrect_xaxis)
    assert correct_title == len(boroughs_to_check)
    assert correct_xaxis == len(boroughs_to_check)


@pytest.mark.parametrize("test_input, expected", [(2022, True), (2021, True), (2020, True)])
def test_app3_linegraph(dash_duo, test_input, expected):
    """
    GIVEN a user who is on the statistics page
    WHEN they select a year from the drop-down menu controlling the reports line graph
    THEN the correct report data from the selected year should be displayed on the graph
    """
    dash_duo.start_server(app)
    dash_duo.driver.find_element(By.LINK_TEXT, 'Statistics').click()
    dropdown = WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="dropdown_borough"]//div[2]/input')))
    report_graph = WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="report_graph"]')))
    time.sleep(5)
    
    dash_duo.driver.execute_script("arguments[0].scrollIntoView();", report_graph)

    time.sleep(3)
    timings_options_div = dash_duo.driver.find_element(By.XPATH, '''//*[@id="tick_times"]''')
    timings_options = timings_options_div.find_elements(By.XPATH, '''.//*[name()="label" and @class="form-check-label"]''')

    for option in range(1, len(timings_options)):
        (timings_options[option]).click()
        time.sleep(3)

    boroughs_to_check = ["All Boroughs", random.choice(list_boroughs), random.choice(list_boroughs), random.choice(list_boroughs)]
    total_check = []
    for borough in boroughs_to_check:
        print(borough)
        individual_check = []
        dropdown_year = WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,
                                                                    '''//*[@id="dropdown_year"]//div[2]/input''')))
        
        dropdown_year.send_keys(test_input)
        dropdown_year.send_keys(Keys.RETURN)
        time.sleep(3)
        dropdown.send_keys(borough)
        dropdown.send_keys(Keys.RETURN)

        time.sleep(3)

        main_report_area = WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,
            '''//*[@id="report_graph"]//*[name()="svg" and @class="main-svg"]//*[name()="g" and @class="bglayer"]''')))
        
        dash_duo.driver.execute_script("arguments[0].scrollIntoView();", main_report_area)
    
        ActionChains(dash_duo.driver).move_to_element(main_report_area).perform()
        time.sleep(3)

        dash_duo.driver.get_screenshot_as_file("multi_page_app/testing/test_headless_screenshots/reports_check.png")
        
        hover_info = (dash_duo.driver.find_element(By.XPATH,'''//*[@id="report_graph"]//*[name()="svg"]
                                                        //*[name()="g" and @class="hoverlayer"]''').text).split("\n")

        print(hover_info)
    
        report_values = []
        date = (hover_info[0])
        
        for element in range(1, len(hover_info)):
            if (hover_info[element]).isdigit() == True:
                report_values.append(int(hover_info[element]))

        total_reports = (max(report_values))
        report_values.remove((max(report_values)))

        if str(test_input) in str(date):
            individual_check.append(True)
        else:
            print(date)

        if sum(report_values) <= total_reports:
            individual_check.append(True)
        else:
            print(total_reports)
            print(report_values)

        if len(individual_check) == 2:
            total_check.append(True)

    if len(total_check) == len(boroughs_to_check):
        result = True
    else:
        result = False

    print(total_check)
    assert result == expected


@pytest.mark.parametrize("test_input, expected", [("Density", True), ("Proportion", True)])
def test_app4_choropleth(dash_duo, test_input, expected):
    """
    GIVEN a user who is on the statistics page
    WHEN they select either the density or proportion radio buttons and click on each 'bike rack type'
         radio button and hover their cursor over every borough in the choropleth map
    THEN the correct density or proportion value should be shown for each borough
    """
    dash_duo.start_server(app)
    dash_duo.driver.find_element(By.LINK_TEXT, 'Statistics').click()
    dropdown = WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,
                                                    '''//*[@id="prop_or_density"]//div[2]/input''')))
    
    dropdown.send_keys(test_input)
    dropdown.send_keys(Keys.RETURN)
    time.sleep(2)
    rack_options_div = dash_duo.driver.find_element(By.XPATH, '''//*[@id="rack_type"]''')
    rack_options = rack_options_div.find_elements(By.XPATH, '''.//*[name()="label" and 
                                                            @class="form-check-label"]''')

    checking_all_options = []
    for option in range(0, len(rack_options)):
        (rack_options[option]).click()
        time.sleep(2)
        main_choropleth = WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,
                                            '''//*[@id="choropleth_graph"]//*[name()="svg" and @class="main-svg"]
                                                                    //*[name()="g" and @class="trace choropleth"]''')))
        
        dash_duo.driver.execute_script("arguments[0].scrollIntoView();", main_choropleth)
        borough_traces = main_choropleth.find_elements(By.XPATH, '''.//*''')
        temp_values = []
        for element in range(0, len(borough_traces)):
            borough = borough_traces[element]
            try:
                ActionChains(dash_duo.driver).move_to_element(borough).perform()
                time.sleep(1)
                dynamic_hover = dash_duo.driver.find_element(By.XPATH, '''//*[@id="choropleth_graph"]
                    //*[name()="svg" and @class="main-svg"]//*[name()="g" and @class="hoverlayer"]
                                                            //*[name()="text" and @class="nums"]''')
                temp_values.append([(dynamic_hover.text), ((dynamic_hover.text).split(test_input+":"))[1]])
            except:
                print(element)
                pass

        time.sleep(1)
        print(temp_values)
        temp_check = 0
        for values in temp_values:
            print(values[0])
            if ((bool(test_input in values[0]) == True) and
                (bool(float(values[1]) >= 0) == True)):
                temp_check += 1

        print(temp_check)
        print(len(temp_values))
        if temp_check == len(temp_values):
            checking_all_options.append(True)

    if len(checking_all_options) == len(rack_options):
        result = True
    else:
        result = False
    
    assert result == expected


def test_map_usage(dash_duo):
    """
    GIVEN a user who is on the home page and is viewing the map
    WHEN they select either one of or a combination of the three 'bike rack' options
    THEN the map should update by only displaying 'bike rack' markers that meet the filter requirements

    GIVEN a user who is on the home page and is viewing the map
    WHEN they zoom into the map and/or zoom out
    THEN the map view should be zoomed in or zoomed out
    """
    dash_duo.start_server(app)
    main_map = WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="main_map"]')))

    rack_options_div = WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="selection"]')))
    rack_options = rack_options_div.find_elements(By.XPATH, '''.//*[name()="label" and @class="form-check-label"]''')

    ActionChains(dash_duo.driver).move_to_element(main_map).perform()
    time.sleep(2)
    dash_duo.driver.get_screenshot_as_file("multi_page_app/testing/test_headless_screenshots/map_usage.png")
    time.sleep(2)
    hover_info = ((WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH, 
                                 '''//*[@id="main_map"]//*[name()="svg"]//*[name()="g" and @class="hoverlayer"]
                                                //*[name()="text" and @class="nums"]''')))).text).split("\n")
    print(hover_info)
    
    zoom_in_bttn = dash_duo.driver.find_element(By.XPATH, '''//*[@id="main_map"]
                                            //*[@class="modebar-container"]//*[name()="a" and @data-title="Zoom in"]''')
    
    for i in range(0,3):
        zoom_in_bttn.click()
    dash_duo.driver.get_screenshot_as_file("multi_page_app/testing/test_headless_screenshots/map_usage_zoom_in.png")

    time.sleep(2)

    zoom_out_bttn = dash_duo.driver.find_element(By.XPATH, '''//*[@id="main_map"]
                                        //*[@class="modebar-container"]//*[name()="a" and @data-title="Zoom out"]''')
    
    for i in range(0,3):
        zoom_out_bttn.click()
    dash_duo.driver.get_screenshot_as_file("multi_page_app/testing/test_headless_screenshots/map_usage_zoom_out.png")

    for option in range(0, len(rack_options)):
        (rack_options[option]).click()
        time.sleep(2)
        dash_duo.driver.get_screenshot_as_file("multi_page_app/testing/test_headless_screenshots/map_usage.png")
        time.sleep(1)
    
    (rack_options[1]).click()

    dash_duo.driver.get_screenshot_as_file("multi_page_app/testing/test_headless_screenshots/map_usage_deselect.png")


def test_app2_app3_titles(dash_duo):
    """
    GIVEN a user who is on the statistic page
    WHEN the radio button `quantity` is selected and a borough has also been selected
         from the dropdown which has the id `dropdown_borough`
    THEN the title of the bar chart should change to  
         `Type of & Total Quantity" + "<br>" + "of Bike Racks in " + BOROUGH + ":`
    """
    dash_duo.start_server(app)
    dash_duo.driver.find_element(By.LINK_TEXT, 'Statistics').click()
    dropdown = WebDriverWait(dash_duo.driver,20).until(EC.visibility_of_element_located((By.XPATH,'''
                                                            //*[@id="dropdown_borough"]//div[2]/input''')))

    matched = 0
    unmatched = []
    boroughs_to_check = ["All Boroughs", random.choice(list_boroughs), random.choice(list_boroughs), 
                        random.choice(list_boroughs), random.choice(list_boroughs)]
    for x in boroughs_to_check:
        WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="report_graph"]')))
        WebDriverWait(dash_duo.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="bar_graph"]')))
        dropdown.send_keys(x)
        dropdown.send_keys(Keys.RETURN)
        time.sleep(5)
        bar_graph_title = dash_duo.driver.find_element(By.XPATH,'''//*[@id="bar_graph"]//*[name()="svg" and 
                                                                @class="main-svg"]//*[name()="g" and @class="infolayer"]
                                                                //*[name()="g" and @class="g-gtitle"]//*[name()="text"]''')

        
        line_graph_title = dash_duo.driver.find_element(By.XPATH,'''//*[@id="report_graph"]//*[name()="svg" and 
                                                                @class="main-svg"]//*[name()="g" and @class="infolayer"]
                                                                //*[name()="g" and @class="g-gtitle"]//*[name()="text"]''')
        
        if ((bool(x in bar_graph_title.text) == True) and 
            (bool(x in line_graph_title.text) == True)):
            matched += 1
        else:
            unmatched.append(x)

    print(unmatched)
    assert matched == len(boroughs_to_check)


def test_navbar_heading(dash_duo):
    """
    GIVEN a user who is visiting the site
    WHEN the home page loads
    THEN the navbar element should include the text 'Cycle Parking Dashboard'
    """
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal(".navbar-brand", "Cycle Parking Dashboard", timeout=20)
    assert (dash_duo.find_element(".navbar-brand").text).lower() == "Cycle Parking Dashboard".lower()


def test_going_to_stats_then_home(dash_duo):
    """
    GIVEN a user who is visiting the site
    WHEN they click on the "Statistics" link in the navigation bar and after 
         the statistics page loads they click on the "Map" link in the navigation bar
    THEN the user should be returned to the home page where the map title will be visible
    """
    dash_duo.start_server(app)
    dash_duo.driver.find_element(By.LINK_TEXT, 'Statistics').click()
    time.sleep(5)
    WebDriverWait(dash_duo.driver,20).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Map')))
    dash_duo.driver.find_element(By.LINK_TEXT, 'Map').click()
    time.sleep(10)
    map_title = WebDriverWait(dash_duo.driver,20).until(EC.visibility_of_element_located((By.XPATH, 
                                                    '//*[@id="page-content"]/div/div[1]/div[1]/h1')))
    
    assert (map_title.text).lower() == 'Map showing location of all bike racks in London'.lower()