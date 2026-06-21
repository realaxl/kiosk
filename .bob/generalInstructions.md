# general instructions

- for all HTML pages, use Bootstrap 5

- for all visible elements in the HTML pages, use German language
    - keep these words in English: "Event", "Management", "Tags"
- Keep the same fonts, font sizes, add padding, margins, etc. as in the original page
- Keep the same colors as in the original page
- Keep the same layout as in the original page

- Keep these color styles for the buttons. Use the Bootstrap CSS classes for the buttons.
    - Save, OK, Confirmations = "primary" - blue
    - Cancel = "secondary" - gray
    - "success" - green
    - Deletions = "danger" - red
    - Enable/disable = "warning" - yellow
    - Links to external sites, manuals etc. = "info" - light blue

- for timestamp display, use the one of the two formats below
    - "01.01.2023" for events, products etc. - German format
    - "01.01.2023 12:34:56" - German format - for sales
- for prices, assume Euro / € currency

# UI elements on HTML pages

- for all delete "Löschen" Buttons:
  - do not delete immediately
  - do not display alert box
  - amend the button in the page to "Sicher löschen?"
  - only if this button is pressed, perform the deletion activity
  
- for textareas, if not otherwise specified, use 3 text rows
