Plane eine Erweiterung:

- manche Produkte stehen in Beziehung zueinander
  - manche Produkte benötigen eine Batterie, also ein weiteres Produkt
  
# Datenbank

- prüfe die Erweiterung in der Datenbank um eine Tabelle gemäß dem db.mmd ERM
  - beide FK, also fromProductId und toProductId, sind Verweise auf ein Product

- Plane eine Erweiterung der Admin Oberfläche, um die Relations zwischen Products zu pflegen
- Plane eine Erweiterung der Gallerie, um die Beziehung anzuzeigen
- Nutze für die Anzeige - je nach Richtung - die fromDescription bzw toDescription
  - Beispiel: A benötigt eine Batterie B
    - fromProductId zeigt auf A
    - toProductId zeigt auf B
    - fromDescription = "benötigt"
    - toDescription = "wird benötigt in"


Plane eine Erweiterung um folgendes Problem:

- manche Produkte benötigen eine Batterie
- generell sollten auch Kits, also eine Zusammenstellung aus mehreren Produkten, angeboten werden können
- Kits sollen genau wie einzelne Produkte behandelt werden

- wie kann die Datenstruktur erweitert werden?
- welche Anpassung in der Admin-Oberfläche benötigen wir?

- zusätzlich: Kits haben immer
  - eine Beschreibung
  - ein Bild / image analog zu den Produkten als Dateiname auf eine JPG oder PNG Datei
  - eine Notiz / note
  - gehören zu einer Kategorie
  - sind in der Gallery gekennzeichnet
  - in der Gallery werden die Verkaufspreise, nicht die Einkaufspreise addiert

Kits sollen möglichst wie Produkte behandelt werden
  - können zum Stock hinzugefügt werden