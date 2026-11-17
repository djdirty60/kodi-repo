# djdirty60 Kodi-repository

Automatische updates voor de eigen Kodi-add-ons van djdirty60:

- **NLZiet** (`plugin.video.nlziet`)
- **Videoland** (`plugin.video.videoland.nl`)

## Installeren (één keer)
1. Installeer `zips/repository.djdirty/repository.djdirty-1.0.0.zip` in Kodi
   (Add-ons → Installeren vanuit zip-bestand).
2. De add-ons staan daarna onder **Add-ons → Installeren vanuit repository →
   djdirty60 Add-ons → Videoadd-ons**.
3. Zet in Kodi *Instellingen → Add-ons → Updates* op **Updates automatisch
   installeren** voor automatische updates.

## Een nieuwe versie publiceren
Bouw de add-on(s), draai daarna `python generate.py` in de repo-root en commit/push.
Dat ververst `zips/addons.xml`, de checksum en de zip-bestanden.
