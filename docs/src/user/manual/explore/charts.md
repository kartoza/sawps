---
title: IDS SAWPS
summary: The SANBI Wildlife Protection System is a platform to track the population levels of endangered wildlife.
    - Jeremy Prior
    - Ketan Bamniya
date: 09-11-2023
some_url: https://github.com/kartoza/sawps/
copyright: Copyright 2023, SANBI
contact: PROJECT_CONTACT
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
context_id: ZSVG5K6yFRsQVQF5WQFqJR
---

# Charts Page: Download Data Visualisation Functionality Documentation

The `Charts` tab is a powerful tool for visualising data through various charts and graphs. This documentation outlines the functionality of the `Download Data Visualisation` feature, which allows the user to download the charts presented on the page.

## Charts Page

![Charts Page](./img/charts-1.png)

1. **Explore**: By clicking on the `EXPLORE` on the navigation bar the user will be able to see the option for the Charts.

2. **Charts**: By clicking on the `CHARTS` tab, the user will be able to see the various charts. The `Charts` tab offers a variety of charts for data visualisation.

3. **Download Data Visualisation**: The `DOWNLOAD DATA VISUALISATION` button is a convenient feature that enables the user to download the charts and visualisations displayed on the page.

## Usage

To utilise the `Download Data Visualisation` functionality, follow these steps:

- Navigate to the `Charts Page` where the user can visualise their data using charts and graphs.

- Locate the `DOWNLOAD DATA VISUALISATION` button, usually placed in a prominent position on the page.

- Click on the button to initiate the download process.

## Charts On Charts Page
The charts shown to user are configurable via group permission in the Group Table in [Django Admin](../../../administrator/manual/django-table.md).

![Charts On Charts Page](./img/charts-2.png)

### Property Count Per Category Charts
These charts show property count per category (population size, property area, area available to species, 
and population density). The colours are configurable via Property Type page in [Django Admin](../../../administrator/manual/django-admin.md) 
![Property count per category](./img/charts-4.png)

## Downloaded Charts PDF

![Downloaded Charts PDF](./img/charts-3.png)

## Summary

The `Download Data Visualisation` functionality on the Charts Page is a valuable feature for saving data visualisations. It allows the user to capture insights presented in charts, making it easier to share and use the data for various purposes, including reporting, analysis, and collaboration with others.
