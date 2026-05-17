add the stocks pages to the admin fronted. 
use German for all frontedn texts

page has a left and a right column
the top part of both columns should stay on top, not scroll

# left = products side
## top for products

- on top is a filter for the product categories to present. it starts with all categories selected
- a toggle to show all, also inactive, default is not to show disabled products

## main part for products
- a list of all products matching the filter criteria
- on the left: if given, a thumbnail image of the product
- product name and below small the description, truncated to a single line
- button to add the product to the selected stock

# right = stocks
## top for stocks

- on top is a filter for the product categories to present. it starts with all categories selected
- a toggle to show all, also inactive, default is not to show disabled products

## main part for stocks
- a list of all products in the selected stock including the properties salePrice, active, initialNumberInStock, currentNumberInStock
- on the right, 
    - a red button to remove the product from the stock, which means to delete this row in the database
	- a yellow button to edit the product in the stock, which means to update the row in the database including properties salePrice, active, initialNumberInStock, currentNumberInStock

