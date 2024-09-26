
---

**Get Started**

- Do ALL the operations specified here in the root directory of the project, otherwise you will receive
      localized results.

---

**Generating the ORM Graph**

- Generating a JPEG file
```bash
python manage.py graph_models -a -g -o bimod_db_dd-MM-YYYY.png
```

- Generating a JSON file
```bash
python manage.py graph_models -a -g -o bimod_db_dd-MM-YYYY.json
```

- Generating an HTML file
```bash
python manage.py graph_models -a -g -o bimod_db_dd-MM-YYYY.html
```

- Generating an SVG file
```bash
python manage.py graph_models -a -g -o bimod_db_dd-MM-YYYY.svg
```

- Generating a DOT file
```bash
python manage.py graph_models -a -g -o bimod_db_dd-MM-YYYY.dot
```

---

**Generating the Class and Package Graphs**

- Generating a SVG file
```bash
pyreverse -o svg -p bimod_project -a 100 -s 100 -f ALL *
```
