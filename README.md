This project provides FACX, a bilingual questioning and answering assistant over Linked Data.


---

### How to use
#### 1. Download Data
Since the data is large, it is not included in this repository. Download link: https://drive.google.com/file/d/1yjtQmLHIxPoZtTfXlHbuMf5YMQJ3w-LF/view?usp=sharing. After download is complete, place the data in bilingual-qald/data folder

#### 2. Change Fuseki-Server Configuration
Change ja:rulesFrom and tdb:location path in bilingual-qald/json2jena/rdf2jena/apache-jena-fuseki-3.10.0.2/run/configuration/fuseki_conf.ttl according to your download folder 

#### 3. Start Apache Server
Go to bilingual-qald/json2jena/rdf2jena/apache-jena-fuseki-3.10.0.2/ and start fuseki-server.

```python
cd bilingual-qald/json2jena/rdf2jena/apache-jena-fuseki-3.10.0.2/ 
./fuseki-server
```

#### 4. Run the Application
start UI_demo.py to ask questions.

```python
python UI_demo.py
```
