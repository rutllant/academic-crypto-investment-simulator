# Manual d'usuari · Academic FX Investment Simulator

Aquest manual està pensat per a persones que **no tenen coneixements previs d'inversió ni de mercat de divises**. Explica què fa cada opció del simulador, què significa cada resultat i quines conclusions es poden —i no es poden— extreure d'un backtest.

> **Important:** el simulador és educatiu i de recerca. No opera amb diners reals, no utilitza palanquejament i no constitueix assessorament financer. Els tipus del BCE són tipus de referència informatius, no preus reals d'execució.

---

## 1. Què fa el simulador?

El programa compara quatre maneres de gestionar una cartera de divises:

1. **Agent tècnic:** pren decisions mecàniques a partir d'EMA, RSI i MACD.
2. **Holders:** converteixen el capital inicial a una sola divisa i la mantenen.
3. **Agents aleatoris:** decideixen a l'atzar; serveixen com a grup de control.
4. **Inversors humans:** permeten introduir decisions de persones reals mitjançant CSV.

Tots parteixen del mateix capital inicial i del mateix període. El programa reconstrueix què hauria passat aplicant aquestes decisions als **tipus de canvi històrics de referència del BCE**.

Això és un **backtest**: una simulació sobre el passat, no una predicció del futur.

---

## 2. Conceptes bàsics

### Què és una divisa?

Una divisa és una moneda utilitzada internacionalment, com:

- EUR — euro
- USD — dòlar dels Estats Units
- GBP — lliura esterlina
- JPY — ien japonès
- CHF — franc suís

### Què és un tipus de canvi?

Indica quant val una moneda expressada en una altra.

Per exemple:

**USD/EUR = 0,87**

significa que, dins del simulador, una unitat de USD val aproximadament 0,87 EUR.

### Què és la divisa de referència?

És la moneda amb què mesurem tota la cartera.

Si escollim **EUR**, el capital inicial, el capital final i el valor de totes les posicions s'expressen en euros.

Si escollim **USD**, tot es valora en dòlars.

### Què és CASH?

CASH és la part de la cartera que no està convertida a cap de les divises seleccionades. En aquest simulador equival a mantenir el capital en la **divisa de referència**.

Si la referència és EUR, CASH significa euros.

---

## 3. D'on surten les dades?

El simulador utilitza la sèrie històrica de **tipus de canvi de referència del Banc Central Europeu (BCE)**.

El BCE publica, normalment cada dia laborable, quantes unitats d'una divisa equivalen a un euro.

Exemple hipotètic:

- 1 EUR = 1,15 USD
- 1 EUR = 0,86 GBP

El programa pot derivar un tipus creuat:

**1 GBP en USD = 1,15 / 0,86 ≈ 1,337 USD**

Això permet utilitzar USD, GBP, JPY, CHF i moltes altres divises com a moneda de referència sense necessitar una segona font de dades.

### Limitació important

Els tipus del BCE són **tipus de referència**. No incorporen exactament:

- spread d'un broker;
- slippage;
- preu intradia;
- comissions específiques;
- swap overnight;
- interessos sobre saldo.

Per això el programa és adequat per a un experiment acadèmic, però no és un simulador complet d'operativa Forex professional.

---

# 4. Apartat «Mercat i cartera»

## Divisa de referència

Escull la moneda en què es valorarà tota la cartera.

Per començar, **EUR** és la configuració més intuïtiva.

## Divises

Aquí selecciones les monedes en què l'agent podrà convertir una part del capital.

Per exemple:

- USD/EUR
- GBP/EUR
- JPY/EUR
- CHF/EUR

Si la referència és EUR, **USD/EUR** significa «valor d'un dòlar expressat en euros».

## Seleccionar totes les divises

Inclou totes les divises disponibles al catàleg del simulador.

Per a una primera prova és millor utilitzar només 3–6 divises: la simulació és més ràpida i els resultats són més fàcils d'interpretar.

## Capital inicial

És una quantitat virtual.

Exemple:

**10.000 EUR**

Tots els grups de comparació parteixen del mateix capital.

## Cost de conversió

Representa de forma simplificada el cost de passar d'una moneda a una altra.

Exemple:

**0,10 %**

Si el model mou 1.000 EUR de valor, el cost aproximat és 1 EUR.

No és un spread real de broker: és una hipòtesi experimental que permet penalitzar estratègies que canvien massa sovint.

## Data inicial i final

Defineixen el període del backtest.

El simulador necessita unes observacions prèvies addicionals per calcular EMA, RSI i MACD abans que comenci la data d'avaluació.

---

# 5. Què és l'agent tècnic?

L'agent no «pensa» ni intenta entendre notícies econòmiques.

Segueix unes regles matemàtiques.

Cada divisa rep punts segons els indicadors. Si supera la puntuació mínima, pot entrar a la cartera.

Això és una estratègia **sistemàtica**: amb les mateixes dades i paràmetres, sempre pren les mateixes decisions.

---

# 6. EMA: detectar tendència

EMA significa **Exponential Moving Average** o mitjana mòbil exponencial.

El simulador compara:

- una EMA curta;
- una EMA llarga.

Exemple:

- EMA curta = 20 sessions
- EMA llarga = 50 sessions

Si:

**EMA20 > EMA50**

la regla interpreta que la tendència recent de la divisa és superior a la tendència de més llarg termini i suma els punts configurats.

No significa que la divisa hagi de continuar pujant.

---

# 7. RSI: mesurar momentum

RSI significa **Relative Strength Index**.

Oscil·la entre 0 i 100 i resumeix la intensitat recent dels moviments.

Exemple:

- període RSI = 14
- mínim = 50
- màxim = 70

La regla suma punts quan:

**50 ≤ RSI(14) ≤ 70**

El simulador no pressuposa que «RSI baix = comprar» o «RSI alt = vendre». Només aplica l'interval que s'ha definit.

---

# 8. MACD: tendència i momentum

MACD significa **Moving Average Convergence Divergence**.

Una configuració típica és:

**MACD (12, 26, 9)**

El simulador suma punts quan la línia MACD està per damunt de la línia de senyal.

Com qualsevol indicador tècnic, descriu el comportament passat dels preus; no garanteix el moviment futur.

---

# 9. Puntuació mínima

Les regles poden sumar punts.

Exemple:

| Regla | Punts |
|---|---:|
| EMA favorable | 2 |
| RSI favorable | 1 |
| MACD favorable | 2 |
| **Màxim** | **5** |

Amb una puntuació mínima de **4**, una divisa necessita almenys quatre punts per ser elegible.

Com més alta és la puntuació mínima, més exigent és l'agent.

---

# 10. Pes màxim per divisa

Limita la concentració de la cartera.

Si tenim 10.000 EUR i el pes màxim és del **40 %**, cap divisa podrà rebre inicialment més de 4.000 EUR de valor en un reequilibri.

La part no assignada queda en CASH, és a dir, en la divisa de referència.

---

# 11. Reequilibri

Un reequilibri és un canvi en la composició de la cartera.

Exemple:

Abans:

- USD: 40 %
- GBP: 40 %
- CASH: 20 %

Després:

- USD: 0 %
- JPY: 40 %
- CHF: 40 %
- CASH: 20 %

Aquests moviments generen el cost de conversió configurat.

---

# 12. Holders

Un holder segueix una estratègia passiva:

1. converteix el capital a una divisa al principi;
2. la manté fins al final;
3. no canvia la decisió.

Serveix per respondre:

> Ha aportat valor l'estratègia tècnica o hauria estat millor mantenir simplement una divisa?

Un agent que obté +5 % no necessàriament és millor si un holder de la mateixa prova obté +12 %.

---

# 13. Agents aleatoris

Els agents aleatoris no utilitzen indicadors.

En cada data de decisió:

- trien aleatòriament quantes divises mantenir;
- trien quines;
- reparteixen el pes respectant el mateix màxim que l'agent tècnic;
- poden quedar totalment o parcialment en CASH.

Se'n poden simular de 100 a 10.000.

Aquesta distribució permet comparar el resultat de l'agent amb allò que pot aparèixer simplement per atzar.

---

# 14. Freqüència de decisió aleatòria

Les opcions són:

- cada 1 sessió;
- cada 5 sessions;
- cada 10 sessions;
- cada 20 sessions.

En dades de dies laborables:

- 5 sessions s'aproxima a una setmana;
- 20 sessions s'aproxima a un mes.

Entre dates de decisió, els agents mantenen les posicions.

---

# 15. Executar simulació

Quan premem **Executar simulació**, el programa:

1. descarrega l'històric del BCE;
2. deriva els tipus creuats necessaris;
3. calcula EMA, RSI i MACD;
4. executa l'agent tècnic;
5. simula els agents aleatoris;
6. calcula els holders;
7. mostra els resultats.

---

# 16. Capital final i rendibilitat

Si comencem amb 10.000 EUR i acabem amb 10.800 EUR:

- capital final = 10.800 EUR
- rendibilitat = +8 %

Si acabem amb 9.200 EUR:

- rendibilitat = −8 %

La rendibilitat no explica per si sola el risc.

---

# 17. Drawdown màxim

El drawdown mesura la caiguda des d'un màxim anterior.

Exemple:

- la cartera arriba a 11.000;
- després baixa a 9.900.

La caiguda és aproximadament del **−10 %**.

Un drawdown gran indica que l'estratègia ha patit una pèrdua temporal important encara que després s'hagi recuperat.

---

# 18. Volatilitat

La volatilitat mesura quant oscil·len els rendiments.

Una volatilitat més alta implica moviments més intensos i, en general, més incertesa sobre el valor de la cartera.

En aquesta versió, la volatilitat diària s'anualitza utilitzant **252 sessions**, una convenció habitual per a dies de mercat.

---

# 19. Índex Sharpe

El Sharpe relaciona rendibilitat i volatilitat.

De manera simplificada:

> quanta rendibilitat s'ha obtingut en relació amb la variabilitat experimentada?

Un Sharpe més alt descriu una millor relació rendiment/volatilitat dins d'aquest model.

No és una nota universal ni una garantia que una estratègia sigui bona.

---

# 20. Percentil respecte dels agents aleatoris

Si l'agent queda al **percentil 90**, significa que en aquell experiment ha acabat per sobre d'aproximadament el 90 % dels agents aleatoris.

No significa:

- 90 % de probabilitat de guanyar;
- 90 % de probabilitat de funcionar en el futur;
- que l'estratègia sigui «segura».

Només descriu la seva posició dins de les simulacions executades.

---

# 21. Histograma

L'histograma mostra la distribució de rendibilitats dels agents aleatoris.

La línia de l'agent tècnic permet veure si queda:

- prop del centre;
- a la zona baixa;
- o a la zona alta de la distribució.

---

# 22. Agent tècnic vs holders

La gràfica mostra l'evolució acumulada de:

- l'agent tècnic;
- cada holder seleccionat.

És útil perquè dues estratègies poden arribar al mateix resultat final amb trajectòries i drawdowns diferents.

---

# 23. Operacions i senyals

## Reequilibris

Mostra quan l'agent modifica la cartera, els pesos assignats, les puntuacions i el cost de conversió.

## Senyals diaris

Mostra les puntuacions i tipus de canvi utilitzats en cada sessió.

## Exportació

Permet baixar CSV per continuar l'anàlisi amb Excel, LibreOffice, Python o R.

---

# 24. Inversors humans

El CSV utilitza:

| Columna | Significat |
|---|---|
| `participant` | Nom o codi |
| `date` | Data de la decisió |
| `choice` | Divisa o CASH |

Exemple:

```csv
participant,date,choice
Persona 1,2026-01-02,USD
Persona 1,2026-02-02,GBP
Persona 1,2026-03-02,CASH
```

L'última decisió es manté fins que se'n registra una de nova.

Quan es tria una divisa, s'hi assigna com a màxim el percentatge definit al **Pes màxim per divisa**.

---

# 25. Configuració senzilla per aprendre

Exemple didàctic:

| Paràmetre | Exemple |
|---|---|
| Divisa de referència | EUR |
| Divises | USD, GBP, JPY, CHF |
| Capital | 10.000 EUR |
| Cost de conversió | 0,10 % |
| Període | 2 anys |
| EMA | activada |
| RSI | activat |
| MACD | activat |
| Holders | USD, GBP, JPY |
| Agents aleatoris | 1.000 |
| Decisió aleatòria | cada 5 sessions |

Això **no és una recomanació d'inversió**. Només és una configuració pedagògica per entendre l'aplicació.

---

# 26. Errors habituals d'interpretació

### «Ha guanyat diners, per tant funciona»

No necessàriament. Cal comparar amb els controls i amb el risc.

### «Ha superat l'atzar, per tant continuarà fent-ho»

No. El resultat pertany a aquell període i configuració.

### «La millor rendibilitat és la millor estratègia»

No necessàriament. Pot haver tingut un drawdown o una volatilitat molt superior.

### «Puc ajustar les regles fins que el resultat sigui bo»

Fer-ho després de veure les dades pot generar **sobreajustament (overfitting)**.

---

# 27. Què NO simula aquesta versió?

La v0.1.0 no és una plataforma de Forex professional.

No incorpora:

- palanquejament;
- short selling;
- marge;
- stop-loss;
- take-profit;
- spreads variables;
- slippage;
- swaps;
- interessos;
- ordres intradia.

Aquesta simplicitat és intencionada: facilita un experiment comparable i comprensible.

---

# 28. Glossari

| Terme | Explicació |
|---|---|
| **Backtest** | Prova amb dades històriques |
| **Divisa de referència** | Moneda en què es valora la cartera |
| **Tipus creuat** | Tipus calculat a partir de dues relacions amb una tercera moneda |
| **CASH** | Capital mantingut en la divisa de referència |
| **EMA** | Mitjana exponencial per observar tendència |
| **RSI** | Indicador de momentum entre 0 i 100 |
| **MACD** | Indicador de tendència i momentum |
| **Holder** | Estratègia de comprar/conservar |
| **Monte Carlo** | Moltes simulacions amb decisions aleatòries |
| **Rendibilitat** | Variació percentual del capital |
| **Volatilitat** | Intensitat de les oscil·lacions |
| **Drawdown** | Caiguda des d'un màxim anterior |
| **Sharpe** | Relació entre rendibilitat i volatilitat |
| **Reequilibri** | Canvi de composició de cartera |
| **Percentil** | Posició relativa dins d'una distribució |
| **Overfitting** | Ajust excessiu de les regles al passat |

---

# 29. Per què no és un sistema de predicció?

EMA, RSI i MACD utilitzen dades passades.

El simulador pot respondre:

> Què hauria passat si haguéssim aplicat aquestes regles?

No pot respondre amb certesa:

> Quina divisa pujarà la setmana vinent?

L'objectiu és **comparar sistemes de decisió**, no predir el futur.

---

# 30. Recomanació per al TDR

Abans del test principal, documenta i congela:

1. versió del programa;
2. divisa de referència;
3. divises seleccionades;
4. dates;
5. capital;
6. cost de conversió;
7. EMA;
8. RSI;
9. MACD;
10. puntuació mínima;
11. pes màxim;
12. holders;
13. nombre d'agents aleatoris;
14. freqüència de decisió.

Si canvies les regles després de veure el resultat, tracta-les com una estratègia nova i prova-les en un altre període.

---

**Versió del manual:** Academic FX Investment Simulator v0.1.0.
