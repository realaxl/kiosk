# *blinkyparts Kiosk* - test with IBM BOB (kiosk-with-bob)

2026-05
[Kanban](https://cryptpad.fr/kanban/#/3/kanban/edit/c6d25d7dc8eb86981e3830eec2e09b86/)

# Specs
- create a Kiosk app for a small sales kiosk
- runs stand alone on Windows 11 and a Raspberry Pi
- local SQL database (SQLite)
- Python REST API backend
- HTML + JavaScript frontend
- Bootstrap 5


## envs

* dev
    * Windows 11
    * IBM BOB
    * uv
    * Python 3
* stage
    * Raspberry Pi 400
    * KioskPi
* prod
    * kiosk (Pi4) for [blinkyparts](https://binary-kitchen.github.io/SolderingTutorial/) @ 2026-06-12 / [Night of Science 2026](https://nightofscience.de/)

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
* [Mermaid online editor](https://www.mermaidflow.app/editor)
* git (local repo): http://172.16.0.16:5000/ibm/kiosk-with-bob
* git (remote repo): [git@github.com:realaxl/kiosk.git](https://github.com/realaxl/kiosk)


### SQL Statements
```sql
INSERT INTO events (name, timestamp, description, note, active)
VALUES ('Night of Science 2026', 1746835200, 'Night of Science 2026', 'Night of Science 2026', 1);
```



## blinkyparts Infos

* https://binary-kitchen.github.io/SolderingTutorial/

* **50ohmDummyLoad** — [EN](https://binary-kitchen.github.io/SolderingTutorial/50ohmDummyLoad/manual/50ohmDummyLoad_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/50ohmDummyLoad/manual/50ohmDummyLoad_de.pdf)
* **AlHackaAlpaka** — [EN](https://binary-kitchen.github.io/SolderingTutorial/AlHackaAlpaka/manual/AlHackaAlpaka_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/AlHackaAlpaka/manual/AlHackaAlpaka_de.pdf)
* **ArrowSMD** — [EN](https://binary-kitchen.github.io/SolderingTutorial/ArrowSMD/manual/ArrowSMD_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/ArrowSMD/manual/ArrowSMD_de.pdf)
* **ATXBreakoutBoardSMD** — [EN](https://binary-kitchen.github.io/SolderingTutorial/ATXBreakoutBoardSMD/manual/ATXBreakoutBoardSMD_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/ATXBreakoutBoardSMD/manual/ATXBreakoutBoardSMD_de.pdf)
* **AxolotlBadge** — [EN](https://binary-kitchen.github.io/SolderingTutorial/AxolotlBadge/manual/AxolotlBadge_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/AxolotlBadge/manual/AxolotlBadge_de.pdf)
* **BleepBot** — [EN](https://binary-kitchen.github.io/SolderingTutorial/BleepBot/manual/BleepBot_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/BleepBot/manual/BleepBot_de.pdf)
* **BlinkenrocketMini** — [EN](https://binary-kitchen.github.io/SolderingTutorial/BlinkenrocketMini/manual/BlinkenrocketMini_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/BlinkenrocketMini/manual/BlinkenrocketMini_de.pdf)
* **BlinkyTree** — [EN](https://binary-kitchen.github.io/SolderingTutorial/BlinkyTree/manual/BlinkyTree_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/BlinkyTree/manual/BlinkyTree_de.pdf)
* **Cat01** — [EN](https://binary-kitchen.github.io/SolderingTutorial/Cat01/manual/Cat01_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/Cat01/manual/Cat01_de.pdf)
* **CatInABox** — [EN](https://binary-kitchen.github.io/SolderingTutorial/CatInABox/manual/CatInABox_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/CatInABox/manual/CatInABox_de.pdf)
* **CubeDIP** — [EN](https://binary-kitchen.github.io/SolderingTutorial/CubeDIP/manual/CubeDIP_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/CubeDIP/manual/CubeDIP_de.pdf)
* **Daisy_RGB** — [EN](https://binary-kitchen.github.io/SolderingTutorial/Daisy_RGB/manual/Daisy_RGB_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/Daisy_RGB/manual/Daisy_RGB_de.pdf)
* **DiceDIP** — [EN](https://binary-kitchen.github.io/SolderingTutorial/DiceDIP/manual/DiceDIP_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/DiceDIP/manual/DiceDIP_de.pdf)
* **DiceMcDIP** — [EN](https://binary-kitchen.github.io/SolderingTutorial/DiceMcDIP/manual/DiceMcDIP_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/DiceMcDIP/manual/DiceMcDIP_de.pdf)
* **Dino** — [EN](https://binary-kitchen.github.io/SolderingTutorial/Dino/manual/Dino_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/Dino/manual/Dino_de.pdf)
* **DraussenfuchsAntenne** — [EN](https://binary-kitchen.github.io/SolderingTutorial/DraussenfuchsAntenne/manual/DraussenfuchsAntenne_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/DraussenfuchsAntenne/manual/DraussenfuchsAntenne_de.pdf)
* **DraussenfuchsSender** — [EN](https://binary-kitchen.github.io/SolderingTutorial/DraussenfuchsSender/manual/DraussenfuchsSender_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/DraussenfuchsSender/manual/DraussenfuchsSender_de.pdf)
* **Elefant** — [EN](https://binary-kitchen.github.io/SolderingTutorial/Elefant/manual/Elefant_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/Elefant/manual/Elefant_de.pdf)
* **ErmerBeeperDIP** — [EN](https://binary-kitchen.github.io/SolderingTutorial/ErmerBeeperDIP/manual/ErmerBeeperDIP_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/ErmerBeeperDIP/manual/ErmerBeeperDIP_de.pdf)
* **HeartDIP** — [EN](https://binary-kitchen.github.io/SolderingTutorial/HeartDIP/manual/HeartDIP_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/HeartDIP/manual/HeartDIP_de.pdf)
* **HeartSMD** — [EN](https://binary-kitchen.github.io/SolderingTutorial/HeartSMD/manual/HeartSMD_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/HeartSMD/manual/HeartSMD_de.pdf)
* **Humo** — [EN](https://binary-kitchen.github.io/SolderingTutorial/Humo/manual/Humo_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/Humo/manual/Humo_de.pdf)
* **ICanSolderDIP** — [EN](https://binary-kitchen.github.io/SolderingTutorial/ICanSolderDIP/manual/ICanSolderDIP_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/ICanSolderDIP/manual/ICanSolderDIP_de.pdf)
* **KatieTheCat** — [EN](https://binary-kitchen.github.io/SolderingTutorial/KatieTheCat/manual/KatieTheCat_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/KatieTheCat/manual/KatieTheCat_de.pdf)
* **KitchenHeadSMD** — [EN](https://binary-kitchen.github.io/SolderingTutorial/KitchenHeadSMD/manual/KitchenHeadSMD_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/KitchenHeadSMD/manual/KitchenHeadSMD_de.pdf)
* **LEDSchmuck** — [EN](https://binary-kitchen.github.io/SolderingTutorial/LEDSchmuck/manual/LEDSchmuck_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/LEDSchmuck/manual/LEDSchmuck_de.pdf)
* **LEDWolf** — [EN](https://binary-kitchen.github.io/SolderingTutorial/LEDWolf/manual/LEDWolf_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/LEDWolf/manual/LEDWolf_de.pdf)
* **Maus** — [EN](https://binary-kitchen.github.io/SolderingTutorial/Maus/manual/Maus_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/Maus/manual/Maus_de.pdf)
* **MoonCat** — [EN](https://binary-kitchen.github.io/SolderingTutorial/MoonCat/manual/MoonCat_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/MoonCat/manual/MoonCat_de.pdf)
* **MotoerBoerd** — [EN](https://binary-kitchen.github.io/SolderingTutorial/MotoerBoerd/manual/MotoerBoerd_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/MotoerBoerd/manual/MotoerBoerd_de.pdf)
* **NE555HeartSMD** — [EN](https://binary-kitchen.github.io/SolderingTutorial/NE555HeartSMD/manual/NE555HeartSMD_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/NE555HeartSMD/manual/NE555HeartSMD_de.pdf)
* **NE555HeartTHT** — [EN](https://binary-kitchen.github.io/SolderingTutorial/NE555HeartTHT/manual/NE555HeartTHT_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/NE555HeartTHT/manual/NE555HeartTHT_de.pdf)
* **NE555HeartTHT_v1.3_b-ware** — [EN](https://binary-kitchen.github.io/SolderingTutorial/NE555HeartTHT_v1.3_b-ware/manual/NE555HeartTHT_v1.3_b-ware_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/NE555HeartTHT_v1.3_b-ware/manual/NE555HeartTHT_v1.3_b-ware_de.pdf)
* **NibblePegDIP** — [EN](https://binary-kitchen.github.io/SolderingTutorial/NibblePegDIP/manual/NibblePegDIP_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/NibblePegDIP/manual/NibblePegDIP_de.pdf)
* **NibblePegDIPSwitch** — [EN](https://binary-kitchen.github.io/SolderingTutorial/NibblePegDIPSwitch/manual/NibblePegDIPSwitch_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/NibblePegDIPSwitch/manual/NibblePegDIPSwitch_de.pdf)
* **NibblePlusPlusSMD** — [EN](https://binary-kitchen.github.io/SolderingTutorial/NibblePlusPlusSMD/manual/NibblePlusPlusSMD_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/NibblePlusPlusSMD/manual/NibblePlusPlusSMD_de.pdf)
* **OpenDTU_Breakout** — [EN](https://binary-kitchen.github.io/SolderingTutorial/OpenDTU_Breakout/manual/OpenDTU_Breakout_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/OpenDTU_Breakout/manual/OpenDTU_Breakout_de.pdf)
* **OwlThiefDIP** — [EN](https://binary-kitchen.github.io/SolderingTutorial/OwlThiefDIP/manual/OwlThiefDIP_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/OwlThiefDIP/manual/OwlThiefDIP_de.pdf)
* **Pinecil_Case** — [EN](https://binary-kitchen.github.io/SolderingTutorial/Pinecil_Case/manual/Pinecil_Case_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/Pinecil_Case/manual/Pinecil_Case_de.pdf)
* **PushItDIP** — [EN](https://binary-kitchen.github.io/SolderingTutorial/PushItDIP/manual/PushItDIP_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/PushItDIP/manual/PushItDIP_de.pdf)
* **RainbowButterfly** — [EN](https://binary-kitchen.github.io/SolderingTutorial/RainbowButterfly/manual/RainbowButterfly_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/RainbowButterfly/manual/RainbowButterfly_de.pdf)
* **RainbowUnicorn01** — [EN](https://binary-kitchen.github.io/SolderingTutorial/RainbowUnicorn01/manual/RainbowUnicorn01_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/RainbowUnicorn01/manual/RainbowUnicorn01_de.pdf)
* **RingLightSMD** — [EN](https://binary-kitchen.github.io/SolderingTutorial/RingLightSMD/manual/RingLightSMD_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/RingLightSMD/manual/RingLightSMD_de.pdf)
* **RoboRobin** — [EN](https://binary-kitchen.github.io/SolderingTutorial/RoboRobin/manual/RoboRobin_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/RoboRobin/manual/RoboRobin_de.pdf)
* **RocketBadge** — [EN](https://binary-kitchen.github.io/SolderingTutorial/RocketBadge/manual/RocketBadge_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/RocketBadge/manual/RocketBadge_de.pdf)
* **SawToothOrganDIP** — [EN](https://binary-kitchen.github.io/SolderingTutorial/SawToothOrganDIP/manual/SawToothOrganDIP_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/SawToothOrganDIP/manual/SawToothOrganDIP_de.pdf)
* **ShittyRobots** — [EN](https://binary-kitchen.github.io/SolderingTutorial/ShittyRobots/manual/ShittyRobots_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/ShittyRobots/manual/ShittyRobots_de.pdf)
* **SmartLED** — [EN](https://binary-kitchen.github.io/SolderingTutorial/SmartLED/manual/SmartLED_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/SmartLED/manual/SmartLED_de.pdf)
* **SolarpunkSynth** — [EN](https://binary-kitchen.github.io/SolderingTutorial/SolarpunkSynth/manual/SolarpunkSynth_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/SolarpunkSynth/manual/SolarpunkSynth_de.pdf)
* **SolderBox** — [EN](https://binary-kitchen.github.io/SolderingTutorial/SolderBox/manual/SolderBox_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/SolderBox/manual/SolderBox_de.pdf)
* **SpaceEggs** — [EN](https://binary-kitchen.github.io/SolderingTutorial/SpaceEggs/manual/SpaceEggs_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/SpaceEggs/manual/SpaceEggs_de.pdf)
* **WeevilEye** — [EN](https://binary-kitchen.github.io/SolderingTutorial/WeevilEye/manual/WeevilEye_en.pdf) · [DE](https://binary-kitchen.github.io/SolderingTutorial/WeevilEye/manual/WeevilEye_de.pdf)

Source: [Binary Kitchen Soldering Tutorials](https://binary-kitchen.github.io/SolderingTutorial/?utm_source=chatgpt.com) ([binary-kitchen.github.io][1])

[1]: https://binary-kitchen.github.io/SolderingTutorial/?utm_source=chatgpt.com "Binary Kitchen Soldering Tutorials"
