# Data Upload Page Documentation

The Data Upload Page is a key component for managing and uploading the users data. This page provides an intuitive interface for adding new data and customising the users view. It also includes a map with interactive features to help the user visualize spatial data.

## Data upload

![Data upload](./img/panel-1.png)

1. **Search area**: The central feature of the Data Upload Page is the data search area, where the user can search for specific areas within the users dataset. This search field allows the user to enter keywords or details related to the users records to locate specific areas.

2. **Select property**: The Property Selection Dropdown is a vital tool for categorising the users data. User can choose from existing property categories to associate the users data with a specific property. This helps organise and categorise the users records effectively.

3. **Create a new property**: If the property the user want to associate the users data with does not exist in the dropdown, the user can create a new property. Click on the `CREATE A NEW PROPERTY` button to add a new property category. User will be prompted to enter a name and details for the new property, and it will be added to the dropdown for future use.

## Interactive Map

In the bottom left corner of the Data Upload Page, the user will find an interactive map that allows the user to visualize spatial data. The map provides several options:

## Map Visualisation

![Map Visualisation](./img/panel-2.png)

1. **Zoom In**: Click on the plus (+) sign to zoom in on the map for a closer view of specific areas.

2. **Zoom Out**: Click on the minus (-) sign to zoom out and get a broader view of the map.

3. **Dark/Light Mode**: Toggle between a dark and light mode by clicking on the moon and sun icons. This feature provides visual comfort based on the users preference.

4. **Print**: Click on the print icon to generate a printable version of the map for the users records or to share with others.

The map enhances the users ability to work with spatial data and provides valuable insights into the geographical aspects of the users records.

## Summary

The Data Upload Page is an essential tool for managing the users data, allowing the user to input new records, categorize them with properties, and visualize spatial data using the interactive map. Whether the user adding new information or searching for existing records, this page provides a user-friendly experience to help the user effectively handle the users data.

## Step 1

The Data Table Page serves as the central hub for viewing and interacting with the users data. This comprehensive platform offers various features to help the user explore, analyze, and manipulate the users dataset. To get started, the user will need to upload data, and the first step in this process involves providing property information using the Property Information Form.

## Property Information Form

![Property Information Form](./img/panel-3.png)

The Property Information Form is the initial stage of data upload. It's designed to capture essential details about the property being added to the dataset. Here is a breakdown of the form fields:

1. **Step 1**: First step of data upload.

2. **Property Name**: Enter the name of the property in the `Property Name` input field.

3. **Owner Name**: The `Owner Name` field is pre-filled with the default owner name.

4. **Owner Email**: Similar to the owner name, the `Owner Email` field is pre-filled with the default owner email.

5. **Open/Close System**: Select the open or close system for the property from the dropdown menu. This choice reflects the accessibility status of the property.

6. **Property Type**: Choose the property type from the `Property Type` dropdown menu. This classification helps categorize the property.

7. **Province**: Select the province or region where the property is located from the `Province` dropdown. This information is vital for geographic referencing.

8. **Organisation**: The `Organisation` displays the name of the organization.

9. **SAVE PROPERTY INFORMATION**: Once the user have filled in all the necessary details, click the `SAVE PROPERTY INFORMATION` button to store this information and proceed with the data upload process.

The map enhances the users ability to work with spatial data and provides valuable insights into the geographical aspects of the users records.

By completing the `Property Information Form`, the user establish a foundational record for the property in the dataset, which is essential for effective data management and analysis.

This step ensures that the users data is organized and ready for further processing within the data upload.

## Step 2

The second step of the data upload process on the Data upload involves working with Parcel ID and Parcel Type. This stage is crucial for adding detailed information related to parcels within the property.

## Parcel Details

![Parcel Details](./img/panel-4.png)

1. **Step 2**: Step 2 of data upload.

2. **Parcel ID**: The Parcel ID is a unique identifier for each parcel within the property.

3. **Parcel Type**: Parcel Type categorizes the parcels based on their purpose or characteristics.

4. **SELECT**: The `SELECT` button allows the user to choose specific parcels from the map.

5. **DIGITISE**: Clicking the `DIGITISE` button initiates the process of mapping parcel boundaries. This step is essential for geospatial data.

6. **UPLOAD**: The `UPLOAD` it is used for creating parcel boundaries using the supported formats: zip, json, geojson, gpkg, kml (CRS 4326).

7. **SAVE PROPERTY INFORMATION**: If the user need to update or modify property information, the user can click the `SAVE PROPERTY INFORMATION` button to make changes to the property-level information.

Completing Step 2 ensures that the users dataset is comprehensive and includes detailed information about individual parcels within the property. This data is essential for various analyses and property management tasks.

## Select parcel using select button

![Select button](./img/panel-5.png)

1. **Select parcel**: Zoom in the map until parcels are visible once the user able to see the parcels select parcels.

2. **Cancel**: User can cancel the selection of the parcel using this button.

3. **Save Boundary**: Click on `SAVE BOUNDARY` button to save the boundaries. After saving the boundary the user will be able to see the selected parcel id and its type.

## Select parcel using the digitise button

The `DIGITISE` button is a powerful tool that allows the user to digitise parcel boundaries. When the user click the `DIGITISE` button, the user will see a set of options on the left top of the map, giving the user full control over the digitisation process. These options are essential for mapping out parcel boundaries accurately.

### Digitisation Options

![Digitisation Options](./img/panel-6.png)

1. **Digitise**: By click on `DIGITISE`  button, the user will see a set of options on the left top of the map to digitise the boundaries.

2. **Polygon tool**: By clicking on the `Polygon tool Icon` the user can choose a specific area on the map. This selection is used to outline the boundaries of the parcel the user digitising.

3. **Delete Icon**: The `Delete Icon` is for removing or deleting any selected area that the user no longer need. This option allows the user to make adjustments as the user digitise.

4. **Save Icon**: Click on the `Save Icon` to save the selected area as a digitised parcel boundary. This is a critical step to preserve the boundaries the user have defined.

5. **Cross Icon**: The `Cross Icon` is used to cancel or discard any digitisation progress if the user need to start over or abandon the current selection.

6. **Digitised parcel**: Digitised parcel is shown.

7. **Save boundary**: After the user have successfully digitised and outlined the parcel boundary using the above options, the user can finalise the process by clicking the `SAVE BOUNDARY` button. This saves the digitised boundary and incorporates it into the users property's data.

By utilising the digitisation options, the user can accurately define parcel boundaries, which is essential for geospatial data and mapping applications. This tool provides the user with the flexibility to create precise boundaries and make adjustments as needed during the digitisation process.

## Upload parcel using the upload data button

The `UPLOAD` button is a pivotal element of the `DATA UPLOAD`, allowing the user to upload essential data for parcel boundaries. By clicking this button, the user initiate the data upload process, which includes defining parcel boundaries and saving them. Here is a step-by-step guide on how to use this feature:

### Uploading Data

![Upload Popup](./img/panel-7.png)

1. **Upload**: Click on the `UPLOAD` button, and a popup window will open, providing the user with options for uploading data.

The popup window includes the following components:

2. **Browse**: Click on the `Browse` and select the file or files the user want to upload. Supported formats include zip, json, geojson, gpkg, kml (CRS 4326). These files typically contain geospatial data, and the user will use them to define parcel boundaries.

3. **Upload Files**: After the user have selected the appropriate files, click the `Upload Files` button to begin the data upload process. This action will upload and process the selected data.

4. **Cancel**: If the user decide not to proceed with the data upload, the user can click the `Cancel` button to close the popup window.

5. **SAVE BOUNDARY**: By clicking the `SAVE BOUNDARY` button. This action will store the boundary and incorporate it into the users property's dataset.

By following these steps, the user can effectively upload data, define parcel boundaries, and save them within the `DATA UPLOAD`. This feature is crucial for geospatial data and mapping applications, ensuring the users data is accurate and complete.

### After selecting the parcel

![Upload Popup](./img/panel-8.png)

1. **Parcel ID**: The Parcel ID is a unique identifier for each parcel within the property.

2. **Parcel Type**: Parcel Type categorizes the parcels based on their purpose or characteristics.

3. **Delete icon**: This delete icon allows the user to delete the perticuler parcel detail.

## Step 3

Step 3 of the data upload process is a crucial phase that allows the user to upload species population data. In this step, the user will find two buttons for uploading the users data, along with an option to download a template for the users convenience. Additionally, there is a button to update property boundaries, which leads the user to Step 2 where the user can make property boundary modifications.

### Data Upload step 3

![Step 3](./img/panel-9.png)

1. **Step 3**: Step 3 of data upload.

2. **Online Form**: Click on the `ONLINE FORM` button to access the online data upload form. This option is ideal for manually entering data into a user-friendly interface. Follow the provided prompts to input the users species population data.
![Online form](./img/panel-10.png)
click on the [Online form](./online-form.md) to see the detailed documentation of online form.

3. **Download Template**: Click on the `DOWNLOAD TEMPLATE` button to obtain a blank template that the user can use as a starting point for entering the users species population data. This template is designed to assist the user in organizing the users data correctly.

4. **Upload Template**: Use the `UPLOAD DATA` button to upload a pre-prepared template containing the users species population data. Templates are useful for bulk data uploads or when the user have data formatted in a specific way. Ensure the users template adheres to the required format and guidelines for a successful upload.
![Upload template](./img/panel-11.png)
click on the [Upload template](./template-upload.md) to see the detailed documentation of template upload.

#### Updating Property Boundary

5. **Update Property Boundary**: By clicking the `UPDATE PROPERTY BOUNDARY` button, the user will be directed to Step 2 of the data upload process. In this step, the user can modify property boundaries.

6. **Property Information Display**: A section is provided on this page to display information about the property. This information is for reference and provides details about the property related to the data the user uploading.

7. **Selected property**: The property is highlighted on the map to make it easy for the user to pinpoint the area.

## Summary

Step 3 of the data upload process provides multiple options for uploading species population data, allowing flexibility in how the user input his information. User can choose between an online form or uploading a prepared template. Additionally, the availability of a downloadable template simplifies data organization. If needed, the user can update property boundaries by clicking the dedicated button, which takes the user to Step 2 where the user can make the necessary adjustments while visually identifying the selected property on the map.
