# Runbook: wöchentlicher Reel-Lauf

Diese Datei ist die Arbeitsanweisung für die geplante Sitzung.
Sie startet frisch und hat keinen Kontext aus früheren Läufen.

## Ablauf

1. **Repo klonen** und in das Verzeichnis wechseln.
2. **Nächsten Tipp wählen:** `content/pool/` enthält freigegebene Tipps.
   `state/posted.json` listet bereits veröffentlichte IDs. Nimm den ersten
   Tipp, der dort noch nicht steht. Ist der Pool leer → Schritt 7.
3. **Rendern:**
   `python3 render.py content/pool/<id>.json brand/<brand>.json docs/reels/<id>.mp4`
4. **Hochladen:** MP4 nach `docs/reels/` committen und pushen.
   Öffentliche URL danach:
   `https://<user>.github.io/<repo>/reels/<id>.mp4`
   Vor dem Posten einmal abrufen und auf HTTP 200 prüfen — GitHub Pages
   braucht nach dem Push bis zu zwei Minuten.
5. **Veröffentlichen** über den Windsor-Connector:
   `execute_action(connector="instagram", action="create_video_post",
    account="<IG_ACCOUNT_ID>", params={"video_url": "<URL>", "caption": "<caption + hashtags>"})`
   Instagram macht aus jedem Einzelvideo automatisch ein Reel.
6. **Eintragen:** ID mit Datum und Permalink in `state/posted.json`, committen.
7. **Melden:** Kurze Nachricht an Stefan — was gepostet wurde, mit Permalink.
   Ist der Pool fast leer (< 4 Tipps), im selben Zug neue Tipps zur
   Freigabe vorschlagen statt selbst welche zu ergänzen.

## Regeln

- **Niemals einen Tipp posten, der nicht in `content/pool/` liegt.**
  Der Pool ist von Stefan freigegeben; alles andere ist ungeprüft.
- Caption = `caption` aus dem JSON + Leerzeile + Hashtags, jeder mit `#`.
- Scheitert ein Schritt, nicht improvisieren: melden und abbrechen.
