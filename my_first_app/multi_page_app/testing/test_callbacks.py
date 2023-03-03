import sys, os
import pytest
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
import map_app, stats
from app import display_page
from map_app import update_df
from app2 import update_bar_chart
from app3 import update_report_chart
from app4 import display_choropleth


@pytest.mark.parametrize("test_input, expected", [("/", map_app.map_app_layout()),
                                                  ("/statistics", stats.stats_layout()),
                                                  ("/non-existing", '404 Page Not Found')])
def test_display(test_input, expected):
    '''
    GIVEN the cycling app site
    WHEN another page is requested
    THEN the correct page content should be shown if the url is valid and exists
         otherwise the "404" error message should be shown
    '''
    output_page = (display_page(test_input))
    assert str(output_page) == str(expected)


@pytest.mark.parametrize("test_input, expected", [(["COVER"], "Covered: TRUE, Secure: FALSE, Is a bike locker: FALSE"),
                                                  (["SECURE"], "Covered: FALSE, Secure: TRUE, Is a bike locker: FALSE"),
                                                  (["LOCKER"], "Covered: FALSE, Secure: FALSE, Is a bike locker: TRUE"),
                                                  (["COVER", "SECURE"], "Covered: TRUE, Secure: TRUE, Is a bike locker: FALSE"),
                                                  (["COVER", "LOCKER"], "Covered: TRUE, Secure: FALSE, Is a bike locker: TRUE"),
                                                  (["SECURE", "LOCKER"], "Covered: FALSE, Secure: TRUE, Is a bike locker: TRUE")])
def test_update_df(test_input, expected):
    '''
    GIVEN the main map on the home page of the app
    WHEN the different 'rack type' filter options are chosen
    THEN the correct bikes should be shown depending on the combination of selections
    '''
    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "selection.value"}]}))
        return update_df(test_input)

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert expected in str(output)


@pytest.mark.parametrize("test_input, expected", [(["All Boroughs", "Quantity"], ["All Boroughs", "{'text': 'Quantity of Bike Racks'}"]),
                                                  (["All Boroughs", "Percentage out of total"], ["All Boroughs", "{'text': 'Percentage (%)'}"]),
                                                  (["Kingston Upon Thames", "Quantity"], ["Kingston Upon Thames", "{'text': 'Quantity of Bike Racks'}"]),
                                                  (["Kingston Upon Thames", "Percentage out of total"], ["Kingston Upon Thames", "{'text': 'Percentage (%)'}"])])
def test_update_bar_chart(test_input, expected):
    '''
    GIVEN the bar chart on the statistics page
    WHEN a borough is selected using the boroughs drop-down menu and either the "Quantity" or "Percentage" 
         radio button is selected
    THEN the correct percentage of all bike racks or the total number of bike racks should
         be shown for the chosen borough only or all boroughs if that is the option selected
    '''
    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "dropdown_borough.value"}, {"prop_id": "quant_percent.value"}]}))
        return update_bar_chart(test_input[0], test_input[1])

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert (expected[0] in str(output)) and (expected[1] in str(output))


@pytest.mark.parametrize("test_input", [("All Boroughs", 2022, ["Morning"]),
                                        ("Lewisham", 2021, ["Morning", "Evening"]),
                                        ("City of London", 2020, ["Morning", "Evening", "All Day"])])
def test_update_report_chart(test_input):
    '''
    GIVEN the reports line chart on the statistics page
    WHEN a borough selection is made or all boroughs are chosen using the drop-down menu,
         and the year is selected using the year selection drop-down menu and the time of day,
         or the "All Day" option is selected
    THEN the reports generated only during the selected times in the specified borough/s
         should be shown
    '''
    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "dropdown_borough.value"}, {"prop_id": "dropdown_year.value"}, {"prop_id": "tick_times.value"}]}))
        return update_report_chart(test_input[0], test_input[1], test_input[2])
        
    ctx = copy_context()
    output = str(ctx.run(run_callback))
    print(output)
    total_check = 0
    if test_input[0] in output:
        total_check += 1
    if str(test_input[1]) in output:
        total_check += 1
    times_present = 0
    for x in test_input[2]:
        if x in output:
            times_present += 1
    if times_present == len(test_input[2]):
        total_check += 1
    assert total_check == 3


@pytest.mark.parametrize("test_input", [("Locker", "Density"), ("Secured", "Density"),
                                                  ("Cover", "Density"), ("All bike racks", "Density"),
                                                  ("Locker", "Proportion"), ("Secured", "Proportion"),
                                                  ("Cover", "Proportion")])
def test_display_choropleth(test_input):
    '''
    GIVEN the choropleth map on the statistics page
    WHEN the rack type and either the density or proportion options are selected
    THEN the callback should return a map of all boroughs and only reveal the 
         density or relative proportion of the user selected bike rack
    '''
    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "rack_type.value"}, {"prop_id": "prop_or_density.value"}]}))
        return display_choropleth(test_input[0], test_input[1])

    ctx = copy_context()
    output = str(ctx.run(run_callback))
    assert (test_input[0] and test_input[1]) in output