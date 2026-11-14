# Runbook: automatischer Posting-Lauf

Arbeitsanweisung für die geplante Sitzung. Sie startet frisch, ohne
Kontext aus früheren Läufen. Alles Nötige steht hier.

Account: **@fachwirt_schulungen**, Instagram-ID `17841468136895555`,
erreichbar über den Windsor-Connector (`connector: "instagram"`).

## Ablauf

1. **Repo holen.** `add_repo` für `Spuhane/reel-fabrik` (access: push),
   dann klonen, wie das Ergebnis es anweist.

2. **Feiertag prüfen.** Fällt der heutige Tag auf den 24., 25.
   oder 26. Dezember, den 31. Dezember oder den 1. Januar, wird
   nichts veröffentlicht. Dann nur eine kurze Meldung an Stefan,
   dass der Lauf wegen des Feiertags ausgesetzt hat.

3. **Nächsten Post bestimmen.** `content/pool/` enthält die
   freigegebenen Posts, `state/posted.json` die bereits
   veröffentlichten. Jeder Post trägt ein Feld `format`
   (`carousel` oder `reel`) und ein Feld `order`.
   Dienstags: der Post mit `format: "carousel"` und der kleinsten
   `order`, der noch nicht in `posted.json` steht.
   Donnerstags: derselbe Griff, aber `format: "reel"`.
   Ist für den jeweiligen Wochentag keiner mehr übrig, nimm den
   nächsten aus dem anderen Format.
   Die Reihenfolge ist in `order` festgelegt und wechselt bereits
   zwischen den Themengebieten. Nicht davon abweichen.

4. **Gegen Instagram prüfen.** Lies über den Connector die Beiträge
   der letzten 7 Tage (`get_data`, Felder `media_permalink`,
   `timestamp`, `media_caption`). Steht der Post dort schon, ist
   `posted.json` veraltet: trag ihn nach und nimm den nächsten.
   Dieser Schritt verhindert Doppelposts, falls ein früherer Lauf
   zwar gepostet, aber nicht mehr pushen konnte.

5. **Medien-URLs nehmen.** Alles ist bereits gerendert. Die URLs
   stehen im Post selbst: `images` (drei JPEG-URLs) beim Karussell,
   `video` (eine MP4-URL) beim Reel. Nichts neu rendern, nichts
   selbst zusammenbauen.

6. **Veröffentlichen.** Caption ist immer
   `caption` + Leerzeile + Hashtags durch Leerzeichen getrennt.

   Karussell:
   `execute_action(connector="instagram", action="create_carousel_post",
    account="17841468136895555",
    params={"image_urls": <images>, "caption": <caption>})`

   Reel:
   `execute_action(connector="instagram", action="create_video_post",
    account="17841468136895555",
    params={"video_url": <video>, "caption": <caption>, "share_to_feed": true})`

7. **Eintragen.** `id`, Datum, `media_id` und Permalink in
   `state/posted.json`, committen, pushen.

8. **Melden.** Kurze Nachricht an Stefan: was gepostet wurde, mit
   Permalink, und wie viele Posts noch im Pool liegen.

## Regeln

- **Nur aus `content/pool/` posten, nur mit `"status": "freigegeben"`.**
  Alles andere ist ungeprüft und bleibt liegen.
- **Keine Inhalte selbst erfinden.** Weder Fragen noch Erklärungen
  noch Captions. Was nicht im Pool steht, wird nicht gepostet.
- **Jeder Hashtag beginnt mit `#`.** Ein Hashtag ohne Raute ist
  wirkungsloser Text.
- **Bei weniger als 4 verbleibenden Posts:** im Meldetext darauf
  hinweisen und neue Fragen zur Freigabe vorschlagen – nicht
  eigenmächtig welche ergänzen.
- **Ist der Pool leer:** nichts posten, nur melden.
- **Scheitert ein Schritt:** nicht improvisieren, nicht mehrfach
  versuchen zu posten. Melden, was schiefging, und abbrechen.

## Stilregeln

Siehe `STYLE.md`. Die gelten auch für jeden Meldetext und jeden
Vorschlag neuer Inhalte.
