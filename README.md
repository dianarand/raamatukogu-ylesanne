# Raamatukogu
Raamatukogu teemaline proovitöö

Nõuded on saadaval failis requirements.txt

## API

| Tegevus | URL | Meetod | Parameetrid |
|---------|-----|--------|-------------|
| Sisselogimine | /login | GET||
| Üldine seis | /book | GET |
| Lisa uus raamat | /book | POST | {"title": [string], "author": [string], "location": [int]} |
| Vaata raamatu infot | /book/:book_id | GET | book_id=[int]
| Võta raamat vastu | /book/:book_id | POST | book_id=[int]
| Kustuta raamat | /book/:book_id | DELETE | book_id=[int]
| Laenuta raamat välja | /book/:book_id/:lender_id | POST | book_id=[int], lender_id=[int]
| Otsi raamatut | /book/search | POST | {"title": [string], "author": [string]}
| Lisa uus laenutaja | /lender | POST | {"name": [string], "surname": [string], "personal_code": [int]}
| Vaata laenutaja infot | /lender/:lender_id | GET | lender_id=[int]
| Otsi laenutajat | /lender/search | POST | {"surname": [string], "personal_code": [int]}
| Üle aja läinud laenutajad | /overtime | GET |

Otsinguid kasutades võib anda sisse nii ühe kui ka mõlemad parameetritest.

## Andmebaas

Raamatutel on järgnevad omadused:
* **id**: raamatu ID [int]
* **title**: raamatu pealkiri [string]
* **author**: raamatu autor [string]
* **location**: raamatu asukoht riiuli numbrina [int]
* **date_added**: raamatukokku saabumise kuupäev [date], vaikimisi väärtus raamatu lisamisel on tänane kuupäev
* **lender_id**: raamatu laenutaja ID [int] 
* **deadline**: raamatu tagastamise tähtaeg [date]

Laenutajatel on järgnevad omadused:
* **id**: laenutaja ID [int]
* **name**: laenutaja eesnimi [string]
* **surname**: laenutaja perekonnanimi [string]
* **personal_code**: laenutaja isikukood [string]
* **books**: laenutatud raamatud
