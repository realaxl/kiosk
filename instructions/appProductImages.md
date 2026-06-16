# product cards web page
write a pythjon web server with flask api
create a web page based on bootstrap 5
read the products table from the db
show all the products on the page in bootstrap cards
each card has a header with the product name
each card has a body with the image of the product
take the images from the images folder in the root of the project
show the price of the prduct in the card footer

# Thumbnail generation and cache:
amend the code for the image display: check, if an image with the same name exists in the cache folder
if it does, display the cached image
if it doesn't, generate the thumbnail and save it in the cache folder with a resolution of 1024x1024 pixels max. Keep image proportions
display the thumbnail
