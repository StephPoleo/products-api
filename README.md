# Zebrands API REST Challenge

API REST for products and users.

## Description

Developing a basic catalog system to manage products.

- A product should have basic info such as sku, name, price and brand. Other fields for product are availability and average rating.

- There will be two type of users:
  (i) admins to create / update / delete products and to create / update / delete other admins.
  (ii) anonymous users who can only retrieve products information but can't make changes.

- Whenever an admin user makes a change in a product (for example, if a price is adjusted), the system notifies all other admins about the change via email.

- Tracking system of the number of times every single product is queried by an anonymous/admin user, and building analytics for the gathered information.

## Getting Started

### Dependencies

- 'rest_framework',
- 'rest_framework_swagger',
- 'drf_yasg'
- 'psycopg2'

### Installing

- To download this project, first you have to clone it from the Github repository by searching the "Code" option or clicking here: https://github.com/StephPoleo/products-api.git

- The project contains 3 folders, 'ProductsProject', 'ProductsAPI' and 'analytics'. For them there are not modifications needed. Unless you are using a database different from PostgresSQL and PgAdmin. In that case, please modify the 'settings.py' file, on the ProductsProject folder. Inside the 'DATABASE' configurations.

- For a PostgreSQL configuration, please use the following credentials:

        'NAME': 'rest-api',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '5432',

### Executing program

Please follow the next steps to execute the project:

- After cloning the repository, open your terminal and go to the project path. Make sure to be on the 'ProductsProject' folder (the one that contains the manage.py file) and type the following comamand:

```
python manage.py makemigrations
```

- If there's any errors, please check your connection to the database. Otherwise, continue:

```
python manage.py migrate
```

- Once everything is set up with the database, the next step is to create a super user:

```
python manage.py createsuperuser
```

- The console will ask you to enter a user, email and password for this super user. Put anything, and then type:

```
python manage.py runserver
```

## Help

Any advise for common problems or issues.

```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

- 0.2
  - Various bug fixes and optimizations
  - See [commit change]() or See [release history]()
- 0.1
  - Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.

- [awesome-readme](https://github.com/matiassingers/awesome-readme)
- [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
- [dbader](https://github.com/dbader/readme-template)
- [zenorocha](https://gist.github.com/zenorocha/4526327)
- [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
