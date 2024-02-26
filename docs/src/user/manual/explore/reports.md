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
context_id: BYbnmQvaLxzHsfjUtsaAFn
---

# Reports Table Page Documentation

The Reports Table Page is the central hub for viewing and interacting with the user's data. This page offers a user-friendly interface for exploring and manipulating the user's dataset. Users can use a variety of features to customise their data view, including filters, column search, and data export options.

> DISCLAIMER: Some of the images in the manual may vary slightly from what you see on the platform due to continuous updates to the platform. On the platform you will see `green question mark` ![Help Desk Icon 1](./img/help-icon.png) buttons in the top right corner (underneath the `LOGOUT` button), you can click on these to access the help desk.

## Reports Display

The main area of the page displays the user's dataset in a tabular format. Each row represents a record, and each column represents a data attribute.

### Reports table

![Reports table](./img/reports-1.png)

1. **Explore**: Click on the `EXPLORE` link available on the navigation bar to open the explore page.
2. **Reports**: Click on the `REPORTS` link to view the data.
3. **Filters**: Utilise the filters provided on the page to refine the user's data view. These filters include:
     * **Species Filter:** Filter data by species.
     * **Report Type Filter:** Filter data by report type.
     * **Organisation Filter:** Filter data by organisation.
     * **Property Filter:** Filter data by property.
     * **Year Range Filter:** Filter data by a specified year range.
     * **Activity Filter:** Filter data by activity type.
     * **Spatial Filter:** Filter data by spatial criteria.

     * **Applying Filters:**
         * Click on the respective filter dropdowns.
         * Set filter criteria.
         * Click on the filter to update the data display based on the user's filter selections.
     * Each filter is designed to help the user narrow down their dataset to view only the data that's relevant to their analysis.

4. **Column Search**: Users can search for specific values within columns by selecting the column. This feature is especially useful when the user needs to locate specific data points within a large dataset. The table will dynamically filter to display the selected column.
5. **DOWNLOAD DATA** In the `DOWNLOAD DATA` dropdown, users can select the preferred file format for downloading.
    ![Download Data Dropdown](./img/reports-10.png)

    1. **CSV Format:** Click on the `DOWNLOAD DATA CSV` button to download the current dataset in CSV format. Each CSV download generates separate files for individual data entries, providing a comprehensive yet modular view of the dataset.

        ![Downloaded CSV File](./img/reports-11.png)

    2. **XLSX Format:** Click on the `DOWNLOAD DATA XLSX` button to download the current dataset in XLSX format. This option consolidates all data into a single Excel file with different tabs, allowing users to conveniently navigate and analyze diverse aspects of the dataset within a unified document.

        ![Downloaded CSV File](./img/reports-12.png)

        - **Sheet 1:** Species report.
        - **Sheet 2:** Property report.

6. **DOWNLOAD DATA REPORT:** Click on the `DOWNLOAD DATA REPORT` button to download the current dataset in PDF format. The downloaded PDF document encapsulates the entire dataset in a cohesive report, featuring a structured layout with a header that provides an overview of the data. This format is ideal for presenting a comprehensive snapshot of the dataset.

    ![Downloaded PDF](./img/reports-13.png)

### Report Type

* **Activity Report:** Report on an activity basis.
* **Property Report:** Report on a property basis.
* **Species Report:** Report on a species basis.
* **Province Report:** Report on a province basis.
Only members of `National data consumer` group can see this report.
* **Sampling Report:** Filter data by property.
Members of `National data consumer` or `Provincial data consumer` **CAN NOT** see this report.

The user group is configurable from the User Table in the [Django Admin](../../../administrator/manual/django-admin.md).

### Reports Page with Reports Filter

![Reports Type](./img/reports-3.png)

1. **Report Type**: Report type filter with the reports type.

2. **Species**: The species icon is displayed with the count of selected species.

3. **Organisation**: The organisation icon is displayed with the count of selected organisations.

4. **Property**: The property icon is displayed with the count of selected properties.

5. **Clock Icon**: The clock icon serves as a visual indicator for the year range filter with year range.

6. **Activity**: The activity icon is displayed with the count of selected activities.

7. **Species List**: Displays the names of the selected species.

8. **Organisation List**: Displays the names of the selected organisations.

9. **Property List**: Displays the names of the selected properties.

10. **Activity List**: Displays the names of the selected activities.

#### Activity Report Filter

![Reports Type Filter](./img/reports-4.png)

1. **Activity Report**: Selected `Activity report`.

##### Activity Report Tables

![Activity Reports Table](./img/reports-5.png)

##### Activity Types

The Activity Report includes information for the following activity types:

1. **Translocation (Intake)**: This table provides details on translocation activities related to the intake of species, for properties per year.

2. **Translocation (Offtake)**: This table displays information about translocation activities related to off-take,  for properties per year.

3. **Planned Hunt/Cull**: This table contains data related to planned hunting or culling activities,  for properties per year.

4. **Planned Euthanasia/DCA**: This table presents information on planned euthanasia or disease control activities, for properties per year.

5. **Unplanned/Illegal Hunting**: This table offers insights into unplanned or illegal hunting activities,  for properties per year.

    **Table Columns**

    Each of the tables associated with the activity types contains the following columns:

     * **Property Name**: The name of the property where the activity took place.
     * **Scientific Name**: The scientific name of the species involved in the activity.
     * **Common Name**: The common name of the species.
     * **Year**: The year in which the activity occurred.
     * **Total**: The total count of the species involved in the activity.
     * **Adult Male**: The count of adult male individuals.
     * **Adult Female**: The count of adult female individuals.
     * **Juvenile Male**: The count of juvenile male individuals.
     * **Juvenile Female**: The count of juvenile female individuals.

##### Summary

The `Activity Report` is a valuable filter for generating detailed reports on a variety of wildlife management activities. It provides specific information for each activity type, including property details, species information, and counts related to the activities. This report allows for a comprehensive view of wildlife management efforts, enabling informed decision-making and analysis of data related to different activities.

#### Property Report

![Property Reports](./img/reports-6.png)

1. **Property Report**: Selected `Property report`.

2. **Property Table**: The property table displays data for the properties.

     **Report Columns**

     The Property Report includes the following columns:

     * **Property Name**: The name of the property being reported on.

     * **Scientific Name**: The scientific name of the species associated with the property.

     * **Common Name**: The common name of the species related to the property.

     * **Owner**: The name of the owner of the property.

     * **Owner Email**: The email address of the property owner.

     * **Property Type**: The type of the property.

     * **Province**: The province where the property is situated.

     * **Property Size (Ha)**: The size of the property in hectares.

     * **Area Available To Species**: The portion of the property that is available for species habitat.

     * **Open/Close Systems**: Indicates whether the property employs open or closed systems for wildlife management.

##### Summary

The `Property Report` is a critical filter for reporting on various properties. It provides information on property details, ownership, type, location, and specific data related to species habitat and wildlife management systems. This report is essential for analysing and managing property-related information in an organised and structured manner.

#### Province Report

![Province Report](./img/reports-9.png)

1. **Province Report**: Select the `Province Report` option to generate a report specifically for provinces.
> DISCLAIMER: 
2. **Province Table**: The Province report table displays data related to the provinces, including population information.

     **Report Columns**

     The Province Report includes the following columns:

     * **Year**: The specific year for which the data is recorded.

     * **Common Name**: The common name of the species associated with the province.

     * **Scientific Name**: The scientific name of the species.

     * **Total Population**: The total population of the species within the province for the specified year.

     * **Total Population Province Name**: The total population of the species within the respective province. This column is repeated for each province, and each entry represents the total population of the species in that specific province for the given year.

##### Summary

The Province Report serves as a valuable filter for reporting on provincial data related to species. It provides essential information on the total population of species within each province, as well as details about the species' common name, scientific name, and the year of data collection. This report is indispensable for in-depth analysis and management of species-related information at the provincial level.

#### Sampling Report Documentation

![Sampling Report](./img/reports-8.png)

1. **Sampling Report**: Selected `Sampling report`.

2. **Sampling Table**: The sampling report table displays data of the species for the property.

     **Report Columns**

     The Sampling Report includes the following columns:

     * **Property Name**: The name of the property where the sampling and population estimates were conducted.

     * **Scientific Name**: The scientific name of the species under consideration.

     * **Common Name**: The common name of the species.

     * **Population Status**: Indicates the status of the species population such as `Migratory` or `Resident`.

     * **Population Estimate Category**: Categorises the population estimate.

     * **Survey Method**: Describes the method used for surveying and data collection.

     * **Sampling Effort Coverage**: Indicates the extent to which the sampling effort covered the entire population or habitat.

     * **Population Estimate Certainty**: This represents the level of certainty of the estimated population.

##### Summary

The Sampling Report is a crucial tool for documenting and reporting on sampling efforts and population estimates for different species. It provides detailed information on property details, species information, and key metrics related to the population and the methods used for data collection. This report is essential for assessing population health and the effectiveness of conservation and management efforts.

#### Species Report

![Species Report](./img/reports-7.png)

1. **Species Report**: Selected `Species report`.

2. **Species Table**: The species report table displays data of the species for the property.

>Note: The users, based on their role, can edit or delete the species details. If the user is an organisational member, they can only edit or delete the records that they have submitted. However, if the user is an organisational manager,  they have the authority to edit or delete any data within that particular organisation.
This clarification ensures that editing and deletion permissions align with the user's role within the organisation, promoting efficient and secure data management practices.

3. **Edit Icon**: Click on the `Edit` icon, to update the species record. When the user clicks on the edit icon the online form step 1 opens. Users can update the species details here.

4. **Delete Icon:** Click on the `Delete` icon to remove the species record. Upon clicking the delete icon, a confirmation popup will appear, seeking confirmation for the deletion of the species record.

    ![confirmation](./img/reports-15.png)

    Within the popup, two buttons are available.

    1. **Cancel:** Click the `Cancel` button to abort the deletion process.

    2. **Delete:** Click the `Delete` button to confirm and proceed with the permanent deletion of the species record.

    Exercise caution and ensure the accuracy of the users' decision before confirming the deletion. This two-step process is designed to prevent accidental deletions and provide users with an opportunity to reconsider their actions.

![Species Report](./img/reports-14.png)

##### Report Columns

The Species Report includes the following columns:

* **Property Name**: The name of the property associated with the species data.

* **Scientific Name**: The scientific name of the species.

* **Common Name**: The common name of the species.

* **Year**: The specific year for which the data is recorded.

* **Group**: Information about the group to which the species belongs.

* **Total**: The total count of the species in the specified year.

* **Adult Males**: The count of adult male individuals within the species.

* **Adult Females**: The count of adult female individuals within the species.

* **Juvenile Males**: The count of juvenile male individuals within the species.

* **Juvenile Females**: The count of juvenile female individuals within the species.

* **Sub-Adult Males**: The count of sub-adult male individuals within the species.

* **Sub-Adult Females**: The count of sub-adult female individuals within the species.

##### Summary

The Species Report is a vital filter for reporting on various species. It provides comprehensive information on species-specific data, including counts, age groups, and associated property details. This report is essential for detailed analysis and management of species-related information.

### Summary

The reports table page is a comprehensive platform for exploring, analysing, and interacting with the user's data. With filters, column search, and data export options, the user has the tools necessary to customise their data view, find specific information, and export data in the format that suits their needs.
