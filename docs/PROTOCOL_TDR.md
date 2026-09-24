# Protocol experimental suggerit · Agent Cripto TDR v0.4

## Pregunta de recerca
Una estratègia sistemàtica basada en indicadors tècnics produeix resultats diferents dels d'una estratègia aleatòria sota les mateixes condicions de capital, univers d'actius i costos?

## Hipòtesis
- **H0:** l'agent tècnic no obté un resultat diferenciat de la distribució dels agents aleatoris.
- **H1:** l'agent tècnic se situa sistemàticament en una zona superior de la distribució aleatòria, considerant també el risc.

## Controls
1. **Holders:** entre 1 i N, on N és el nombre de criptomonedes seleccionades. Cada holder compra una moneda a l'inici i no fa cap altra operació.
2. **Agents aleatoris:** 100–10.000 simulacions sobre el mateix univers d'actius i amb el mateix pes màxim per actiu.
3. **Participants humans:** persones sense coneixements específics previs; les seves decisions es registren amb data i actiu.

## Regles de l'agent
L'aplicació permet definir abans de l'experiment:
- períodes i puntuació de l'EMA;
- període, interval i puntuació del RSI;
- paràmetres i puntuació del MACD;
- puntuació mínima perquè una moneda sigui elegible;
- pes màxim per actiu.

Les regles s'han de documentar a la memòria del TDR. Per al test principal s'han de **congelar abans d'observar els resultats**.

## Variables a registrar
- Capital final i rendibilitat total.
- Drawdown màxim.
- Volatilitat anualitzada.
- Índex Sharpe.
- Nombre de reequilibris.
- Comissions acumulades.
- Percentil de l'agent dins la distribució aleatòria.
- Rendibilitat de cadascun dels holders.

## Precaucions
- No interpretar un únic període favorable com una prova general de superioritat de l'anàlisi tècnica.
- No canviar les regles després de veure el resultat del període de test sense obrir un nou test fora de mostra.
- Si es seleccionen moltes monedes, deixar constància que el període efectiu pot quedar condicionat per la moneda amb menys història disponible.
