# Reel-Fabrik

Erzeugt Instagram-Reels (1080x1920, MP4) aus Text-Tipps und veröffentlicht sie
auf @fachwirt_schulungen.

    python3 render.py content/pool/wfw-001.json brand/wfw.json docs/reels/wfw-001.mp4

## Struktur

    brand/        Farben, Logo, URL je Marke (wfw, hfw, sw)
    content/pool/ von Stefan freigegebene Tipps — nur daraus wird gepostet
    docs/reels/   gerenderte MP4s, via GitHub Pages öffentlich erreichbar
    state/        was bereits veröffentlicht wurde
    render.py     Renderer (Pillow + ffmpeg)
    RUNBOOK.md    Arbeitsanweisung für den wöchentlichen Lauf

## Voraussetzungen

Python 3 mit Pillow und numpy, ffmpeg, Inter-Schriftfamilie.

## Keine Zugangsdaten

Der Instagram-Zugang liegt im Windsor.ai-Connector, nicht in diesem Repo.
Hier gehören keine Tokens, Passwörter oder Schlüssel hinein.
