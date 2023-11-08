# Django Admin Page Documentation

## Description

The Django Admin is the central hub to create, read, update, or delete your data. Only user with staff status can enter the admin page.

## Heading to Django Admin

_![Django Admin](./img/admin-1.png)_

1. Click on your profile icon, then click **Django Admin**.

## Django Admin Layout

The Welcome page will be the first thing that administrators see. It typically displays a welcome message and provides an overview of the available actions and options within the administration panel.

![Django Admin Layout](./img/admin-2.png)

In the top right corner of the administration panel, administrators will find a section that usually displays their username. In this section, administrators have the following options:

1. **Welcome**: Displays welcome with the administrator's name.

2. **View Site**: Clicking on this option will take administrators to the `SAWPS` website.

3. **Change Password**: Clicking on this option allows administrators to change their administration password. Administrators will be prompted to provide their current password and then set a new one.

    ![Change Password](./img/admin-8.png)

    **Input Fields**

    1. **Old Password**: In this field, administrators should provide the current password associated with their account. This is a mandatory field.

    2. **New Password**: In this field, administrators should enter the new password they want to set for their account. The password should meet the following criteria:

    * The password can't be too similar to other personal information.
    * The password must contain at least 12 characters.
    * The password can't be a commonly used password.
    * The password can't be entirely numeric.
    * The password should include the following:
        * Numeric character
        * Uppercase letter
        * Special character (@#%;)

    * Ensure that the new password adheres to these requirements.

    3. **New Password Confirmation**: Re-enter the new password in this field to confirm it. It should match the password entered in the `New Password` field.

    4. **Change My Password Button**: Once administrators have filled in the required information, they can click the `CHANGE MY PASSWORD` button to submit the form. If all the input is valid and the new password meets the criteria, the password for their account will be updated.

After successfully changing the password, the administrator will receive a confirmation message indicating that the password has been updated.

4. **Log Out**: Clicking on this option will log the administrator out of the administration panel and return them to the login page.

    ![Logout admin page](./img/admin-9.png)

    1. **Log in again**: Clicking this option will open the login page.

5. **Recent Actions**: The `Recent Actions` section is located on the right side of the administration panel and provides a list of recent actions that have been performed within the administration interface. These actions may include additions, deletions, or changes to data in the project. Clicking on any of the available links will take an administrator to the details of the recent action.

6. **Site Administration**: This section provides links to various models and apps registered with the administration panel. It serves as the primary navigation point for managing a project's data. Clicking on any of the available links will take an administrator to the respective model's management page.

7. **Add**: This button is used to create a new item for the associated model. Clicking on `Add` link will open a form where administrators can enter the details of the new record.

8. **Change**: This button is used to edit an existing item from the list. When administrators click the `Change` button, they will be redirected to a page where they can see all the associated data for that model and can select the data to change.

* **Table**: To see data in a table, click on the table name.

## Django Admin Table

![Django Admin Table](./img/admin-11.png)

1. **Table Name**: Clicking on the table name will allow administrators to see the table name.

2. **Table**: Displays the table with the data.

* For more information, click [here](django-table.md) to see more in-depth tables documentation

* For more information, click [here](django-add-data.md) to see how to add new data.

* For more information, click [here](django-change-data.md) to see how to edit data.
