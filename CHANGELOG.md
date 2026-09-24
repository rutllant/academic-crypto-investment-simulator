# Changelog

## 0.4.1
- Redissenyada la distribució Windows per reduir falsos positius d'antivirus.
- Eliminats `setup.ps1`, `ExecutionPolicy Bypass` i la instal·lació dinàmica de Python a l'ordinador de l'usuari.
- La Release inclou un runtime Python portable i totes les dependències necessàries.
- GitHub Actions verifica el runtime empaquetat abans de publicar-lo.
- La Release genera un ZIP portable, un instal·lador convencional `Setup.exe` amb Inno Setup i un fitxer `SHA256SUMS.txt`.
- Afegit `SECURITY.md` amb informació de seguretat i verificació.
- El motor de simulació i les regles d'inversió no canvien respecte de la v0.4.0.

## 0.4
- Afegida interfície multiidioma.
- Idiomes: català, castellà, anglès, euskera i gallec.
- Traduccions separades en fitxers JSON dins `app/locales/`.
- Afegit mòdul `app/i18n.py` amb fallback al català.
- Actualitzada la versió de l'instal·lador Inno Setup a 0.4.

## 0.3
- Catàleg dinàmic de criptomonedes.
- Regles EMA, RSI i MACD editables.
- Holders configurables i gràfic comparatiu de rendibilitat.
- Monte Carlo i inversors humans generalitzats.
