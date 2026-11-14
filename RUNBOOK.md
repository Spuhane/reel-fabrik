# Runbook: automatischer Posting-Lauf

Arbeitsanweisung für die geplante Sitzung. Sie startet frisch, ohne
Kontext aus früheren Läufen. Alles Nötige steht hier.

Account: **@fachwirt_schulungen**, Instagram-ID `17841468136895555`,
erreichbar über den Windsor-Connector (`connector: "instagram"`).

## Ablauf

1. **Repo holen.** `add_repo` für `Spuhane/reel-fabrik` (access: push),
   dann klonen, wie das Ergebnis es anweist.

2. **Nächsten Post bestimmen.** `content/pool/` enthält die
   freigegebenen Posts, `state/posted.json` die bereits
   veröffentlichten. Nimm den ersten Post mit
   `"status": "freigegeben"`, dessen `id` noch nicht in
   `posted.json` steht. Reihenfolge: nach Themengebiet abwechselnd,
   damit nicht zwei Posts desselben Gebiets aufeinanderfolgen.

3. **Gegen Instagram prüfen.** Lies über den Connector die Beiträge
   der letzten 7 Tage (`get_data`, Felder `media_permalink`,
   `timestamp`, `media_caption`). Steht der Post dort schon, ist
   `posted.json` veraltet: trag ihn nach und nimm den nächsten.
   Dieser Schritt verhindert Doppelposts, falls ein früherer Lauf
   zwar gepostet, aber nicht mehr pushen konnte.

4. **Bild-URLs bilden.** Die Folien sind bereits gerendert und liegen
   unter `docs/posts/`. Öffentlich erreichbar sind sie als
   `https://spuhane.github.io/reel-fabrik/posts/<id>-1.jpg` (ebenso -2, -3).
   Nichts neu rendern.

5. **Veröffentlichen.**
   `execute_action(connector="instagram", action="create_carousel_post",
    account="17841468136895555",
    params={"image_urls": [<URL 1>, <URL 2>, <URL 3>],
            "caption": <caption> + "\n\n" + <hashtags, durch Leerzeichen getrennt>})`

6. **Eintragen.** `id`, Datum, `media_id` und Permalink in
   `state/posted.json`, committen, pushen.

7. **Melden.** Kurze Nachricht an Stefan: was gepostet wurde, mit
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
