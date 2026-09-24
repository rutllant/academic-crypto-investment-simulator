# Manual d'usuari · Academic Crypto Investment Simulator

Aquest manual està pensat per a persones que **no tenen coneixements previs d'inversió**. L'objectiu és entendre què fa cada opció del simulador, què signifiquen els resultats i com interpretar-los sense confondre una simulació amb una predicció.

> **Important:** el simulador té una finalitat educativa i de recerca. No opera amb diners reals, no necessita claus API i no constitueix assessorament financer. Un resultat favorable en el passat no garanteix que una estratègia funcioni en el futur.

---

## 1. Què fa exactament el simulador?

El programa compara quatre maneres diferents de prendre decisions sobre criptomonedes:

1. **Agent tècnic:** segueix unes regles mecàniques basades en indicadors com EMA, RSI i MACD.
2. **Holders:** compren una criptomoneda al principi i no fan res més fins al final.
3. **Agents aleatoris:** prenen decisions a l'atzar. Serveixen com a grup de control.
4. **Inversors humans:** permet introduir decisions de persones reals mitjançant un fitxer CSV.

Tots parteixen del mateix capital inicial i del mateix període d'estudi. Això permet comparar els resultats en condicions similars.

El programa fa un **backtest**, és a dir, aplica aquestes decisions a dades històriques reals de mercat per veure què hauria passat.

---

## 2. Abans de començar: quatre idees bàsiques

### Criptomoneda

És un actiu digital, com Bitcoin (BTC), Ether (ETH) o Solana (SOL). El seu preu varia contínuament segons l'oferta i la demanda.

### Mercat spot

El simulador utilitza mercats **spot**. Això significa que treballa amb compra i venda directa de l'actiu, sense palanquejament, futurs ni productes derivats.

### Cartera

La cartera és el conjunt de diners i criptomonedes que té l'agent en cada moment.

Per exemple, una cartera de 10.000 € podria tenir:

- 3.000 € en BTC,
- 2.000 € en ETH,
- 5.000 € en efectiu.

### Efectiu o CASH

És la part del capital que no està invertida en cap criptomoneda. En el simulador no genera interessos.

---

# 3. Apartat «Mercat i cartera»

## Exchange

Un **exchange** és una plataforma on es compren i venen criptomonedes.

El simulador pot obtenir dades públiques de:

- Kraken
- Binance
- Coinbase
- Bitstamp

No s'hi obre cap compte i no es fan operacions reals. L'exchange només actua com a **font de dades històriques**.

És normal que el mateix actiu tingui petites diferències de preu entre exchanges.

---

## Divisa de referència

És la moneda amb què s'expressen els preus.

El simulador permet:

- EUR
- USD
- USDT
- USDC

Per exemple:

**BTC/EUR** significa que el preu de Bitcoin s'expressa en euros.

**ETH/USD** significa que el preu d'Ether s'expressa en dòlars.

Per comparar correctament diversos actius, totes les criptomonedes seleccionades utilitzen la mateixa divisa de referència.

---

## Criptomonedes

Aquí es trien els actius que formaran l'univers de l'experiment.

Per exemple:

- BTC/EUR
- ETH/EUR
- SOL/EUR

L'agent tècnic només pot invertir en les criptomonedes seleccionades.

Seleccionar moltes criptomonedes no significa necessàriament fer una simulació millor. Com més actius hi ha, més dades s'han de descarregar i és més probable que alguna moneda tingui poc historial.

---

## Seleccionar totes les criptomonedes disponibles

Permet incloure tots els mercats spot disponibles en aquell exchange i divisa.

És una opció útil per experimentar, però pot fer que:

- la descàrrega sigui més lenta;
- el càlcul de milers d'agents aleatoris trigui més;
- el període efectiu d'anàlisi es redueixi si alguna criptomoneda és molt recent.

Per a una primera prova és preferible treballar amb poques criptomonedes.

---

## Capital inicial

És la quantitat virtual de diners amb què comença cada estratègia.

Per exemple:

**10.000 €**

Aquests diners no són reals. El simulador calcula què hauria passat amb aquesta quantitat durant el període seleccionat.

Per fer comparacions, tots els grups han de començar amb el mateix capital.

---

## Comissió per operació

En els mercats reals, comprar o vendre acostuma a tenir un cost.

Si indiquem:

**0,10 %**

una operació de 1.000 € té aproximadament un cost d'1 €.

Incloure comissions és important perquè una estratègia que compra i ven molt sovint pot semblar molt rendible si s'ignoren aquests costos.

---

## Data inicial i data final

Defineixen el període que volem estudiar.

Exemple:

**1 de gener de 2024 — 31 de desembre de 2025**

El simulador descarrega dades històriques i comprova què hauria passat durant aquest interval.

Això no és una predicció del futur: és una reconstrucció del passat.

---

# 4. L'agent tècnic

L'agent tècnic no «pensa» ni intenta endevinar el mercat.

Segueix unes regles matemàtiques. Cada regla pot donar punts a una criptomoneda. Quan una moneda arriba a la puntuació mínima establerta, pot entrar a la cartera.

Això converteix l'estratègia en una estratègia **sistemàtica**: davant les mateixes dades i els mateixos paràmetres, prendrà la mateixa decisió.

---

# 5. EMA: detectar tendència

EMA significa **Exponential Moving Average**, o mitjana mòbil exponencial.

És una mitjana del preu que dona més importància als preus recents.

El simulador compara dues EMA:

- una **EMA curta**, que reacciona ràpidament als canvis;
- una **EMA llarga**, que representa una tendència de més llarg termini.

### Exemple

EMA curta = 20 dies  
EMA llarga = 50 dies

Si:

**EMA20 > EMA50**

el simulador interpreta que el preu recent està per damunt de la seva tendència de llarg termini i suma els punts assignats a aquesta regla.

No significa que el preu hagi de continuar pujant. Només indica una condició de tendència definida prèviament.

### Punts EMA

Determinen el pes d'aquesta regla dins del sistema.

Per exemple:

EMA = 2 punts  
RSI = 1 punt  
MACD = 2 punts

En aquest cas, EMA i MACD tenen més influència en la decisió final que RSI.

---

# 6. RSI: mesurar el momentum

RSI significa **Relative Strength Index**.

És un indicador que oscil·la entre **0 i 100** i intenta mesurar la intensitat recent dels moviments del preu.

De manera orientativa, sovint es parla de:

- valors baixos: mercat amb pressió venedora;
- valors alts: mercat amb forta pressió compradora.

Però el simulador no interpreta automàticament «baix = comprar» o «alt = vendre». Utilitza l'interval que nosaltres definim.

### Exemple

RSI període = 14  
RSI mínim = 50  
RSI màxim = 70

La regla sumarà punts quan:

**50 ≤ RSI(14) ≤ 70**

Això busca una situació amb momentum positiu, però evita exigir un RSI extremadament alt.

### RSI període

És el nombre de sessions utilitzades per calcular l'indicador.

Un període més curt reacciona més ràpidament; un període més llarg és més estable.

---

# 7. MACD: tendència i momentum

MACD significa **Moving Average Convergence Divergence**.

Utilitza dues mitjanes exponencials i una línia de senyal.

Els paràmetres habituals tenen aquesta forma:

**MACD (12, 26, 9)**

on:

- 12 és el període ràpid;
- 26 és el període lent;
- 9 és el període de la línia de senyal.

En el simulador, la regla suma punts quan la línia MACD està per damunt de la seva línia de senyal.

Això s'interpreta com una situació de momentum favorable segons aquesta regla concreta.

Igual que amb EMA i RSI, és només un indicador matemàtic. No garanteix que el preu pugi.

---

# 8. Puntuació mínima per invertir

Les tres regles poden sumar punts.

Exemple:

| Regla | Punts |
|---|---:|
| EMA favorable | 2 |
| RSI dins l'interval | 1 |
| MACD favorable | 2 |
| **Màxim possible** | **5** |

Si establim:

**Puntuació mínima = 4**

una criptomoneda només podrà entrar a la cartera quan obtingui almenys 4 punts.

Una puntuació mínima baixa fa que l'agent sigui més permissiu.

Una puntuació mínima alta fa que exigeixi més coincidència entre els indicadors.

---

# 9. Pes màxim per criptomoneda

Indica quin percentatge màxim de la cartera pot ocupar un sol actiu.

Per exemple:

**Pes màxim = 40 %**

Amb 10.000 € de capital, cap criptomoneda podria ocupar inicialment més de 4.000 € de la cartera en un reequilibri.

Aquesta regla evita que tot el capital es concentri en una sola moneda.

Si no hi ha prou criptomonedes que compleixin les regles, una part dels diners queda en **CASH**.

---

# 10. Què és un reequilibri?

Un **reequilibri** és un moment en què l'agent modifica la distribució de la cartera.

Per exemple, podria passar de:

- BTC: 40 %
- ETH: 40 %
- CASH: 20 %

a:

- BTC: 0 %
- ETH: 40 %
- SOL: 40 %
- CASH: 20 %

Aquest canvi implica compres i vendes i, per tant, pot generar comissions.

El nombre de reequilibris permet saber si l'estratègia ha estat molt activa o molt estable.

---

# 11. Holders de control

Un **holder** segueix una estratègia molt simple:

1. compra una criptomoneda al principi;
2. la manté durant tot el període;
3. no pren cap altra decisió.

Aquesta estratègia també es coneix com **buy and hold** o, en l'argot de les criptomonedes, **HODL**.

### Per què serveixen els holders?

Permeten respondre una pregunta important:

> Ha valgut la pena utilitzar totes les regles de l'agent o hauria estat millor simplement comprar una moneda i esperar?

Si l'agent tècnic obté un 15 % però un holder de BTC obté un 40 %, el resultat de l'agent és positiu, però no ha superat aquella alternativa passiva.

---

# 12. Agents aleatoris

Els agents aleatoris formen el principal grup de control de l'experiment.

No utilitzen EMA, RSI ni MACD. Decideixen aleatòriament quines criptomonedes mantenir.

Podem simular:

- 100
- 500
- 1.000
- 5.000
- 10.000 agents

Com més agents utilitzem, millor podem observar la distribució de resultats produïts per l'atzar, encara que el càlcul tarda més.

---

## Decisió dels agents aleatoris

Indica cada quant temps poden modificar la cartera:

- cada dia;
- cada 7 dies;
- cada 14 dies;
- cada 30 dies.

Entre dues dates de decisió, mantenen les posicions.

Això evita comparar l'agent tècnic amb agents que estiguin canviant obligatòriament de cartera cada dia.

---

# 13. Executar simulació

Quan premem **Executar simulació**, el programa:

1. descarrega les dades històriques públiques;
2. calcula EMA, RSI i MACD;
3. executa l'agent tècnic;
4. simula els agents aleatoris;
5. calcula els holders;
6. mostra els resultats.

La simulació pot trigar més si hi ha moltes criptomonedes o milers d'agents aleatoris.

---

# 14. Com interpretar els resultats

## Capital final

És el valor final de la cartera.

Si comencem amb 10.000 € i acabem amb 11.500 €:

**Capital final = 11.500 €**

---

## Rendibilitat

És el canvi percentual del capital.

En l'exemple anterior:

**+15 %**

Si el capital final fos 8.500 €:

**−15 %**

La rendibilitat per si sola no explica tot el risc assumit.

---

# 15. Drawdown màxim

El **drawdown** mesura la caiguda des d'un màxim anterior de la cartera.

Exemple:

La cartera arriba a:

**12.000 €**

i després cau fins a:

**9.000 €**

El descens és:

**−25 %**

Encara que després es recuperi, el drawdown màxim registra aquella caiguda.

És una mesura important perquè dues estratègies poden acabar amb la mateixa rendibilitat però haver tingut riscos molt diferents.

En general:

- drawdown més proper a 0 % = caigudes més petites;
- drawdown molt negatiu = caigudes fortes.

---

# 16. Índex Sharpe

L'**índex Sharpe** relaciona rendibilitat i volatilitat.

Simplificant molt:

> intenta indicar quanta rendibilitat s'ha obtingut en relació amb les oscil·lacions assumides.

Un Sharpe més alt indica una millor relació entre rendiment i variabilitat dins del model utilitzat.

No s'ha d'interpretar com una nota universal ni com una garantia de qualitat.

Especialment en criptomonedes, les distribucions de rendiments poden ser molt irregulars i una sola mètrica no resumeix tot el risc.

---

# 17. Percentil respecte als agents aleatoris

El simulador compara el capital final de l'agent tècnic amb tots els agents aleatoris.

Si diu:

**percentil 90**

vol dir aproximadament que l'agent tècnic ha obtingut un resultat superior al 90 % de les simulacions aleatòries d'aquell experiment.

No significa que tingui un 90 % de probabilitats de guanyar en el futur.

Només descriu la posició de l'agent dins de **les simulacions realitzades en aquell període i amb aquella configuració**.

---

# 18. Histograma dels agents aleatoris

L'histograma mostra com s'han distribuït les rendibilitats dels agents aleatoris.

Cada barra representa quants agents han acabat dins d'un determinat interval de rendibilitat.

La línia de l'**agent tècnic** permet veure visualment si el seu resultat se situa:

- al centre de la distribució;
- en una zona baixa;
- o en una zona alta.

És una de les gràfiques més importants per comparar l'estratègia tècnica amb l'atzar.

---

# 19. Agent tècnic vs holders

Aquesta gràfica mostra l'evolució de la rendibilitat acumulada de:

- l'agent tècnic;
- cadascun dels holders seleccionats.

Permet veure no només qui acaba millor, sinó també **com ha arribat fins allí**.

Dues estratègies poden acabar amb resultats semblants però haver tingut trajectòries molt diferents.

---

# 20. Operacions i senyals

## Reequilibris

Mostra les dates en què l'agent ha modificat la cartera.

És útil per saber:

- quan ha entrat o sortit d'actius;
- amb quina freqüència ha canviat la cartera;
- quines operacions han generat comissions.

## Senyals diaris

Mostra els valors dels indicadors i les puntuacions calculades per a les criptomonedes.

Aquesta taula permet entendre **per què** una moneda era o no elegible en una determinada data.

## Exportació

Permet descarregar els resultats en CSV per analitzar-los amb Excel, LibreOffice, Python, R o altres eines.

---

# 21. Inversors humans

El simulador permet comparar l'agent amb decisions preses per persones.

Primer es descarrega una plantilla CSV.

Les columnes són:

| Columna | Significat |
|---|---|
| `participant` | Nom o codi de la persona |
| `date` | Data de la decisió |
| `choice` | Criptomoneda escollida o CASH |

Exemple:

```csv
participant,date,choice
Persona 1,2025-01-10,BTC
Persona 1,2025-02-15,ETH
Persona 1,2025-03-20,CASH
```

Això significa que la Persona 1:

- escull BTC el 10 de gener;
- canvia a ETH el 15 de febrer;
- passa a efectiu el 20 de març.

Quan selecciona una criptomoneda, el simulador hi destina com a màxim el percentatge definit a **Pes màxim per criptomoneda**. La resta queda en CASH.

---

# 22. Què significa CASH en els inversors humans?

**CASH** significa no mantenir cap criptomoneda en aquell moment.

És útil si el participant considera que no vol estar exposat al mercat.

No és necessari introduir una decisió cada dia. L'última decisió es manté fins que el participant en registra una de nova.

---

# 23. Una configuració senzilla per aprendre

Per entendre el simulador abans de fer l'experiment formal es pot començar, només com a exemple didàctic, amb:

| Paràmetre | Exemple |
|---|---|
| Exchange | Kraken |
| Divisa | EUR |
| Criptomonedes | BTC, ETH, SOL |
| Capital | 10.000 € |
| Comissió | 0,10 % |
| Període | 2 anys |
| EMA | activada |
| RSI | activat |
| MACD | activat |
| Holders | BTC, ETH i SOL |
| Agents aleatoris | 1.000 |
| Decisió aleatòria | cada 7 dies |

Aquesta configuració **no és una recomanació d'inversió**. Només és una manera senzilla de familiaritzar-se amb el funcionament del programa.

Per al TDR, els paràmetres definitius s'han de justificar metodològicament i congelar abans del test principal.

---

# 24. Errors habituals d'interpretació

### «L'agent ha guanyat diners, per tant funciona»

No necessàriament. Cal comparar-lo amb holders, agents aleatoris, risc assumit i altres períodes.

### «Ha superat els agents aleatoris, per tant sempre els superarà»

No. El resultat només correspon al període, actius i paràmetres utilitzats.

### «El millor resultat és l'estratègia més segura»

No. Una rendibilitat alta pot haver implicat caigudes molt grans.

### «Si ajusto els paràmetres fins que el gràfic queda molt bé, he trobat una bona estratègia»

Això pot ser **sobreajustament** o *overfitting*: adaptar les regles massa bé al passat.

Per això, en un experiment acadèmic, és important definir les regles abans d'observar el període de test.

---

# 25. Paraules clau del simulador

| Terme | Explicació breu |
|---|---|
| **Backtest** | Provar una estratègia amb dades del passat |
| **Exchange** | Plataforma de negociació que proporciona les dades |
| **Spot** | Compra o venda directa de l'actiu |
| **Cartera** | Conjunt d'actius i efectiu |
| **EMA** | Mitjana exponencial utilitzada per observar tendències |
| **RSI** | Indicador de momentum entre 0 i 100 |
| **MACD** | Indicador que combina tendència i momentum |
| **HODL / Holder** | Comprar i mantenir sense canvis |
| **Monte Carlo** | Repetir moltes simulacions amb decisions aleatòries |
| **Rendibilitat** | Variació percentual del capital |
| **Drawdown** | Caiguda des d'un màxim anterior |
| **Sharpe** | Relació entre rendiment i volatilitat |
| **Reequilibri** | Canvi en la composició de la cartera |
| **CASH** | Capital no invertit |
| **Percentil** | Posició relativa dins d'un conjunt de resultats |
| **Overfitting** | Ajustar massa una estratègia als resultats passats |

---

# 26. Per què aquest simulador no és un sistema de predicció?

Els indicadors tècnics es calculen a partir de preus passats.

El simulador pot respondre preguntes com:

> Què hauria passat si haguéssim aplicat aquestes regles durant aquest període?

Però no pot respondre amb certesa:

> Què passarà amb Bitcoin la setmana vinent?

L'objectiu principal del projecte és **comparar sistemes de decisió**, no predir preus.

---

# 27. Recomanació per a l'ús acadèmic

Perquè els resultats siguin comparables i reproduïbles:

1. definir les criptomonedes;
2. definir el període;
3. fixar la comissió;
4. fixar EMA, RSI i MACD;
5. fixar la puntuació mínima;
6. fixar el pes màxim;
7. definir holders i agents aleatoris;
8. guardar aquesta configuració;
9. executar el test;
10. no modificar les regles després d'haver vist el resultat principal.

Si es canvien les regles després d'observar els resultats, s'ha de considerar una nova estratègia i provar-la en un altre període.

---

## Documentació relacionada

- `README.md` — instal·lació i característiques del projecte.
- `docs/PROTOCOL_TDR.md` — proposta de protocol experimental.
- `SECURITY.md` — informació sobre la distribució i verificació dels fitxers.

---

**Versió del manual:** compatible amb Academic Crypto Investment Simulator v0.4.2.
