# blinkyparts Kiosk - test with IBM BOB
2026-05

## blinkyparts Infos

* 

## envs

* dev
    * Windows 11
    * IBM BOB
    * uv
    * Python 3
* prod
    * Raspberry Pi 400
    * KioskPi

## running app on Windows 11

```powershell
PS C:\dev\kiosk-with-bob> uv run .\src\app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.16.0.106:5000
```


## KioskPi - running app on RasPi



Raspberry Pi Auto-Update Setup
/tmp/kiosk-auto-update.log


## Support

### Tools
* git (local repo): http://172.16.0.16:5000/ibm/kiosk-with-bob
* git reset --hard origin/main: how-do-i-force-git-pull-to-overwrite-local-files
* [Mermaid online editor](https://www.mermaidflow.app/editor)


### SQL Statements
```sql
INSERT INTO events (name, timestamp, description, note, active)
VALUES ('Night of Science 2026', 1746835200, 'Night of Science 2026', 'Night of Science 2026', 1);
```

