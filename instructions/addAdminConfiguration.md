# Konfiguration

check the general instructions in .bob folder

add a DB table "config" as specified in the db schema

add an admin page "Konfiguration" that shows an editable list of the content of the `config` db table.
  - title "Konfiguration"
  - add button "Element hinzufügen"
  - list of properties
    - key
    - value
    - note as textarea with 3 lines
    - active as toggle
    - a delete "Löschen" button
  
amend the handling of the "current event" property
