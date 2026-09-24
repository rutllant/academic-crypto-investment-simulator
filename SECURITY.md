# Security

## Abast del projecte

Academic Crypto Investment Simulator és una aplicació educativa. No executa operacions reals, no demana credencials d'exchange i no necessita claus API.

## Distribució Windows v0.4.1+

Les Releases de Windows es construeixen automàticament mitjançant GitHub Actions. El runtime Python i les dependències s'incorporen durant el procés de build; l'ordinador de l'usuari no descarrega ni instal·la Python i no executa scripts PowerShell de bootstrap.

La distribució publica:
- un ZIP portable;
- un instal·lador Inno Setup;
- un fitxer `SHA256SUMS.txt` amb el hash SHA-256 dels artefactes.

## Verificació

A PowerShell de Windows es pot comprovar un fitxer descarregat amb:

```powershell
Get-FileHash .\Agent_Cripto_TDR_Windows_v0.4.1.zip -Algorithm SHA256
```

El valor ha de coincidir exactament amb el publicat a `SHA256SUMS.txt` de la mateixa Release.

## Signatura digital

Actualment l'instal·lador no està signat amb un certificat comercial de code signing. Per això Windows SmartScreen o alguns antivirus poden mostrar avisos de reputació o indicar «editor desconegut». Una alerta de reputació no equival per si sola a una detecció de malware, però qualsevol detecció concreta s'ha d'investigar abans d'afegir excepcions.

## Historial

La v0.4.0 incloïa `setup.ps1`, que descarregava Python des de python.org i l'instal·lava de manera silenciosa. Aquest mecanisme es va retirar a la v0.4.1 perquè el patró podia activar heurístiques d'antivirus.
