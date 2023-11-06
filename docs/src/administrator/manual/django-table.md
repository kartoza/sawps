# Django Tables

## Activities Table

![Django Admin Table](./img/django-table-1.png)

1. **Add button**: Clicking on this button will allow administrators to add a new record in the table. Clicking [here](django-add-data.md) will redirect users to the add data record documentation.

2. **Search**: Feature to allow for searching of a specific object in the table using keywords.

3. **Toggle select records**: Checkbox to select/deselect records.

4. **Action**: Administrators can choose the action from this dropdown and then perform it on a selected object.

5. **Go**: Clicking on this button will allow administrators to perform the selected option on the selected object.

6. **Objects**: Available objects containing records. Administrators can see the details of the object by clicking on the link (i.e. the object name).

## Group Table

![Group Table](./img/django-table-2.png)

This table is used to store existing user groups, that will affect the available options in the [Report](../../user/manual/explore/reports.md).

Administrators can assign a user to groups in the User Table.

1. **Toggle sorting**: Clicking on this icon will allow administrators to toggle the displayed order of the data.

2. **Add Group**: Clicking on the `ADD GROUP` button will allow administrators to add a new group. Click [here](django-add-data.md) to see detailed documentation about adding a new group.

3. **Edit Record**: Clicking on the object will allow administrators to change/edit a particular record. Click [here](django-change-data.md) to see detailed documentation about editing a group.

## User Table

![User Table](./img/django-table-4.png)

The user table within the Django Admin interface allows administrators to manage user-related tasks efficiently.

1. **Add User**: Clicking on the `ADD USER` button allows administrators to add a new user. Click on [add user](django-add-data.md) to see detailed documentation on adding a new user.

2. **Filter**: Available filters to filter the records of the user table.

    - ![Filters](./img/django-table-5.png)

    1. **Clear All Filters**: Clicking on the `clear all filters` allows administrators to clear all the filters.

    2. **Filter Field**: The names of the filter field and attributes for filtering the records.

3. **Search Functionality**: The administrators can search the records using the search functionality.

4. **User Table**: The user table with records.

5. **Edit User**: Clicking on the object allows the administrators to change or edit a particular record. Click [here](django-change-data.md) to view detailed documentation on editing a user.

## TOTP(Time-based One-Time Passwords) Device

![TOTP Device](./img/django-table-6.png)

This table is used for storing, generating, and deleting the TOTP device.

1.  **TOTP Table**: The table displays the record for the TOTP device.

2.  **QRCode**: The administrator can view the QRCode of the TOTP device by clicking on the `qrcode` link.

    - ![QRCode](./img/django-table-7.png)
    1. **QRCode**: Displays QRCode.
    2. **URI**: URI(Uniform Resource Identifier) for configuring TOTP.

3. **Add TOTP Device**: The administrator can add a TOTP device by clicking on the `ADD TOTP DEVICE` button. Click on the [add TOTP device](./django-add-data.md) to view detailed documentation about adding a new TOTP device.

4. **Edit TOTP Device**: The administrator can edit the TOTP device for that particular object by clicking on the object. Click on the [edit TOTP device](./django-change-data.md) to view detailed documentation about editing a TOTP device.
