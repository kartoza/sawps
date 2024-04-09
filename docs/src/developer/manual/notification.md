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
context_id: X6HSV6uqFkdc2UdmcRqRXL
---

# Admin

::: django_project.notification.admin
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


# Models

::: django_project.notification.models.reminder
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


# Test Case

::: django_project.notification.tests.reminder_factory
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: django_project.notification.tests.test_api_views
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: django_project.notification.tests.test_reminder
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


