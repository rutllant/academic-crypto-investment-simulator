# Changelog

## 0.4.3
- Afegida una auditoria numèrica automatitzada del motor de simulació.
- Corregit el biaix d'execució a la mateixa barra: un senyal calculat amb el tancament del dia t només pot executar-se a l'obertura de la sessió següent.
- El registre d'operacions incorpora `signal_date` i la data d'execució.
- Els holders compren a l'obertura de la primera sessió d'avaluació i es valoren al tancament.
- Les decisions humanes datades a t es fan efectives a la primera sessió posterior.
- Corregit el càlcul de drawdown i rendiments diaris perquè el capital inicial formi part del punt de referència; així les pèrdues/comissions de la primera sessió no desapareixen de les mètriques.
- Millorat el càlcul de comissions: el cost es resol de manera coherent amb el capital postoperació i el nominal realment negociat.
- Afegida validació d'integritat OHLCV: timestamps, valors finits i positius, coherència high/low i volum no negatiu.
- Afegits tests independents per EMA, RSI i MACD, HODL amb resultat conegut, comissions, pesos, drawdown, no-look-ahead, decisions humanes i reproductibilitat Monte Carlo.
- GitHub Actions executa la suite numèrica abans de considerar vàlid el projecte.
- Afegit `VALIDATION.md` amb l'abast, els resultats esperats i les limitacions de l'auditoria.
- Els resultats generats amb v0.4.2 o anteriors no són estrictament comparables amb v0.4.3 perquè canvia el moment d'execució de les ordres.

## 0.4.2
- Incorporats dos manuals d'usuari pensats per a persones sense experiència prèvia en inversions.
- Afegit `docs/MANUAL_USUARI.md` en català.
- Afegit `docs/USER_MANUAL_EN.md` en anglès.
- Els manuals expliquen exchange, spot, cartera, CASH, EMA, RSI, MACD, holders, agents aleatoris, Monte Carlo, rendibilitat, drawdown, Sharpe, percentils, reequilibris, inversors humans i overfitting.
- Els manuals queden inclosos automàticament al ZIP portable i al `Setup.exe`.
- La validació automàtica exigeix la presència dels dos manuals.

## 0.4.1
- Redissenyada la distribució Windows per reduir falsos positius d'antivirus.
- Eliminats `setup.ps1`, `ExecutionPolicy Bypass` i la instal·lació dinàmica de Python a l'ordinador de l'usuari.
- La Release inclou un runtime Python portable i totes les dependències necessàries.
- GitHub Actions verifica el runtime empaquetat abans de publicar-lo.
- La Release genera un ZIP portable, un instal·lador convencional `Setup.exe` amb Inno Setup i `SHA256SUMS.txt`.
- Afegit `SECURITY.md`.

## 0.4
- Afegida interfície multiidioma.
- Idiomes: català, castellà, anglès, euskera i gallec.
- Traduccions separades en fitxers JSON dins `app/locales/`.
- Afegit mòdul `app/i18n.py` amb fallback al català.

## 0.3
- Catàleg dinàmic de criptomonedes.
- Regles EMA, RSI i MACD editables.
- Holders configurables i gràfic comparatiu de rendibilitat.
- Monte Carlo i inversors humans generalitzats.
