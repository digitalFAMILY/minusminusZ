Requested features
==================

- Kommandos von ASCII 1-31
- Keine Schleifen
- Goto mit "Schlüsselwort", welches vorher eindeutig im Quelltext vorgekommen ist
- alle zahlen in 8 bit
- if: goto wenn vorher ein True im Speicher steht
- keine block-klammern
- kein unicode
- lochkarten gui
- jit compiler
- rückwärtsablauf des programms
- interpreter
- Vorl. Name: --Z
- keine funktionen, nur subroutinen
- keine arrays, nur pointer
- nur file I/O mit FIFOs
- subroutine muss prüfsumme der zeile beinhalten

Syntax
======

Die Syntax von --Z ist sehr trivial
- Programm läuft von unten nach oben ab
- Anweisungen bestehen aus den vergessenen Ersten 31 Ascii Zeichen.
- keine Blockklammern
- am Ende jeder Zeile muss eine Prüfsumme stehen
- Wertübergabe nur mit Variablen (kein callback, kein return)

Datentypen
----------

In --Z gibt es eine Handvoll Datentypen und ein paar statische Elemente, die man kennen sollte.
Integer, Float und String Variablen werden automatisch deklariert und können nachträglich nicht geändert werden. true und false nehmen einen besonderen Platz ein, sie haben die bool-Werte true und false und werden i.d.R. für Vergleiche genutzt.

Prüfsumme
---------

Summe(F)\*Summe(a)+AlleZeichenDerZeile+Summe(Zahlen)-Summe(Vars)\*Summe(Leerzeichen)+AnzahlDerZeichenDerLetztenZeile
Am Ende jeder Zeile muss die Prüfsumme stehen. Nach der Anweisung befindet sich ein Leerzeichen, welches nicht mit mitgerechnet wird und vor der Prüfsumme befindet sich ein Leerzeichen, welches ebenfalls nicht beachtet wird.

Kommentare
----------

Einzeilige Kommentare werden mit /// eingeleitet und reichen bis zum Ende der Zeile, sie können nicht in der Zeile terminiert werden
Mehrzeilige Kommentare gibt es nicht.

check
-----

--Z hat keine if-Funktion sämtliche Überprüfungen werden mit dem ASCII Char. 020 (DLE) durchgeführt. Dabei muss die Prüfbedingung wie folgt übergeben werden:
`\016 var1 var2 var3`
 * var1 u. var2: Diese Variablen werden verglichen.
 * var3: Diese Variable wird auf true gezt wenn var1 und var2 gleich sind.

Arithmetik
----------

--Z kann natürlich auch rechnen. Eine arithmetische Anweisung wird mit ASCII Char. 021 (DC1) eingeleitet nach einem Leerzeichen wird als einzeln Zeichen die Operation (+-*/) übergeben. Das Ergebnis wird in eine Variable gespeichert.

Beispiel:

`
\021 + 23 42 foo /// foo=65
\021 / 23 5 bar /// bar=4.6
\021 - 5 10 baz /// baz=-5
`

Goto
----

--Z ist eine absolut funktions- und schleifenfreie Sprache. Sämtliche Wiederholungen werden mittels eines gotos erledigt. In der goto-Anweisung müssen zwei Parameter stehen 1. dem Punkt, wohin gesprungen werden soll, und 2. eine Variable, wenn diese Wahr, also true, ist, wird das goto ausgeführt, andernfalls läuft das Programm weiter nach oben. Der Sprungpunkt (1) ist ein String, welcher bereits geparst sein muss, d.h. er muss vor dem goto ausgeführt worden sein. Die Anweisung für ein goto ist: \014 (FF)

Beispiel:

`
\014 "\025 bar 2 bar" baz
\016 foo false baz
\016 10 bar foo  /// wenn bar=10 dann ist foo=true
\021 + 2 bar bar  /// addiere zu bar 2 hinzu
\012 1 true
\025 bar 2  /// bar =2
`


set
---
Natürlich ist es in --Z, als beliebteste Sprache, möglich Variablen zu setzen. Dies geschieht mit _set_ oder besser gesagt dem Ascii char 025 (NAK). 

Beispiel:

`
\025 'bar' foo /// variable foo übernimmt den Wert 'bar'
\025 42 bar    /// variable bar übernimmt den Wert 42
\025 13.36 baz /// variable baz übernimmt den Wert 13,37
`
jump
----

Weil --Z so eine tolle Sprache ist, absolut frei von Funktionen, arrays, oder gar so einem Hexenwerk wie Zeilen Nummern, gibt es jump. Jump kann eine oder mehrere Zeilen im Programm Übersprigen. Dies kann z.B. nützlich sein um bestimmte Subroutinen zu überspringen, weil sie erst später benötigt werden. Jump wird mit dem Ascii Char. \013 (VT) aufgerufen, der Anweisung wird eine Variable übergeben und die Anzahl der Zeilen.

Beispiel:

`
/// foo=true
\012 5 foo /// Springt fünf Zeilen nach Oben
/// bar=false
\012 4 bar /// läuft einfach durch
`
Ausgabe
-------

Mit --Z ist es natürlich auch möglich Ausgaben zu erzeugen. Hierfür wird das ASCII Char. 002 (STX) benuzt. Das stdout von --Z ist eine Datei. Der Anweisung werden zwei Parameter übergeben, die eigentliche Ausgabe und die Datei, in welche geschrieben wird. Nach diesem Befehl wird in der Ausgabedatei ein Zeilenvorschub geschrieben, möchte man also den Inhalt mehrerer Variablen in der selben Zeile haben, kann man dies durch ein "." (Punkt) erzielen.

Beispiel:
`
\002 "Dies ist ein Beispiel" out.txt
/// foo="bar"
\002 bar baz.txt
\002 bar." <- die bar Datei!" baz.txt
`

Eingabe
-------

Selbstverständlich ist es auch möglich eingaben zu tätigen, --Z erstellt dafür eine Datei in welche geschrieben werden kann. Der Inhalt dieser Datei wird dann in eine Variable geparst. Anschließend wird diese Datei gelöscht. Die entsprechende Anweisung ist \003 (ETC).
Beispiel:

`
\003 datei.foo foo  \\\ Inhalt von der Datei "datei.foo" wird in die Variable foo 'verschoben'
`