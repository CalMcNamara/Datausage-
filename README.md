# Datausage-
Small application that shows the amount of the network usage sent/recv. Displays graphics and allows you to compare to previous times. 





Network.update_current_time 
  - Updates the current time. 
  - Changes current_time.
Network.change_type
  - Changes the tpye of data value. Switches between b, kb and mb.
  - Changes data_type.
Network.update_label
  - Updates the labels information with the most current information and logs it.
  - After it runs it calls itself after 5 seconds. 
Network.create_graph_ct
  -  creates a graph using the current time
     first it creats a string for the sql statement then it will extract the information from the db. 
     going to create a 2 line line graph. 
Network.get_all_time
    - gets all the times from the database then creates a listbox to select them from. Then can create graph using it.
    - Uses same functions a create_graph_ct for the comparison. 
 Network.create_button
    - Creates the starting buttons that are on the UI. 
 Network.test_connection
    -tests the connections for the database. 
 Network.get_all
  -Gets all the data from the database. 
 Network.inset_data
  - Inserts data into the database. 
  
  
    
