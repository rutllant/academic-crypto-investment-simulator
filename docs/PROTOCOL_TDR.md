# Protocol experimental suggerit · Agent Cripto TDR v0.4.3

## Pregunta de recerca
Una estratègia sistemàtica basada en indicadors tècnics produeix resultats diferents dels d'una estratègia aleatòria sota les mateixes condicions de capital, univers d'actius i costos?

## Hipòtesis
- **H0:** l'agent tècnic no obté un resultat diferenciat de la distribució dels agents aleatoris.
- **H1:** l'agent tècnic se situa sistemàticament en una zona superior de la distribució aleatòria, considerant també el risc.

## Regla temporal d'execució

Per evitar *look-ahead bias*, el simulador aplica aquesta seqüència:

1. es tanca la sessió del dia **t**;
2. es calculen EMA, RSI, MACD i la puntuació amb aquesta informació ja completa;
3. el senyal només pot executar-se a l'**obertura de la sessió següent**;
4. la cartera es valora al tancament de cada sessió.

Per tant, el model no atribueix a l'agent una pujada o baixada produïda entre el tancament que genera el senyal i l'obertura següent.

Les decisions dels participants humans segueixen un criteri equivalent: una decisió registrada a la data **t** s'executa a la primera sessió posterior.

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
- Data del senyal i data d'execució de cada reequilibri.
- Percentil de l'agent dins la distribució aleatòria.
- Rendibilitat de cadascun dels holders.

## Validació del programari

La v0.4.3 incorpora tests automàtics per verificar indicadors, comptabilitat, comissions, drawdown, integritat OHLCV, absència d'execució a la mateixa barra i reproductibilitat dels agents aleatoris. L'abast complet està documentat a `VALIDATION.md`.

Aquesta validació comprova la coherència del programari, però no demostra que l'estratègia tingui capacitat predictiva.

## Precaucions
- No interpretar un únic període favorable com una prova general de superioritat de l'anàlisi tècnica.
- No canviar les regles després de veure el resultat del període de test sense obrir un nou test fora de mostra.
- Si es seleccionen moltes monedes, deixar constància que el període efectiu pot quedar condicionat per la moneda amb menys història disponible.
