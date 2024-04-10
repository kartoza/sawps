---
title: IDS SAWPS
summary: The SANBI Wildlife Protection System is a platform to track the population levels of endangered wildlife.
    - Jeremy Prior
    - Faneva Andriamiadantsoa
    - Zulfikar Muzakki
date: 09-11-2023
some_url: https://github.com/kartoza/sawps/
copyright: Copyright 2023, SANBI
contact: PROJECT_CONTACT
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
context_id: NHUoStSTW5N7xpC7uCCD5z
---

# Admin

::: django_project.property.admin
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


# Factories

::: django_project.property.factories
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true

# Models

::: django_project.property.models
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


# Test Case

::: django_project.property.tests.test_property_models
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: django_project.property.tests.test_spatial_data
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: django_project.property.tests.test_migration
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: django_project.property.tests.test_generate_property_centroid
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


# Tasks


::: django_project.property.tasks.generate_property_centroid
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: django_project.property.tasks.generate_spatial_filter
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true


::: django_project.property.tasks.update_organisation_property_short_code
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true

# Spatial Data


::: django_project.property.spatial_data
    handler: python
    options:
        docstring_style: sphinx
        heading_level: 1
        show_source: true
