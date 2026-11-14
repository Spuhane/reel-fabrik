#!/usr/bin/env python3
import json, os
BASE = ["#wirtschaftsfachwirt", "#ihkprüfung", "#fachwirt", "#weiterbildung",
        "#aufstiegsfortbildung", "#prüfungsvorbereitung"]

def save(p, extra_tags):
    p["brand"] = "wfw"; p["status"] = "freigegeben"; p["freigegeben_am"] = "2026-11-14"
    p["hashtags"] = BASE + extra_tags
    n = {"formel": 1, "verwechslung": 1, "erklaerung": 3, "raetsel": 2}[p["type"]]
    p["format"] = "single" if n == 1 else "carousel"
    p["images"] = [f"https://spuhane.github.io/reel-fabrik/posts/{p['id']}-{i}.jpg"
                   for i in range(1, n + 1)]
    json.dump(p, open(f"content/pool/{p['id']}.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return p["id"]

RW, HQIFC, HQLP, BMC = ("Rechnungswesen & Finanzen", "Investition & Controlling (HQ)",
                        "Logistik & Prozesse (HQ)", "BWL, Marketing & Controlling")

F = [
 dict(id="f-deckungsbeitrag", type="formel", topic=RW, track="WBQ", title="Deckungsbeitrag",
  formel="Erlös − variable Kosten",
  teile=[{"label":"Erlös","text":"Was der Verkauf einbringt"},
         {"label":"variable K.","text":"Kosten, die je Stück anfallen: Material, Akkordlohn, Energie"},
         {"label":"Ergebnis","text":"Der Betrag, der zur Deckung der Fixkosten bleibt"}],
  caption="Der Deckungsbeitrag ist die meistgebrauchte Kennzahl der ganzen Prüfung – und die, bei der am häufigsten die Fixkosten hineingerechnet werden.\n\nSie gehören nicht hinein. Der Deckungsbeitrag sagt genau, was nach den variablen Kosten übrig bleibt, um die Fixkosten überhaupt erst zu decken.\n\nSpeicher dir die Karte für die Wiederholung.",
  tags=["#kostenrechnung","#controlling"]),

 dict(id="f-roi", type="formel", topic=BMC, track="WBQ", title="Return on Investment",
  formel="Umsatzrendite × Kapitalumschlag",
  teile=[{"label":"Umsatzrendite","text":"Gewinn geteilt durch Umsatz"},
         {"label":"Kapitalumschlag","text":"Umsatz geteilt durch eingesetztes Kapital"},
         {"label":"Ergebnis","text":"Wie viel das eingesetzte Kapital verdient"}],
  caption="Der ROI lässt sich auf zwei Wegen verbessern: mehr Gewinn je Euro Umsatz, oder mehr Umsatz je Euro Kapital.\n\nGenau das macht die DuPont-Zerlegung sichtbar. Wer in der Prüfung nur die Formel kennt, kann rechnen. Wer die zwei Stellschrauben kennt, kann argumentieren.\n\nAn welcher der beiden würdest du zuerst drehen?",
  tags=["#controlling","#kennzahlen"]),

 dict(id="f-eigenkapitalquote", type="formel", topic=RW, track="WBQ", title="Eigenkapitalquote",
  formel="Eigenkapital ÷ Gesamtkapital",
  teile=[{"label":"Eigenkapital","text":"Was den Eigentümern gehört"},
         {"label":"Gesamtkapital","text":"Die Summe der Passivseite, also Eigen- plus Fremdkapital"},
         {"label":"Ergebnis","text":"In Prozent: der Anteil, der nicht zurückgezahlt werden muss"}],
  caption="Die Eigenkapitalquote ist die erste Zahl, auf die eine Bank schaut. Sie sagt, wie viel Verlust ein Unternehmen aushält, bevor es den Gläubigern ans Geld geht.\n\nIn der Prüfung steckt die Falle meist im Nenner: Gesamtkapital, nicht Fremdkapital.\n\nSpeicher dir das für die Bilanzanalyse.",
  tags=["#bilanz","#finanzierung"]),

 dict(id="f-breakeven", type="formel", topic=HQIFC, track="HQ", title="Break-even-Menge",
  formel="Fixkosten ÷ DB je Stück",
  teile=[{"label":"Fixkosten","text":"Kosten, die unabhängig von der Menge anfallen"},
         {"label":"DB je Stück","text":"Preis minus variable Kosten je Stück"},
         {"label":"Ergebnis","text":"Die Stückzahl, ab der die Kosten gedeckt sind"}],
  caption="Am Break-even ist der Gewinn null – nicht maximal. Das ist die häufigste Verwechslung bei dieser Kennzahl.\n\nDie Rechnung selbst ist eine Division: Wie viele Deckungsbeiträge braucht es, um den Fixkostenblock zu füllen?\n\nWie sicher bist du bei Break-even-Aufgaben?",
  tags=["#controlling","#kostenrechnung"]),

 dict(id="f-lagerumschlag", type="formel", topic=HQLP, track="HQ", title="Lagerumschlagshäufigkeit",
  formel="Wareneinsatz ÷ Ø Lagerbestand",
  teile=[{"label":"Wareneinsatz","text":"Wert der Ware, die in der Periode verbraucht wurde"},
         {"label":"Ø Lagerbestand","text":"Durchschnitt aus Anfangs- und Endbestand"},
         {"label":"Ergebnis","text":"Wie oft sich das Lager im Jahr komplett erneuert"}],
  caption="Ein hoher Lagerumschlag bindet weniger Kapital. Ein zu hoher gefährdet die Lieferfähigkeit. Deshalb ist die Kennzahl in Logistikaufgaben fast immer eine Abwägung, keine Maximierung.\n\nAchte auf den Nenner: der Durchschnittsbestand, nicht der Endbestand.\n\nWie oft schlägt euer Lager im Jahr um?",
  tags=["#logistik","#kennzahlen"]),
]

V = [
 dict(id="v-aufwand-kosten", type="verwechslung", topic=RW, track="WBQ",
  title="Aufwand ist nicht Kosten",
  links={"name":"Aufwand","text":"Jeder Werteverzehr einer Periode, so wie ihn die Buchhaltung erfasst. Auch betriebsfremdes wie eine Spende."},
  rechts={"name":"Kosten","text":"Nur der Werteverzehr, der dem eigentlichen Betriebszweck dient. Die Spende zählt hier nicht mit."},
  merksatz="Jede Kostenart ist Aufwand. Nicht jeder Aufwand ist Kosten.",
  caption="Zwei Begriffe, die im Alltag dasselbe meinen und in der Prüfung nicht.\n\nDie Buchhaltung erfasst Aufwand, die Kostenrechnung rechnet mit Kosten. Dazwischen liegt alles, was zwar Geld kostet, aber nichts mit dem Betriebszweck zu tun hat.\n\nSpeicher dir die Abgrenzung, sie kommt in jeder Klausur zum Rechnungswesen vor.",
  tags=["#rechnungswesen","#kostenrechnung"]),

 dict(id="v-ertrag-leistung", type="verwechslung", topic=RW, track="WBQ",
  title="Ertrag ist nicht Leistung",
  links={"name":"Ertrag","text":"Der gesamte Wertzuwachs einer Periode nach Buchhaltung, auch aus dem Verkauf einer alten Maschine."},
  rechts={"name":"Leistung","text":"Nur der Wertzuwachs aus der eigentlichen betrieblichen Tätigkeit."},
  merksatz="Ertrag und Aufwand gehören zur Buchhaltung, Leistung und Kosten zur Kostenrechnung.",
  caption="Das Gegenstück zu Aufwand und Kosten – und genauso prüfungsrelevant.\n\nVerkauft ein Betrieb eine ausgemusterte Maschine, ist der Erlös Ertrag, aber keine Leistung. Mit dem eigentlichen Geschäft hat er nichts zu tun.\n\nMerkhilfe: Die beiden Begriffspaare laufen parallel.",
  tags=["#rechnungswesen","#kostenrechnung"]),

 dict(id="v-bilanz-guv", type="verwechslung", topic=RW, track="WBQ",
  title="Bilanz oder GuV?",
  links={"name":"Bilanz","text":"Eine Momentaufnahme zum Stichtag. Zeigt Vermögen und Kapital, also Bestände."},
  rechts={"name":"GuV","text":"Eine Zeitraumrechnung. Zeigt Aufwand und Ertrag einer ganzen Periode."},
  merksatz="Die Bilanz ist ein Foto, die GuV ein Film.",
  caption="Bestandsgrößen oder Stromgrößen – an dieser Unterscheidung hängt die halbe Bilanzbuchhaltung.\n\nEine Maschine steht in der Bilanz. Ihre Abschreibung steht in der GuV. Dasselbe Objekt, zwei Rechenwerke, zwei völlig verschiedene Fragen.\n\nSpeicher dir das Bild, es trägt durch viele Aufgaben.",
  tags=["#bilanz","#rechnungswesen"]),

 dict(id="v-skonto-rabatt", type="verwechslung", topic=BMC, track="WBQ",
  title="Skonto ist kein Rabatt",
  links={"name":"Rabatt","text":"Ein Preisnachlass, der von vornherein gewährt wird, etwa für große Mengen oder treue Kunden."},
  rechts={"name":"Skonto","text":"Ein Abzug fürs schnelle Zahlen. Er belohnt nicht den Kauf, sondern den Zahlungszeitpunkt."},
  merksatz="Rabatt gilt für den Kauf, Skonto für die Zahlung.",
  caption="Skonto sieht nach einem kleinen Nachlass aus und ist in Wahrheit ein teurer Kredit – für den, der ihn nicht zieht.\n\n2 Prozent Skonto bei 30 Tagen Ziel entsprechen aufs Jahr gerechnet einem zweistelligen Zinssatz. Genau das wird in Prüfungsaufgaben gerechnet.\n\nZieht ihr Skonto konsequent?",
  tags=["#einkauf","#bwl"]),

 dict(id="v-liquiditaet-rentabilitaet", type="verwechslung", topic=RW, track="WBQ",
  title="Liquidität ist nicht Rentabilität",
  links={"name":"Liquidität","text":"Die Fähigkeit, Rechnungen pünktlich zu bezahlen. Eine Frage des Zeitpunkts."},
  rechts={"name":"Rentabilität","text":"Das Verhältnis von Gewinn zum eingesetzten Kapital. Eine Frage des Erfolgs."},
  merksatz="An fehlender Rentabilität stirbt ein Betrieb langsam. An fehlender Liquidität sofort.",
  caption="Ein Unternehmen kann profitabel sein und trotzdem insolvent gehen. Das klingt widersprüchlich und ist der häufigste Grund für Insolvenzen im Mittelstand.\n\nGewinn steht in der GuV. Liquidität steht auf dem Konto. Zwischen beiden liegen Zahlungsziele, Lagerbestände und offene Forderungen.\n\nWelche der beiden beobachtet ihr enger?",
  tags=["#finanzierung","#controlling"]),
]

ids = [save(p, p.pop("tags")) for p in F + V]
print("Neu gebaut:", len(ids))
for i in ids: print("  ", i)
