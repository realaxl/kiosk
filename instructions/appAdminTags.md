# manage tags admin page

- add the tags pages to the admin fronted. 
- use German for all frontednd texts

## top of page
- the top part of both columns should stay on top, not scroll
- on top, theres a selector for the tag names to present. the default is "all"
- a toggle to show all, also inactive, tags. default is not to show disabled tags

## main list below
- a list of all products matching the filter criteria to have a tag of that name
- on the left: if given, a thumbnail image of the product
- product name and below small the description, truncated to a single line
- on the right side, the tagging is managed:
    - existing tags are displayed as badges in the form name: value. 
    - the badge has an delete icon (cross) to delete the tag from the tags table
    - a plus sign to agg a tag in a modal
      - the modal shows the tag name and a field to enter the value of the tag
      - the name field has a drop down to select one of the existing names
      - also a new name can be entered
      - a save button to save the new tag and the new value
      - the note field is a textarea
      

