#!/usr/bin/env python3
"""Baut aus den Kandidaten die freigabefertigen Karussell-Posts."""
import json, os, re

SOCIAL = {
"BMC-40": ("Wie berechnet sich die Umsatzrendite?",
 "Die Umsatzrendite setzt den Gewinn ins Verhältnis zum Umsatz. Sie beantwortet die Frage, wie viel von jedem Euro Umsatz am Ende als Gewinn übrig bleibt. In der DuPont-Zerlegung ist sie einer der beiden Faktoren des Return on Investment.",
 "Zwei Unternehmen machen denselben Umsatz – und verdienen völlig unterschiedlich daran. Die Umsatzrendite macht diesen Unterschied sichtbar.\n\nZusammen mit dem Kapitalumschlag ergibt sie den ROI. Wer beide Kennzahlen auseinanderhalten kann, hat in der Prüfung schon die halbe Aufgabe gelöst.\n\nHättest du sie gewusst?",
 ["#controlling", "#kennzahlen", "#bwl"]),

"BMC-41": ("Wie berechnet sich der Kapitalumschlag?",
 "Der Kapitalumschlag zeigt, wie oft das eingesetzte Kapital im Umsatz umgeschlagen wird. Je mehr Umsatz ein Unternehmen aus demselben Kapital erzielt, desto besser fällt der Return on Investment aus.",
 "Umsatzrendite und Kapitalumschlag werden in der Prüfung gern verwechselt – dabei stehen Zähler und Nenner genau andersherum.\n\nMerkhilfe: Beim Umschlag steht der Umsatz oben. Beides zusammen ergibt den ROI.\n\nWelche Kennzahl bereitet dir am meisten Kopfzerbrechen?",
 ["#controlling", "#kennzahlen", "#bwl"]),

"HQ_BM-47": ("Was ist eine Stabsstelle?",
 "Stabsstellen unterstützen die Führung mit Fachwissen, etwa Recht, Controlling oder Qualitätsmanagement. Sie beraten und bereiten Entscheidungen vor, dürfen aber selbst keine Weisungen erteilen. Genau diese fehlende Weisungsbefugnis ist das Prüfungsmerkmal.",
 "Die Stabsstelle ist ein Klassiker – und die Falle steckt immer an derselben Stelle: Beratung ja, Weisung nein.\n\nWer das verwechselt, verliert Punkte bei jeder Aufgabe zur Aufbauorganisation.\n\nSpeicher dir das für die Wiederholung.",
 ["#organisation", "#unternehmensführung"]),

"HQ_BM-76": ("Womit priorisiert man schnell eine große Menge an Ideen?",
 "Bei der Punktabfrage bekommt jede Person eine feste Zahl an Klebepunkten und verteilt sie auf die gesammelten Ideen. In wenigen Minuten entsteht so eine Rangfolge, die alle mitgetragen haben.",
 "Zwanzig Ideen auf dem Flipchart und eine halbe Stunde Zeit: Die Punktabfrage löst das zuverlässiger als jede Diskussionsrunde.\n\nFunktioniert im Workshop genauso wie in der Prüfungsaufgabe zur Moderation.\n\nNutzt ihr das im Betrieb?",
 ["#moderation", "#projektmanagement"]),

"HQ_FZ-45": ("Welche Maßnahme zählt zur Personalentwicklung on the job?",
 "On the job heißt: Die Entwicklung findet direkt am Arbeitsplatz statt. Dazu zählen Job Rotation, Projektarbeit, Job Enlargement und Job Enrichment. Assessment-Center und Seminare laufen dagegen außerhalb der eigentlichen Tätigkeit.",
 "On the job, off the job, near the job – drei Begriffe, die in der Prüfung regelmäßig durcheinandergeraten.\n\nDie Trennlinie ist einfach: Passiert es am Arbeitsplatz selbst oder daneben?\n\nWelche Maßnahme hast du zuletzt im Betrieb erlebt?",
 ["#personalentwicklung", "#führung"]),

"HQ_FZ-92": ("Wozu dient ein Ishikawa-Diagramm?",
 "Das Ishikawa-Diagramm, auch Fischgräten- oder Ursache-Wirkungs-Diagramm genannt, ordnet mögliche Ursachen eines Problems nach Kategorien wie Mensch, Maschine, Material und Methode. So wird sichtbar, wo die Suche nach der Wurzelursache ansetzen sollte.",
 "Wenn der Ausschuss steigt und keiner weiß warum: Das Ishikawa-Diagramm sortiert die Ursachen, statt sie zu erraten.\n\nMensch, Maschine, Material, Methode – die vier M sind der Einstieg. Qualitätsmanagement-Aufgaben greifen das gern auf.\n\nSpeichern für die Prüfung.",
 ["#qualitätsmanagement", "#prozesse"]),

"HQ_IFC-69": ("Was passiert am Break-even-Punkt?",
 "Am Break-even-Punkt deckt der Umsatz exakt die Gesamtkosten aus Fixkosten und variablen Kosten. Der Gewinn ist genau null. Jede weitere verkaufte Einheit bringt ab diesem Punkt Gewinn.",
 "Der Break-even ist nicht der Punkt des höchsten Gewinns – das ist die häufigste Verwechslung.\n\nEr ist der Punkt, an dem der Verlust aufhört. Gewinn null, alle Kosten gedeckt. Erst danach wird verdient.\n\nWie sicher bist du bei Break-even-Aufgaben?",
 ["#controlling", "#kostenrechnung"]),

"HQ_IFC-24": ("Welche Form gehört zur Außenfinanzierung?",
 "Außenfinanzierung bedeutet, dass Kapital von außen zufließt, etwa durch Einlagen der Gesellschafter oder durch Kredite. Rücklagenbildung, Selbstfinanzierung und Abschreibungsgegenwerte entstehen dagegen im Unternehmen selbst und zählen zur Innenfinanzierung.",
 "Innen- oder Außenfinanzierung? Die Frage ist immer: Kommt das Geld von außen herein oder entsteht es im Unternehmen?\n\nGesellschaftereinlagen und Kredite kommen von außen. Alles, was aus dem eigenen Umsatz stammt, bleibt innen.\n\nSpeicher dir die Systematik.",
 ["#finanzierung", "#bwl"]),

"HQ_LP-52": ("Welche Kennzahl misst die Lieferperformance?",
 "Die Termintreue gibt an, welcher Anteil der Lieferungen zum zugesagten Termin beim Kunden ankommt. Sie misst damit die Zuverlässigkeit gegenüber dem Kunden, während Lagerumschlag und ROI andere Fragen beantworten.",
 "Termintreue ist die Kennzahl, an der Kunden eine Lieferbeziehung bewerten – nicht am Preis und nicht am Lagerbestand.\n\nIn Logistikaufgaben wird sie gern gegen andere Kennzahlen gestellt, die ganz andere Dinge messen.\n\nWie steht ihr bei der Termintreue da?",
 ["#logistik", "#kennzahlen"]),

"HQ_MV-63": ("Wofür steht CRM?",
 "CRM steht für Customer Relationship Management. Gemeint ist die systematische Pflege der Kundenbeziehungen über alle Kontaktpunkte hinweg, meist gestützt auf eine Software, die Kundendaten und Vorgänge bündelt.",
 "CRM ist eine dieser Abkürzungen, die jeder benutzt und in der Prüfung trotzdem danebengeht.\n\nCustomer Relationship Management – es geht um die Beziehung, nicht um die Software. Die ist nur das Werkzeug.\n\nWelche Abkürzung bringt dich am meisten ins Schwitzen?",
 ["#marketing", "#vertrieb"]),

"HQ_MV-60": ("Wofür steht SEA im Online-Marketing?",
 "SEA steht für Search Engine Advertising, also bezahlte Anzeigen in Suchmaschinen wie Google Ads. Davon zu unterscheiden ist SEO, die Suchmaschinenoptimierung, die auf unbezahlte Treffer zielt.",
 "SEA und SEO klingen fast gleich und meinen das Gegenteil voneinander: einmal bezahlt, einmal organisch.\n\nIn Marketingaufgaben steht fast immer diese Abgrenzung im Mittelpunkt.\n\nSpeicher dir den Unterschied, bevor die Prüfung danach fragt.",
 ["#marketing", "#onlinemarketing"]),

"PLQP-16": ("Wie lange darf ein Daily Scrum höchstens dauern?",
 "Das Daily Scrum ist auf 15 Minuten begrenzt. In dieser Zeit synchronisiert sich das Team über Fortschritt, Hindernisse und die Planung des Tages. Die kurze Dauer ist Teil des Formats, nicht eine Empfehlung.",
 "Fünfzehn Minuten, im Stehen, jeden Tag. Wer das Daily länger zieht, hat kein Daily mehr, sondern ein Meeting.\n\nIn Prüfungsaufgaben zu agilen Methoden wird die Zeitbegrenzung gern abgefragt.\n\nWie lange dauern eure Dailys wirklich?",
 ["#agil", "#projektmanagement", "#scrum"]),

"PLQP-19": ("Wozu dient die 5-Why-Methode?",
 "Bei der 5-Why-Methode wird fünfmal hintereinander nach dem Warum gefragt, bis man von der sichtbaren Störung bei der eigentlichen Wurzelursache ankommt. Sie verhindert, dass nur das Symptom behoben wird.",
 "Die Maschine stand still. Warum? Und warum? Und warum?\n\nNach dem fünften Warum steht meistens eine ganz andere Ursache da als die, die man zuerst vermutet hat. Genau das ist der Zweck der Methode.\n\nKennst du das aus deinem Betrieb?",
 ["#qualitätsmanagement", "#prozesse"]),

"RFI-111": ("Wofür steht FIFO?",
 "FIFO steht für First In, First Out. Die zuerst beschafften Güter werden zuerst entnommen oder verbraucht. In der Bewertung bedeutet das, dass der Lagerbestand mit den Preisen der jüngsten Zugänge bewertet wird.",
 "FIFO klingt nach Lagerorganisation und ist zugleich ein Bewertungsverfahren im Rechnungswesen. Beide Seiten können geprüft werden.\n\nFirst In, First Out: Was zuerst kam, geht zuerst raus.\n\nWie sicher bist du bei den Bewertungsverfahren?",
 ["#rechnungswesen", "#lager"]),

"RFI-17": ("Was kennzeichnet Gemeinkosten?",
 "Gemeinkosten lassen sich einem einzelnen Kostenträger nicht direkt zurechnen. Miete, Energie oder Verwaltung fallen für den gesamten Betrieb an und werden über Zuschlagssätze verteilt. Einzelkosten dagegen gehören direkt zu einem Produkt.",
 "Einzelkosten oder Gemeinkosten? Die Prüfungsfrage lautet nie anders als: Kann ich diese Kosten einem Produkt direkt zuordnen?\n\nMiete und Verwaltung kann man nicht. Deshalb der Umweg über Zuschlagssätze im BAB.\n\nSpeicher dir die Abgrenzung.",
 ["#rechnungswesen", "#kostenrechnung"]),

"RS-66": ("Was regelt § 169 AO?",
 "§ 169 der Abgabenordnung regelt die Festsetzungsverjährung, also die Fristen, innerhalb derer das Finanzamt eine Steuer noch festsetzen oder ändern darf. Nach Ablauf dieser Frist ist eine Änderung nicht mehr möglich.",
 "Paragrafen auswendig zu lernen bringt wenig – ein paar zentrale sollte man aber zuordnen können.\n\n§ 169 AO ist einer davon: Festsetzungsverjährung. Danach ist für das Finanzamt Schluss.\n\nWelcher Paragraf will bei dir einfach nicht hängenbleiben?",
 ["#steuerrecht", "#recht"]),

"UF-100": ("Outcome oder Output – worin liegt der Unterschied?",
 "Output ist die erzeugte Menge, also was ein Prozess hervorbringt. Outcome ist die Wirkung, die damit erzielt wird. Zehn Schulungen sind Output. Dass danach weniger Fehler passieren, ist der Outcome.",
 "Zehn Schulungen durchgeführt klingt nach Erfolg. Aber was hat sich dadurch verändert?\n\nOutput ist die Menge, Outcome die Wirkung. Zielvereinbarungen, die nur den Output messen, steuern am eigentlichen Zweck vorbei.\n\nWoran werdet ihr gemessen?",
 ["#unternehmensführung", "#controlling"]),

"UF-06": ("Situatives Führen: Welcher Stil passt zu Reifegrad R4?",
 "Reifegrad R4 beschreibt Mitarbeitende, die fachlich kompetent und zugleich motiviert sind. Dafür ist Delegating der passende Stil: hohe Autonomie, wenig Steuerung. Telling eignet sich dagegen für R1, wenn weder Können noch Zutrauen vorhanden sind.",
 "Situatives Führen heißt: Der Stil richtet sich nach der Person, nicht nach der Vorliebe der Führungskraft.\n\nWer kompetent und motiviert ist, braucht keine Anweisungen, sondern Freiraum. Alles andere bremst.\n\nWelcher Führungsstil begegnet dir am häufigsten?",
 ["#führung", "#unternehmensführung"]),

"VWL-28": ("Wie lautet die Quantitätsgleichung?",
 "Die Quantitätsgleichung lautet M mal V gleich P mal Y: Geldmenge mal Umlaufgeschwindigkeit entspricht Preisniveau mal realem Bruttoinlandsprodukt. Sie ist die Grundlage für die Erklärung, wie Geldmenge und Inflation zusammenhängen.",
 "Vier Buchstaben, eine Gleichung – und die ganze Diskussion über Geldmenge und Inflation steckt darin.\n\nM mal V gleich P mal Y. Wächst die Geldmenge schneller als die Produktion, steigt bei gleicher Umlaufgeschwindigkeit das Preisniveau.\n\nSpeicher dir die Formel.",
 ["#vwl", "#geldpolitik"]),

"VWL-10": ("Nominales oder reales BIP – was ist der Unterschied?",
 "Das nominale Bruttoinlandsprodukt wird zu den Preisen des laufenden Jahres gerechnet, das reale zu konstanten Preisen eines Basisjahres. Nur das reale BIP zeigt echtes Wachstum, weil die Preisentwicklung herausgerechnet ist.",
 "Die Wirtschaft ist um vier Prozent gewachsen – nominal. Real waren es vielleicht eins.\n\nDer Unterschied ist die Inflation. Wer beide Größen verwechselt, liest jede Konjunkturmeldung falsch.\n\nWie sicher bist du bei den VWL-Grundbegriffen?",
 ["#vwl", "#konjunktur"]),

"HQ_LP-36": ("Welche Transportart ist die schnellste?",
 "Luftfracht ist die schnellste Transportart, zugleich aber die teuerste je Tonnenkilometer. In Logistikaufgaben geht es deshalb fast immer um den Zielkonflikt zwischen Geschwindigkeit, Kosten und Transportmenge.",
 "Am schnellsten heißt nicht am besten. Luftfracht gewinnt bei der Zeit und verliert beim Preis.\n\nLogistikaufgaben prüfen fast nie eine Transportart allein, sondern die Abwägung zwischen Zeit, Kosten und Menge.\n\nWelches Verkehrsmittel nutzt ihr am häufigsten?",
 ["#logistik", "#transport"]),

"RS-108": ("Wie hoch ist der Körperschaftsteuersatz?",
 "Der Körperschaftsteuersatz beträgt 15 Prozent des zu versteuernden Einkommens. Hinzu kommt der Solidaritätszuschlag auf die Körperschaftsteuer, außerdem fällt für den Gewerbebetrieb noch Gewerbesteuer an.",
 "Fünfzehn Prozent Körperschaftsteuer – das ist nur der erste Teil der Rechnung.\n\nDazu kommen Solidaritätszuschlag und Gewerbesteuer. Deshalb liegt die tatsächliche Belastung einer Kapitalgesellschaft deutlich höher.\n\nSpeicher dir die Systematik.",
 ["#steuerrecht", "#recht"]),
}

BASE_TAGS = ["#wirtschaftsfachwirt", "#ihkprüfung", "#fachwirt", "#weiterbildung",
             "#aufstiegsfortbildung", "#prüfungsvorbereitung"]

cands = {q["id"]: q for q in json.load(open("work/candidates.json", encoding="utf-8"))}
os.makedirs("content/pool", exist_ok=True)
built = []
for qid, (sq, expl, caption, tags) in SOCIAL.items():
    q = cands.get(qid)
    if not q:
        print("FEHLT in Kandidaten:", qid); continue
    slug = "q-" + qid.lower().replace("_", "-")
    post = {
        "id": slug, "type": "carousel", "brand": "wfw", "status": "entwurf",
        "source_question_id": qid, "topic": q["_topic_name"], "track": q["_track"],
        "question": {"id": qid, "question": q["question"], "social_question": sq,
                     "options": q["options"], "correct": q["correct"]},
        "explanation": expl,
        "caption": caption,
        "hashtags": BASE_TAGS + tags,
    }
    json.dump(post, open(f"content/pool/{slug}.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    built.append(slug)
print("Posts gebaut:", len(built))
