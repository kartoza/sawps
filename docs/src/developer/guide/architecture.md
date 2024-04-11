---
title: IDS SAWPS
summary: The SANBI Wildlife Protection System is a platform to track the population levels of endangered wildlife.
    - Jeremy Prior
    - Luna Asefaw
date: 09-11-2023
some_url: https://github.com/kartoza/sawps/
copyright: Copyright 2023, SANBI
contact: M.Child@sanbi.org.za
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
context_id: StvndnegfjdfNwBXQywyzA
---

# System architecture

In this section, we outline the system architecture using ER Diagrams, Software Component Diagrams etc. and key libraries / frameworks used in this project.

## Frameworks used

The following is a list, with brief descriptions, of the key components used in creating this platform. Please refer to their individual documentation for in-depth technical information.

| Logo | Name | Notes |
|------------|---------|----------------|
|![Django](img/architecture-django-1.png){: style="height:30px"} | [Django](https://djangoproject.com) | Django makes it easier to build better web apps more quickly and with less code. |
|![Reactjs](img/architecture-reactjs-1.png){: style="height:30px"} | [ReactJS](https://react.dev/) | React lets you build user interfaces out of individual pieces called components. Create your own React components like `Thumbnail`, `LikeButton`, and `Video`. Then combine them into entire screens, pages, and apps.|
| ![Docker](img/architecture-docker-1.png){: style="height:30px"}  |  [Docker](https://docker.com) | Accelerate how you build, share, and run applications. Docker helps developers build, share, and run applications anywhere — without tedious environment configuration or management. |
| ![Docker-rest-framework](img/architecture-django-rest-framework-1.png){: style="height:30px"}  | [Django Rest Framework](https://www.django-rest-framework.org/) | Django REST framework is a powerful and flexible toolkit for building Web APIs. |
| ![Maplibre](img/architecture-maplibre-1.png){: style="height:30px"}   | [MapLibre](https://maplibre.org/)  | Open-source mapping libraries for web and mobile app developers. |
| ![Postgis](img/architecture-postgis-1.png){: style="height:30px"}   | [PostGIS](https://postgis.net/) | PostGIS extends the capabilities of the PostgreSQL relational database by adding support storing, indexing and querying geographic data. |
| ![PostgreSQL](img/architecture-postgresql-1.png){: style="height:30px"}   | [PostgreSQL](https://www.postgresql.org/) | PostgreSQL is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.  |
| ![Tegola](img/architecture-tegola-1.png){: style="height:30px"}  | [Tegola](https://tegola.io/) | An open source vector tile server written in Go, Tegola takes geospatial data and slices it into vector tiles that can be efficiently delivered to any client. |
| ![Mapbox](img/architecture-mapbox-1.png){: style="height:30px"}  | [Mapbox](https://www.mapbox.com/) | Mapbox is a mapping and location cloud platform for developers |
| ![Maputnik](img/architecture-maputnik-1.png){: style="height:30px"}  | [Maputnik](https://maputnik.github.io/) | Maputnik is a free and open source visual editor for the Mapbox GL style specification. |
| ![Plumber](img/architecture-plumber-1.png){: style="height:30px"}  | [Plumber](https://www.rplumber.io/) | The plumber package allows you to create APIs from your R code. |
| ![Jenkins](img/architecture-jenkins-1.png){: style="height:30px"}  | [Jenkins](https://www.jenkins.io/) | It is used to continually create and test software projects, making it easier for developers and DevOps engineers to integrate changes to the project and for consumers to get a new build. |
| ![Argo](img/architecture-argo-1.png){: style="height:30px"} | [Argo](https://www.argodevops.co.uk/) | Argo Events is an event-driven workflow automation framework and dependency manager that helps you manage Kubernetes resources, Argo Workflows, and serverless workloads on events from a variety of source. |

## High-level system architecture

This is the high-level system architecture relating to the interaction between the applications.
![Overview](img/architecture-overview-1.png)

This is an overview of the interaction between the backend and frontend.
![Backend-frontend](img/architecture-backend-frontend-1.png)

This is the high level overview of the DevOps implementation.
![DevOps](img/architecture-devops-1.png)

## Data model

The project's ERD can be found [here](https://drive.google.com/file/d/1O92w2zwbKm_SARXnXIljHbX-rQPmFiXM/view)

![ERD](img/architecture-ERD-1.png)

Click [SchemaSpy Documentation](https://sawps-data-model.vercel.app/) for the full documentation of the data model.
