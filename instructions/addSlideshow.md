Add a Slideshow/Diashow feature to the Gallery main page:

- add a "Slideshow" button left to the admin button to the top bar
- check if you can re-use existing endpoints instead of new ones. The product Detail modal should be sufficient

# Slideshow details

- use the same page, do not add a sub-page but a query Parameter or similar
- a close button "Schließen" in the top Right which Returns to the normal presentation of products in the gallery
- present the products of the current Event 
  - in random order, if the .env Parameter SLIDESHOW_ORDER_RANDOM is true, Default false
  - Show them including
  - large Image (50% of screen height)
  - badges for the tags
  - sale Price = Verkaufspreis
  - the link to the manualUrl + QR code + a button to open the Manual in a new tab
  - product category
- read the delay from .env Parameter SLIDESHOW_DELAY with Default 7 seconds
- add an Animation to switch from one product to the next