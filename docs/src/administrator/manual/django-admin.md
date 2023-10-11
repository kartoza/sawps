# Django Admin Page Documentation

## Description

The Django Admin is the central hub to create, read, update, or delete your data. Only user with staff status can enter the admin page.

## Heading to Django Admin
_![Django Admin](./img/admin-1.png)_

1. Click on your profile icon, then click **Django Admin**.

## Django Admin Layout
_![Django Admin Layout](./img/admin-2.png)_

1. **Application**: Application or module that exist in this site.
2. **Table**: Table or model, where the data is stored.
3. **Recent Actions**: List of activities recently happened in admin site.

To data in a table, click on the table name.

## Django Admin Table
_![Django Admin Table](./img/admin-3.png)_

1. **Table records**: Show the first page of table records. 
2. **Count of selected records**: Shows the number of selected records.
3. **Toggle select records**: Checkbox to select/deselect records.
4. **Add new records**: Button to add a new record.

To edit a record, click on the record.

## Django Admin Form
_![Django Admin Form](./img/admin-4.png)_

1. **Form fields**: Form where we can input values for our record. 
2. **Delete button**: Delete currently opened record. It will take you to confirmation page.
3. **Save and add another**: Save current record, then redirect to a new page to add new record.
4. **Save and continue editing**: Save current record while still showing current record.
5. **Save**: Save current record, then redirect to Django Admin Table/record list.
6. **History**: Button to see actions applied to current record.

## Activities Table

_![Activities Table](./img/admin-5.png)_

This table is used to store existing activity types e.g. `Unplanned/natural deaths`.

1. **Colour**: Used as color identifier in reports and charts.
2. **Export fields**: Used as export fields in Activity Report. The value should be an array/list, containing 
`Annual Population Per Activity` field to export. Currently available fields are:
    * founder_population
    * reintroduction_source
    * intake_permit
    * offtake_permit
    * translocation_destination

This is an example of correct **Export fields** value:
`["translocation_destination", "founder_population"]`
