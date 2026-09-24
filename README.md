# Agent Cripto TDR — Windows · v0.4

Aplicació educativa per comparar una estratègia tècnica de criptomonedes amb **holders**, agents aleatoris i inversors humans utilitzant dades reals de mercat. **No executa operacions reals ni necessita claus API.**

## Instal·lació: zero configuració

1. Descomprimeix la carpeta `Agent_Cripto_TDR` en un lloc normal de Windows (Documents o Escriptori, per exemple).
2. Fes doble clic a **`INSTAL_LAR_AGENT.bat`**.
3. El programa ho fa tot automàticament:
   - descarrega i instal·la un Python dedicat a l'Agent, sense modificar el Python del sistema;
   - crea un entorn privat `.venv`;
   - instal·la **Streamlit**, `pandas`, `numpy`, `plotly` i `ccxt`;
   - comprova que totes les llibreries es carreguen correctament;
   - crea l'accés directe **Agent Cripto TDR** a l'escriptori.
4. Inicia l'aplicació des de l'accés directe o amb `INICIAR_AGENT.bat`.

**No cal instal·lar manualment Python, Streamlit, VS Code ni cap altra llibreria.**

## Novetats v0.4

- **Interfície multiidioma completa:** català, castellà, anglès, euskera i gallec.
- Selector d'idioma a la part superior de la barra lateral.
- Traducció de menús, ajudes, regles EMA/RSI/MACD, missatges de simulació, resultats, gràfics, taules i apartat d'inversors humans.
- Arquitectura d'internacionalització separada a `app/locales/`, amb un fitxer JSON per idioma.
- Afegir un nou idioma ja no requereix modificar la lògica de l'aplicació: n'hi ha prou amb crear un nou fitxer de traduccions.

## Funcions de la v0.3 que es mantenen

- **Catàleg dinàmic de criptomonedes:** carrega les parelles spot disponibles a l'exchange per a EUR, USD, USDT o USDC.
- **Regles editables:** EMA, RSI i MACD es poden activar/desactivar i modificar.
- **Holders configurables:** es tria quants holders hi haurà i quina criptomoneda manté cadascun.
- **Gràfic de rendibilitat:** mostra l'evolució percentual de l'agent tècnic i de tots els holders.
- **Monte Carlo:** comparació amb fins a 10.000 agents aleatoris.
- **Inversors humans:** importació de decisions mitjançant CSV.

## Idiomes

Els fitxers de traducció són:

- `app/locales/ca.json` — Català
- `app/locales/es.json` — Español
- `app/locales/en.json` — English
- `app/locales/eu.json` — Euskara
- `app/locales/gl.json` — Galego

La lògica de càrrega i fallback és a `app/i18n.py`. Si manca una clau en algun idioma, s'utilitza el català com a idioma de reserva.

## Exchanges inclosos a la interfície

Kraken, Binance, Coinbase i Bitstamp. La disponibilitat de mercats i profunditat històrica depenen de cada exchange. Si se seleccionen moltes criptomonedes, la descàrrega pot trigar i el període comú d'anàlisi pot començar més tard si alguna moneda té poca història.

## Criteri metodològic important

L'aplicació permet editar les regles per experimentar. Per a la part principal del TDR convé **definir i congelar les regles abans del període de test**. Si es retoquen després de veure els resultats, cal tractar-ho com una nova especificació i provar-la en un altre període fora de mostra.

## Diagnòstic

Si la instal·lació falla, consulta `install.log`. L'instal·lador no marca la instal·lació com a completada fins que comprova que `streamlit`, `pandas`, `numpy`, `plotly` i `ccxt` funcionen.

## Seguretat i abast

Projecte exclusivament educatiu. No guarda claus d'exchange, no opera amb diners reals i no ofereix assessorament financer.
