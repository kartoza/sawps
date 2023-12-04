---
title: IDS SAWPS
summary: The SANBI Wildlife Protection System is a platform to track the population levels of endangered wildlife.
    - Jeremy Prior
    - Luna Asefaw
date: 09-11-2023
some_url: https://github.com/kartoza/sawps/
copyright: Copyright 2023, SANBI
contact: PROJECT_CONTACT
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
context_id: 8r7JA5mUz3eJQxgL8fkQbL
---

# Managing Lookup Tables

This section describes how administrators can manage the values in the look-up tables (i.e. add/edit/delete the options available in dropdown menus) on the backend so these values are reflected in the front-end and backend dropdown menus.

## Where to Manage Lookup Tables

When you are adding/managing/deleting records on the administration site you will see a little yellow pencil (Similar to ✏️). If you click on the yellow pencil, a popup window will open with a form you can edit to manage a specific lookup table.

![Manage Lookup Tables 1](./img/manage-lookup-tables-1.png)

## How to Manage Lookup Tables

On the popup that opens you will be able to edit the record within the lookup table.

![Manage Lookup Tables 2](./img/manage-lookup-tables-2.png)

Once you have made your changes you can click on 1️⃣ the `Save` button.

![Manage Lookup Tables 3](./img/manage-lookup-tables-3.png)

## Lookup tables that you can edit

On the landing page of the administration site you will see links to the various lookup tables. The tables that you can edit are as follows:

- Survey Methods
- Open Close System (must also update template)
- Population Estimate Category (must also update template)
- Population Status (must also update template)
- Sampling Effort Coverage (must also update template)
- Property Types
- Taxa (Read through [manage taxa](./manage-taxa.md) for more in-depth information)
- Titles

## Lookup tables that you should not edit

The tables that should not be edited/touched without a core developer present to guide you are:

- Activities
- Everything under Front-end heading
- Provinces
- Parcel Types
