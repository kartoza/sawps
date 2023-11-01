# Add Admin Table

## Activity

![Add Activity](./img/django-add-data-3.png)

1. **Form fields**: Form where user can input values for record.

    This table is used to store existing activity types e.g. `Unplanned/natural deaths`.

    * **Colour**: Used as color identifier in reports and charts. The default is black (`#000000`).
    * **Width**: Column width in the Activity Report.
    * **Export fields**: Used as export fields in Activity Report. The value should be an array/list, containing
    `Annual Population Per Activity` field to export. Currently available fields are:
        * founder_population
        * reintroduction_source
        * intake_permit
        * offtake_permit
        * translocation_destination

    This is an example of correct **Export fields** value:
    `["translocation_destination", "founder_population"]`

    Any update on this table will be reflected on the [Activity Report](../../user/manual/explore/reports.md).


3. **Save and add another**: Save current record, then redirect to a new page to add new record.

4. **Save and continue editing**: Save current record while still showing current record.

5. **Save**: Save current record, then redirect to Django Admin Table/record list.

## Group

![Group Permissions](./img/django-add-data-1.png)

1. **Permissions**: Available permission for the user. Admin can choose permission from the list and assign to the user.

2. **Arrow**: Using this arrow admin can move the permissions here and there.

3. **Plus icon**: Clicking on plus icon will allow admin to add new permission. Popup will open for creating new permission.

    ![Add Permission](./img/django-add-data-2.png)

    1. **Form Fields**: Form where user can input values for record.

    2. **Save**: Button to save permission.


4. **Choose All**: Button to choose all permissions and assign to user.

5. **Remove All**: Button to choose all permissions and remove from user.

6. **Save and add another**: Save current record, then redirect to a new page to add new record.

7. **Save and continue editing**: Save current record while still showing current record.

8. **Save**: Save current record, then redirect to Django Admin Table/record list.
