# Raamatukogu
Raamatukogu teemaline proovitöö

| Tegevus | URL | Meetod | Parameetrid |
|---------|-----|--------|-------------|
| Sisselogimine | /login | GET||
| Üldine seis | /book | GET |
| Lisa uus raamat | /book | POST | {"title": [string], "author": [string], "location": [int]} |
| Vaata raamatu infot | /book/:book_id | GET | book_id=[int]
| Võta raamat vastu | /book/:book_id | POST | book_id=[int]
| Kustuta raamat | /book/:book_id | DELETE | book_id=[int]
| Laenuta raamat välja | /book/:book_id/:lender_id | POST | book_id=[int], lender_id=[int]
| Otsi raamatut | /book/search | POST |
| Lisa uus laenutaja | /lender | POST | {"name": [string], "surname": [string], "personal_code": [int]}
| Vaata laenutaja infot | /lender/:lender_id | GET | lender_id=[int]
| Otsi laenutajat | /lender/search | POST |
| Üle aja läinud laenutajad | /overtime | GET |
