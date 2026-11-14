# Runbook: automatischer Posting-Lauf

Arbeitsanweisung für die geplante Sitzung. Sie startet frisch, ohne
Kontext aus früheren Läufen. Alles Nötige steht hier.

Account: **@fachwirt_schulungen**, Instagram-ID `17841468136895555`,
erreichbar über den Windsor-Connector (`connector: "instagram"`).
Läuft dienstags und donnerstags um 19:41 Uhr.

## Ablauf

1. **Repo holen.** `add_repo` für `Spuhane/reel-fabrik` (access: push),
   dann klonen, wie das Ergebnis es anweist.

2. **Feiertag prüfen.** Fällt der heutige Tag auf den 24., 25. oder
   26. Dezember, den 31. Dezember oder den 1. Januar, wird nichts
   veröffentlicht. Dann nur eine kurze Meldung an Stefan, dass der
   Lauf wegen des Feiertags ausgesetzt hat.

3. **Nächsten Beitrag bestimmen.** `content/pool/` enthält die
   freigegebenen Beiträge, `state/posted.json` die bereits
   veröffentlichten. Nimm den Beitrag mit der **kleinsten `order`**,
   der noch nicht in `posted.json` steht und `"status":
   "freigegeben"` trägt.

   Die Reihenfolge in `order` ist bewusst gesetzt: Sie lässt die
   Inhaltstypen einander abwechseln, damit der Feed nicht eintönig
   wird. Nicht davon abweichen und nicht nach Thema oder Format
   auswählen.

4. **Gegen Instagram prüfen.** Lies über den Connector die Beiträge
   der letzten 7 Tage (`get_data`, Felder `media_permalink`,
   `timestamp`, `media_caption`). Steht der Beitrag dort schon, ist
   `posted.json` veraltet: trag ihn nach und nimm den nächsten.
   Dieser Schritt verhindert Doppelposts, falls ein früherer Lauf
   zwar veröffentlicht, aber nicht mehr pushen konnte.

5. **Medien-URLs nehmen.** Alles ist bereits gerendert. Die URLs
   stehen im Beitrag selbst: `images` (Liste von JPEG-URLs) oder
   `video` (eine MP4-URL). Nichts neu rendern, nichts selbst
   zusammenbauen.

6. **Veröffentlichen.** Die Caption ist immer `caption` + Leerzeile +
   die `hashtags` durch Leerzeichen getrennt. Welche Aktion gilt,
   entscheidet das Feld `format`:

   `format: "single"` (ein Bild in `images`):
   `execute_action(connector="instagram", action="create_image_post",
    account="17841468136895555",
    params={"image_url": <images[0]>, "caption": <caption>})`

   `format: "carousel"` (zwei oder drei Bilder in `images`):
   `execute_action(connector="instagram", action="create_carousel_post",
    account="17841468136895555",
    params={"image_urls": <images>, "caption": <caption>})`

   `format: "reel"` (eine MP4-URL in `video`):
   `execute_action(connector="instagram", action="create_video_post",
    account="17841468136895555",
    params={"video_url": <video>, "caption": <caption>, "share_to_feed": true})`

7. **Eintragen.** `id`, Datum, `media_id` und Permalink in
   `state/posted.json`, committen, pushen.

8. **Melden.** Kurze Nachricht an Stefan: was veröffentlicht wurde,
   welcher Typ, mit Permalink, und wie viele Beiträge noch im Pool
   liegen.

## Regeln

- **Nur aus `content/pool/` veröffentlichen, nur mit
  `"status": "freigegeben"`.** Alles andere ist ungeprüft.
- **Keine Inhalte selbst erfinden.** Weder Fragen noch Erklärungen,
  Rechenwege, Merksätze noch Captions. Was nicht im Pool steht, wird
  nicht veröffentlicht.
- **Jeder Hashtag beginnt mit `#`.** Ein Hashtag ohne Raute ist
  wirkungsloser Text.
- **Bei weniger als 6 verbleibenden Beiträgen:** im Meldetext darauf
  hinweisen und neue Inhalte zur Freigabe vorschlagen – nicht
  eigenmächtig welche ergänzen.
- **Ist der Pool leer:** nichts veröffentlichen, nur melden.
- **Scheitert ein Schritt:** nicht improvisieren, nicht mehrfach
  versuchen zu posten. Melden, was schiefging, und abbrechen.

## Inhaltstypen

| Typ | Folien | Was es ist |
|---|---|---|
| `quiz` | 3 oder Reel | Prüfungsfrage, Auflösung, Merksatz |
| `erklaerung` | 3 | Begriff, Erläuterung, Merksatz |
| `raetsel` | 2 | Rechenaufgabe, Lösung mit Rechenweg |
| `formel` | 1 | Formel mit ihren Bestandteilen |
| `verwechslung` | 1 | Zwei verwechselte Begriffe gegenübergestellt |

## Stilregeln

Siehe `STYLE.md`. Die gelten auch für jeden Meldetext und jeden
Vorschlag neuer Inhalte.
