# Garbage Bot
UB HACKATHON 2017, Garbage Kids багийн бүтээл

## Chatbot хөдөлгүүр

### Ажиллуулах
#### Тохиргоо
`AIbase/settings/main.json` файлыг нээж тохиргоог тохируулна үүний дараа 
`AIbase` хавтасан доторхи `run.py` файлыг ажиллуулсанаар чатбот хөдөлгүүр ачааллна

Хэрэв ачааллах үед сургалтын моделийн файлыг олсонгүй гэсэн алдаа гарвал `AIbase/learn.py` файлыг ачааллсанаар машин-сургалтыг эхлүүлж, сургалтын модел файлтай болно.

#### Тохиргоо хийх файл
```javascript
{
  "corpus_source":{
    "file_or_database": true, /* True (DB-с унших), False (Файлаас унших) */
    "database": {
      "engine": "mongodb", /* DBMS, Одоохондоо зөвхөн mongo дэмжинэ */
      "username": "admin", /* Нэврэх нэр */
      "passowrd": "admin", /* Нэврэх нууц үг */
      "dbname": "mydatabase", /* DB сангийн нэр */
      "host" : "127.0.0.1", /* DB холбогдох хаяг */
      "port" : 27017 /* DB холбогдох порт */
    },
    "file": {
      "data_location" : "case.data", /* текст мөр бүхий сургалтын корпус */
      "meta_location" : "case.meta" /* текст мөрүүдэд харгалзах ангилалуудыг агуулсан файл */
    }
  },
  "learning": {
    "model_filename": "garbageKidsDemo", /* сургасан моделоо хадгалах файлын нэр */
    "learn_validation_token": "GHTWXADWA" 
  },
  "receiver": {
    "format": "json", /* Мэссэж хүлээж авах/илгээх формат */
    "method": "POST" /* Мэссэж хүлээж авах HTTP Method */
  },
  "defaults": {
    /* Чатбот хариулт өгөх боломжгүй эсвэл хангалттай өндөр магадлалтай хариулт олж чадахгүй бол */
    "unknown_text": "Уучлаарай. Асуултанд хариулахад миний мэдлэг хүрэлцэхгүй байна"
  }
}
```

### Хамаарал
* Python 3.X
* Natural Language Tool Kit - [суулгах](http://www.nltk.org/install.html)
* Flask - [суулгах](http://flask.pocoo.org/)
