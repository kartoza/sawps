---
title: IDS SAWPS
summary: The SANBI Wildlife Protection System is a platform to track the population levels of endangered wildlife.
    - Jeremy Prior
    - Faneva Andriamiadantsoa
    - Zulfikar Muzakki
date: 09-11-2023
some_url: https://github.com/kartoza/sawps/
copyright: Copyright 2023, SANBI
contact: M.Child@sanbi.org.za
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
context_id: HwVCsNKPhxe9LX6tUa4EPr
---

## Settings
::: django_project.core.settings.base
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


## ASGI
::: django_project.core.asgi
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


## CELERY
::: django_project.core.celery
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true

## URLS
::: django_project.core.urls
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true

## WSGI
::: django_project.core.wsgi
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true