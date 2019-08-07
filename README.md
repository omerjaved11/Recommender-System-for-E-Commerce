# Recommender-System-for-E-Commerce
## Live @ http://ecommercefyp.herokuapp.com/

### Clone the Repo
 
```bash

git clone https://github.com/omerjaved11/Recommender-System-for-E-Commerce


```

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required libraries.

```bash

pip install -r requirments.txt

```

### migrations
```bash

python manage.py makemigrations --settings=e_commerce.settings_local

python manage.py migrate

```
### Run


```bash

python manage.py runserver --settings=e_commerce.settings_local

```
