from Gui.setup.windowDetails import WindowDetails

# TODO refactor the code to get rid og this - function automatic size of window needed
main_window_setup = WindowDetails('Invoicer App - select an action', 500, 400, False)
customer_window_setup = WindowDetails('New Customer', 500, 700, False)
customer_selection_window_setup = WindowDetails('Select Customer', 1500, 600, True)
project_window_setup = WindowDetails('New Project', 700, 350, False)
item_selection_window_setup = WindowDetails('Select kind of item', 400, 150, False)
item_window_setup = WindowDetails('Add General Item', 800, 800, False)
settings_window_setup = WindowDetails('Settings', 500, 900, False)
