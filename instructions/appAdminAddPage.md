amend the app so it reads a .env file when started. Do not crash if the file does not exist. The file should contain the following variables:
* PORT=5000
* DB_NAME=db.sqlite
* ADMIN_PASSWORD=secret
* EVENT="some event"

# reading .env file
* if the DB_NAME variable is provided, print a message saying "database name is set". If it is not provided, print a message saying "database name is not set". 
* use the PORT variable to start the server. If it is not provided, use the default port 5000. 
* if the EVENT variable is provided, check the db if an event of this name exists. If it does, print a message saying "event already exists". If it does not, create a new event in the database. Set the event date to the current date. set active to true.
* if the ADMIN_PASSWORD variable is provided, print a message saying "admin password is set". If it is not provided, print a message saying "admin password is not set". 
* after reading the .env file, check if the database file provided exists in the folder db. If not, exit with an error message. If it does, continue.
* if the ADMIN_PASSWORD variable is provided, add a new route to the app that can only be accessed if the user provides the correct password. The route should be /admin and should return a message saying "admin page". 

# admin interface
add a new file to the src folder for the admin interface of the web app. 
all functions in this can only be accessed if the user provided the password from .env
the admin page offers the following functions: 
* add a new event to the database
* delete an event from the database
* edit an event in the database
* view all events in the database
* set events active or inactive
* view all orders in the database
* add a new order to the database
* delete an order from the database
* edit an order in the database
* view all products in the database
* add a new product to the database
* view all stocks in the database
* add a new stocks to the database
* set stocks active or inactive

# stocks page
there will also be a page to administer the stock of the products for an event.
* left side
	* on top, theres a dropdown for the productCategories
	* all active products are listed with their images on the left in a list

* right side
	* on top, theres a dropdown for the events. the current event is selected by default.
	* theres a table with the stock of the product for the selected event
	* theres a button to add a new stock for the selected event and product
	* theres a button to delete the selected stock
	* theres a button to edit the selected stock
	* theres a button to set the selected stock active or inactive
	* theres a button to set the selected stock as a favorite
	* theres a input box to set the initial and current stock of the product for the selected event

# events page
there will also be a page to administer the events
* on top, theres a toggle to display only active events or all events. default is "active only"
* on top, theres a button to add a new event
* on top, theres a button to delete the selected event
* on top, theres a button to edit the selected event
* on top, theres a button to set the selected event active or inactive
* below is list view of the events

# product categories page
there will also be a page to administer the content of the productCategories table
* on top, theres a toggle to display only active productCategories or all productCategories. default is "active only"
* on top, theres a button to add a new productCategory
* on top, theres a button to deactivate the selected productCategory
* on top, theres a button to edit the selected productCategory
* below is list view of the productCategories

# product page
there will also be a page to administer the content of the products table
* on top, theres a toggle to display only active products or all products. default is "active only"
* on top, theres a button to add a new product
	* use the current date for the timestamp
	* set the purchasePrice to 0
* on top, theres a button to deactivate the selected product
* on top, theres a button to edit the selected product
* below is list view of the products
* if a product is clicked, a modal will open with the product details
	* the modal will have a button to edit the product
	* the modal will have a button to deactivate the product
	* the modal will have a read-only display of the productId
	* the modal will have a dropdown for the productCategory showing the name of the category
	* the modal will have a date selector for the timestamp
	* note and description are textareas with 3 lines of height