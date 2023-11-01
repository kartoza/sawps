# Django Admin Page Documentation

## Description

The Django Admin is the central hub to create, read, update, or delete your data. Only user with staff status can enter the admin page.

## Heading to Django Admin

_![Django Admin](./img/admin-1.png)_

1. Click on your profile icon, then click **Django Admin**.

## Django Admin Layout

The Welcome page will be the first thing user see. It typically displays a welcome message and provides an overview of the available actions and options within the admin panel.

_![Django Admin Layout](./img/admin-2.png)_

In the top right corner of the admin panel, user will find a section that usually displays user's username. In this section, user have the following options:

1. **Welcome**: Displays welcome with admin name.

2. **View Site**: Clicking on this option will take user to the `SAWPS` website.

3. **Change Password**: Clicking on this option allows user to change user's admin password. User will be prompted to provide your current password and set a new one.

    ![Change Password](./img/admin-8.png)

    **Input Fields**

    1. **Old Password**: In this field, user should provide the current password associated with the user account. This is a mandatory field.

    2. **New Password**: In this field, user should enter the new password user want to set for the user account. The password should meet the following criteria:

    * Your password can't be too similar to your other personal information.
    * Your password must contain at least 12 characters.
    * Your password can't be a commonly used password.
    * Your password can't be entirely numeric.
    * Your password should include the following:
    * Numeric character
    * Uppercase letter
    * Special character (@#%;)

    * Ensure that the new password adheres to these requirements.

    3. **New Password Confirmation**: Re-enter the new password in this field to confirm it. It should match the password entered in the `New Password` field.

    4. **Change My Password Button**: Once user have filled in the required information, click the `CHANGE MY PASSWORD` button to submit the form. If all the input is valid and the new password meets the criteria, the password for the user account will be updated.

After successfully changing the password, user will receive a confirmation message indicating that the password has been updated.

4. **Log Out**: Clicking on this option will log user out of the admin panel and return user to the login page.

    ![Logout admin page](./img/admin-9.png)

    1. **Log in again**: Clicking this option will open login page.

5. **Recent Actions**: The `Recent Actions` section is typically located on the right side of the admin panel and provides a list of recent actions that have been performed within the admin interface. These actions may include additions, deletions, or changes to data in your project. Clicking on any of the available links will take user to the detail of recent action.

6. **Site Administration**: Site Administration this section provides links to various models and apps registered with the admin panel. It serves as the primary navigation point for managing your project's data. Clicking on any of the available links will take user to the respective model's management page.

7. **Add**: This button is used to create a new item of the associated model. Clicking on it will open a form where you can enter the details of the new item.

8. **Change**: This button is used to edit an existing item from the list. When user click the `Change` button user will be redirected to a page where user can see all the associate data of that model and can select data to change.

* **Table**: To see data in a table, click on the table name.

## Django Admin Table

![Django Admin Table](./img/admin-11.png)

1. **Table Name**: Clicking on the table name will allow user to see table.

2. **Table**: Displays the table with the data.

* Click on the [table](django-table.md) to see the tables documentation

* Click on the [add](django-add-data.md) to see how to add new data.

* Click on the [edit](django-change-data.md) to see how to edit data.
