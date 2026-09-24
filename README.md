# Academic Crypto Investment Simulator · v0.4.2

Aplicació educativa per comparar una estratègia tècnica de criptomonedes amb **holders**, agents aleatoris i inversors humans utilitzant dades públiques reals de mercat. **No executa operacions reals, no utilitza claus API i no ofereix assessorament financer.**

## Manuals per començar de zero

Si no tens experiència en inversions o anàlisi tècnica, tens disponibles dos manuals introductoris:

- **[Manual en català](docs/MANUAL_USUARI.md)**
- **[User manual in English](docs/USER_MANUAL_EN.md)**

Expliquen pas a pas què són l'exchange, la divisa de referència, la cartera, EMA, RSI, MACD, els holders, els agents aleatoris, el drawdown, l'índex Sharpe, els percentils, els reequilibris i la càrrega de decisions humanes, amb exemples senzills i advertiments d'interpretació. Els dos manuals també s'inclouen dins del ZIP portable i del Setup.exe de la v0.4.2.

## Windows: instal·lació sense Python ni PowerShell

Des de la v0.4.1 el sistema de distribució és autocontingut; la v0.4.2 incorpora també els manuals d'usuari dins del paquet. L'ordinador de l'usuari **ja no descarrega ni instal·la Python, no executa `pip` i no utilitza `setup.ps1` ni `ExecutionPolicy Bypass`**.

Cada Release de Windows es construeix automàticament a GitHub Actions i inclou:
- un runtime oficial de Python portable;
- Streamlit i totes les dependències necessàries;
- el codi de l'aplicació;
- un ZIP portable;
- un instal·lador `Setup.exe` creat amb Inno Setup;
- `SHA256SUMS.txt` per comprovar la integritat dels artefactes.

### Opció recomanada: Setup.exe

Descarrega `Agent_Cripto_TDR_Setup_v0.4.2.exe` des de la Release corresponent i executa'l. L'instal·lador només copia els fitxers autocontinguts i crea els accessos directes seleccionats. No descarrega components durant la instal·lació.

### Opció portable: ZIP

Descarrega `Agent_Cripto_TDR_Windows_v0.4.2.zip`, descomprimeix-lo i executa `INICIAR_AGENT.bat`. No cal instal·lar Python, Streamlit, VS Code ni cap altra llibreria.

> L'accés a Internet continua sent necessari quan l'aplicació consulta dades públiques de mercat als exchanges.

## Seguretat de la distribució

La v0.4.0 utilitzava un bootstrap de PowerShell que descarregava Python i l'instal·lava silenciosament. Aquest patró podia activar deteccions heurístiques d'antivirus encara que el codi fos legítim. La v0.4.1 va eliminar completament aquest mecanisme i la v0.4.2 manté aquesta arquitectura.

Els artefactes de cada Release es construeixen a GitHub Actions. Pots verificar-los amb els hashes SHA-256 publicats a `SHA256SUMS.txt`.

L'instal·lador encara no està signat amb un certificat comercial de code signing; per tant, Windows o algun antivirus poden mostrar avisos de reputació o «editor desconegut». Consulta `SECURITY.md` per als detalls.

## Funcions

- **Catàleg dinàmic de criptomonedes:** parelles spot disponibles a Kraken, Binance, Coinbase i Bitstamp per a EUR, USD, USDT o USDC.
- **Regles editables:** EMA, RSI i MACD activables i configurables.
- **Holders configurables:** cada holder manté una criptomoneda durant tot el període.
- **Monte Carlo:** comparació amb fins a 10.000 agents aleatoris.
- **Inversors humans:** importació de decisions mitjançant CSV.
- **Resultats:** capital final, rendibilitat, drawdown, Sharpe, reequilibris, gràfics i exportacions CSV.
- **Interfície multiidioma:** català, castellà, anglès, euskera i gallec.

## Idiomes

Els fitxers de traducció són:
- `app/locales/ca.json` — Català
- `app/locales/es.json` — Español
- `app/locales/en.json` — English
- `app/locales/eu.json` — Euskara
- `app/locales/gl.json` — Galego

La lògica de càrrega i fallback és a `app/i18n.py`. Si manca una clau en algun idioma, s'utilitza el català com a idioma de reserva.

## Criteri metodològic

L'aplicació permet editar les regles per experimentar. Per a la part principal del TDR convé **definir i congelar les regles abans del període de test**. Si es retoquen després de veure els resultats, cal tractar-ho com una nova especificació i provar-la en un altre període fora de mostra.

## Desenvolupament des del codi font

El repositori no conté el runtime binari de Python. Els binaris només es generen a les Releases mitjançant GitHub Actions. Per executar directament el codi font cal un entorn Python propi i instal·lar `requirements.txt`.

## Abast

Projecte exclusivament educatiu. No guarda credencials d'exchange, no opera amb diners reals i el resultat d'un backtest no garanteix rendiments futurs.
