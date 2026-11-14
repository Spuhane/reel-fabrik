#!/usr/bin/env python3
"""Baut die Erklaerungs- und Raetsel-Beitraege."""
import json

BASE = ["#wirtschaftsfachwirt", "#ihkprüfung", "#fachwirt", "#weiterbildung",
        "#aufstiegsfortbildung", "#prüfungsvorbereitung"]


def save(p, extra):
    p["brand"] = "wfw"
    p["status"] = "freigegeben"
    p["freigegeben_am"] = "2026-11-14"
    p["hashtags"] = BASE + extra
    n = {"erklaerung": 3, "raetsel": 2}[p["type"]]
    p["format"] = "carousel"
    p["images"] = [f"https://spuhane.github.io/reel-fabrik/posts/{p['id']}-{i}.jpg"
                   for i in range(1, n + 1)]
    json.dump(p, open(f"content/pool/{p['id']}.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return p["id"]


RW = "Rechnungswesen & Finanzen"
UF = "Unternehmensführung & Organisation"
HQIFC = "Investition & Controlling (HQ)"
HQLP = "Logistik & Prozesse (HQ)"
VWL = "VWL & Wirtschaftspolitik"

E = [
 dict(id="e-kuppelprodukt", type="erklaerung", topic=RW, track="WBQ",
      kicker="Kurz erklärt", begriff="Kuppelprodukt",
      untertitel="Wenn ein Prozess mehrere Produkte zugleich erzeugt",
      text="Bei der Erdölraffination entstehen Benzin, Diesel und Heizöl zwangsläufig gemeinsam. Keines lässt sich einzeln herstellen, also lassen sich die Kosten keinem Produkt direkt zurechnen. Man verteilt sie deshalb nachträglich, meist über den Marktwert der einzelnen Produkte.",
      merksatz="Ein Kuppelprodukt entsteht nicht freiwillig, sondern unvermeidlich mit.",
      caption="Kuppelprodukte sind der Grund, warum es in der Kostenrechnung Verteilungsverfahren gibt, die auf den ersten Blick willkürlich wirken.\n\nWenn aus einem Prozess zwangsläufig mehrere Produkte fallen, gibt es keine verursachungsgerechte Zurechnung. Man behilft sich mit dem Marktwert.\n\nKennst du ein Kuppelprodukt aus deinem Betrieb?",
      tags=["#kostenrechnung", "#rechnungswesen"]),

 dict(id="e-opportunitaetskosten", type="erklaerung", topic=VWL, track="WBQ",
      kicker="Kurz erklärt", begriff="Opportunitätskosten",
      untertitel="Der Wert dessen, worauf man verzichtet",
      text="Wer eine Halle für die eigene Produktion nutzt, zahlt dafür keine Miete. Trotzdem entstehen Kosten: die Miete, die man durch Vermietung hätte einnehmen können. Dieser entgangene Nutzen taucht in keiner Buchhaltung auf, gehört aber in jede Entscheidungsrechnung.",
      merksatz="Opportunitätskosten stehen in keiner Buchhaltung und entscheiden trotzdem mit.",
      caption="Die wichtigsten Kosten einer Entscheidung sind oft die, die niemand bucht.\n\nJede Ressource, die man so verwendet, kann man nicht anders verwenden. Was die beste verworfene Alternative gebracht hätte, ist der wahre Preis der Entscheidung.\n\nIn Investitionsaufgaben ist das der Unterschied zwischen richtig und fast richtig.",
      tags=["#vwl", "#entscheidung"]),

 dict(id="e-make-or-buy", type="erklaerung", topic=HQLP, track="HQ",
      kicker="Kurz erklärt", begriff="Make or Buy",
      untertitel="Selbst fertigen oder zukaufen?",
      text="Für die Rechnung zählen nur die Kosten, die sich durch die Entscheidung ändern. Fixkosten, die ohnehin weiterlaufen, gehören nicht in den Vergleich. Dazu kommen Gründe, die sich schlecht beziffern lassen: Abhängigkeit vom Lieferanten, eigenes Know-how, Lieferzeiten.",
      merksatz="Vergleiche nur, was sich durch die Entscheidung ändert.",
      caption="Die Make-or-Buy-Rechnung geht fast immer an derselben Stelle schief: Jemand rechnet die vollen Selbstkosten gegen den Einkaufspreis.\n\nRichtig ist der Vergleich der entscheidungsrelevanten Kosten. Eine Halle, die so oder so dasteht, macht die Eigenfertigung nicht teurer.\n\nWie entscheidet ihr das im Betrieb?",
      tags=["#logistik", "#einkauf"]),

 dict(id="e-cashflow", type="erklaerung", topic=RW, track="WBQ",
      kicker="Kurz erklärt", begriff="Cashflow",
      untertitel="Was tatsächlich an Geld hereinkommt",
      text="Der Gewinn aus der GuV enthält Positionen, die kein Geld bewegen, allen voran Abschreibungen. Rechnet man sie zum Gewinn hinzu, nähert man sich dem, was wirklich geflossen ist. Deshalb gilt der Cashflow als schwerer manipulierbar als der ausgewiesene Gewinn.",
      merksatz="Abschreibungen mindern den Gewinn, kosten aber kein Geld.",
      caption="Zwei Unternehmen mit demselben Gewinn können völlig unterschiedlich dastehen. Der Unterschied heißt Cashflow.\n\nAbschreibungen mindern den Gewinn, kosten aber in dieser Periode kein Geld. Wer das herausrechnet, sieht, was wirklich in der Kasse ankommt.\n\nSpeichern für die Bilanzanalyse.",
      tags=["#bilanz", "#finanzierung"]),

 dict(id="e-gegenstromverfahren", type="erklaerung", topic=UF, track="WBQ",
      kicker="Kurz erklärt", begriff="Gegenstromverfahren",
      untertitel="Planung von oben und von unten zugleich",
      text="Die Leitung gibt einen vorläufigen Rahmen vor. Die Fachbereiche prüfen ihn und melden zurück, was sie tatsächlich leisten können. Aus beiden Richtungen entsteht die endgültige Planung. Das dauert länger als reine Vorgaben von oben, wird aber von denen getragen, die sie umsetzen.",
      merksatz="Top-down setzt den Rahmen, bottom-up prüft ihn auf Machbarkeit.",
      caption="Zahlen, die von oben kommen, sind schnell beschlossen und selten erreicht. Zahlen, die nur von unten kommen, sind bequem.\n\nDas Gegenstromverfahren verbindet beides: Rahmen von oben, Realitätsprüfung von unten, Abstimmung dazwischen.\n\nWie läuft die Planung bei euch?",
      tags=["#unternehmensführung", "#planung"]),
]

R = [
 dict(id="r-breakeven", type="raetsel", topic=HQIFC, track="HQ",
      gegeben=[{"label": "Fixkosten", "wert": "50.000 €"},
               {"label": "Preis je Stück", "wert": "80 €"},
               {"label": "variable Kosten je Stück", "wert": "55 €"}],
      frage="Ab wie vielen Stück arbeitet der Betrieb gewinnbringend?",
      ergebnis="2.000 Stück",
      rechenweg="Der Deckungsbeitrag je Stück beträgt 80 € minus 55 €, also 25 €. Die Fixkosten von 50.000 € geteilt durch 25 € ergeben 2.000 Stück. Ab dem 2.001. Stück entsteht Gewinn.",
      caption="Eine Aufgabe, die so oder ganz ähnlich in jeder zweiten Prüfung steht.\n\nDer Weg ist immer derselbe: erst den Deckungsbeitrag je Stück, dann die Fixkosten dadurch teilen. Wer das Schema einmal sitzen hat, löst die Aufgabe in zwei Zeilen.\n\nHattest du die 2.000?",
      tags=["#controlling", "#kostenrechnung"]),

 dict(id="r-deckungsbeitrag", type="raetsel", topic=HQIFC, track="HQ",
      gegeben=[{"label": "Absatzmenge", "wert": "1.500 Stück"},
               {"label": "Preis je Stück", "wert": "120 €"},
               {"label": "variable Kosten je Stück", "wert": "85 €"}],
      frage="Wie hoch ist der gesamte Deckungsbeitrag?",
      ergebnis="52.500 €",
      rechenweg="Je Stück bleiben 120 € minus 85 €, also 35 €. Multipliziert mit 1.500 Stück ergibt das 52.500 €. Dieser Betrag steht zur Deckung der Fixkosten zur Verfügung.",
      caption="Zwei Rechenschritte, und trotzdem die Aufgabe, bei der in der Prüfung am häufigsten die Fixkosten mit hineinrutschen.\n\nDer Deckungsbeitrag kennt keine Fixkosten. Er sagt nur, was nach den variablen Kosten übrig bleibt.\n\nSchreib dein Ergebnis in die Kommentare.",
      tags=["#controlling", "#kostenrechnung"]),

 dict(id="r-eigenkapitalquote", type="raetsel", topic=RW, track="WBQ",
      gegeben=[{"label": "Eigenkapital", "wert": "180.000 €"},
               {"label": "Fremdkapital", "wert": "420.000 €"}],
      frage="Wie hoch ist die Eigenkapitalquote?",
      ergebnis="30 %",
      rechenweg="Das Gesamtkapital beträgt 180.000 € plus 420.000 €, also 600.000 €. Davon sind 180.000 € Eigenkapital. Das ergibt 30 Prozent.",
      caption="Die Falle steckt im Nenner. Gefragt ist der Anteil am Gesamtkapital, nicht das Verhältnis zum Fremdkapital.\n\nWer 180.000 durch 420.000 teilt, kommt auf 43 Prozent und liegt daneben. Erst addieren, dann teilen.\n\nBist du drauf reingefallen?",
      tags=["#bilanz", "#finanzierung"]),

 dict(id="r-lagerumschlag", type="raetsel", topic=HQLP, track="HQ",
      gegeben=[{"label": "Wareneinsatz", "wert": "600.000 €"},
               {"label": "Ø Lagerbestand", "wert": "75.000 €"}],
      frage="Wie oft schlägt das Lager im Jahr um?",
      ergebnis="8-mal",
      rechenweg="600.000 € geteilt durch 75.000 € ergibt 8. Das Lager erneuert sich also achtmal im Jahr, die durchschnittliche Lagerdauer beträgt rund 45 Tage.",
      caption="Aus der Umschlagshäufigkeit lässt sich direkt die Lagerdauer ableiten: 360 Tage geteilt durch 8 ergibt 45 Tage.\n\nBeide Kennzahlen werden in Logistikaufgaben gern nacheinander abgefragt. Wer die erste hat, hat die zweite geschenkt.\n\nWie lange liegt eure Ware?",
      tags=["#logistik", "#kennzahlen"]),
]

if __name__ == "__main__":
    ids = [save(p, p.pop("tags")) for p in E + R]
    print("Neu gebaut:", len(ids))
    for i in ids:
        print("  ", i)
