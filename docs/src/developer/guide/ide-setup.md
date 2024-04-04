---
title: IDS SAWPS
summary: The SANBI Wildlife Protection System is a platform to track the population levels of endangered wildlife.
    - Jeremy Prior
    - Faneva Andriamiadantsoa
    - Jeff Osundwa
date: 09-11-2023
some_url: https://github.com/kartoza/sawps/
copyright: Copyright 2023, SANBI
contact: PROJECT_CONTACT
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
context_id: Y5SchQtfwRzvqu2qiHdxSe
---

## Setting up a dev env

Please follow the Kartoza [coding standards](https://kartoza.github.io/TheKartozaHandbook/development/conventions/coding_standards/#compliance).

### 🏃‍♂️ How To Run Project with Visual Studio Code

Copy and customize environnment file: Create a copy of the ```deployment/.template.env``` file and name it ```deployment/.env```. Update the ```deployment/.env``` file with your project-specific settings.
![image](https://user-images.githubusercontent.com/178003/231014472-c77f7a00-1a1d-43d0-8c06-ef9634f2ccc7.png)


Add a ```.env``` file in the project root directory with the below content:

```
COMPOSE_PROJECT_NAME=sanbi
```

This is to ensure the containers that VS Code builds are using that project name. For more information, follow [this link](https://code.visualstudio.com/remote/advancedcontainers/set-docker-compose-project-name).

Ensure Dev Containers extension is installed
![image](https://user-images.githubusercontent.com/178003/231014270-65212ed8-6d78-4966-9c2b-f9ebe82f9025.png)

Build and open project in devcontainer: press ```Cmd+Shift+P``` (macOS) or ```Ctrl+Shift+P``` (Windows/Linux) to open the Command Palette. Type ```Dev Containers: Rebuild and Reopen in Container``` and select it to reopen the folder inside the devcontainer.
![image](https://user-images.githubusercontent.com/178003/231014643-3e4e9e56-1d03-4e15-9015-9f85a2a715a2.png)

Change the permissions of the django_project folder:

```
chmod -R a+rw django_project
```

Install dependencies inside the container: Press ```Cmd+Shift+P``` (macOS) or ```Ctrl+Shift+P``` (Windows/Linux), type ```Tasks: Run Tasks``` and select it. Choose ```React: Install dependencies``` to install the necessary dependencies.

![image](https://user-images.githubusercontent.com/178003/231015768-39803d00-95dc-42c7-a08f-ab58ac09fa58.png)

![image](https://user-images.githubusercontent.com/178003/231016195-5d78356b-e802-40f6-aa33-82404b65925d.png)


Run the migrations inside the container: Press ```Cmd+Shift+P``` (macOS) or ```Ctrl+Shift+P``` (Windows/Linux), and type ```Tasks: Run Tasks``` and select it. Choose ```Django: Migrate```.

![image](https://user-images.githubusercontent.com/178003/231015768-39803d00-95dc-42c7-a08f-ab58ac09fa58.png)

![django-migrate](./img/ide-setup-django-migrate-1.png)

#### 👩‍💻 Open the developer site

Run the project inside the container: Press ```Cmd+Shift+D``` (macOS) or ```Ctrl+Shift+D``` (Windows/Linux), and choose ```Django+React``` in the RUN AND DEBUG dropdown.

![image](https://user-images.githubusercontent.com/178003/231016537-cda1d85f-5123-45ef-8f51-c12e90e1d0c9.png)


Review the list of forwarded ports from the container to your local host:

![forwarded-ports](./img/ide-setup-forwarded-ports-1.png)


Open your web browser and go to localhost:8000 to view the running application.

#### 👩‍🏭 Create a super user

![django-superuser1](./img/ide-setup-django-superuser1.png)

#### 💽 Restoring layer schema for map

The full dump file for layer schema is ~5.3GB, meanwhile compact dump file is only 24MB.

[Download Full Dump File for Layer.](https://drive.google.com/file/d/1-6y5tuMNc2sQ1G3qjyntL4PDV6ubCnbc/view?usp=sharing)

[Download Compact Dump File for Layer.](https://drive.google.com/file/d/1Q0WhUP74MCoC_JcD4qMK1Egs575xrhqQ/view?usp=sharing)

Preview for compact dump file:
![sanbi_maps_compact](./img/sanbi_compact_preview.jpg)

Copy the dump file to db container. Then run pg_restore from inside db container to restore the dump file.

```
docker cp sanbi_layer_db_compact.dump deployment-db-1:/home/sanbi_layer_db_compact.dump
docker exec -it deployment-db-1 /bin/bash
cd /home
pg_restore -h 127.0.0.1 -U docker -d django -n layer sanbi_layer_db_compact.dump
```

#### Load Fixtures

To load fixtures into your database, you can use the `loaddata` management command.

Run this command to load all the fixtures.
```
cd django_project
python manage.py loaddata fixtures/*.json
```

Run this command to load the specific fixture.
```
cd django_project
python manage.py loaddata fixtures/<name of the fixture>.json
```
