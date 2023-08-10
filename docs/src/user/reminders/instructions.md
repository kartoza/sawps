# Reminders Feature

## Description
The Reminders feature enables a user or organisation to do the following:
*   1 organisation: set a reminder for everyone within the organisation.
*   2 user: set a personal reminder
*   Editing a reminder. Changing its state from active, draft and passed or altering other details etc.
*   deleting a reminder.
*   The reminder set is sent via email and also the user is notified via the platform.

Other functionalities offered on the Reminders Page:
*	Searching specific reminders.
*	Searching by filtering.
*	Pagination.
*   organisation: viewing all reminders set by different users who have the role to create reminders for all members of that specific organisation.
*   user: viewing personal reminders.



![instr_reminders_page](../img/reminders_page.png)


## 1 Navigation Link
Under the profile section a tab for reminders is available. When clicked renders the reminders page.
## 2 Add Reminder
When clicked will present the user with the form to fill for the reminder they intend to create.

![instr_add_reminder](../img/add_reminder.png)

*   __1 Title__: The user should provide the reminder title.
*   __2 Date and Time__: the user should schedule the reminder.
*   __3 Reminder__: the user should provide the description of the reminder.
*   __4 Reminder Type__: Based on the user role within that specific organisation the user is able to specify if the reminder is for all organisation members or it's a personal reminder.
*   __5 Add button__: when clicked creates the reminder.

## 3 Search box
Allows the user to search for a specific reminder. The search looks for keywords within the reminder and the title.
## 4 Filter
The user is able to filter by title or reminder. This refines the search to only return reminders containing the providing keywords specifically in the filter provided.
## 5 Reminder
Clicking on any reminder will cause the pop up modal for editing the reminder to appear.

![instr_edit_reminder](../img/edit_reminder.png)

*   __1 Title__: the user can change the reminder title.
*   __2 Date and Time__: the user can change scheduled time for the reminder.
*   __3 Reminder__: the user can change the description of the reminder.
*   __4 Reminder Type__: Based on the user role within that specific organisation the user is able to specify if the reminder is for all organisation members or if it's a personal reminder.
*   __4 Reminder Status__: the user is able to change the state of the reminder. If set to active the reminder is still scheduled, if set to draft the reminder is on pause, if set to passed the reminder will not be moved to the notifications section but no email is sent.
*   __5 Save button__: when clicked saves the new edited details.

## 6 Delete icon
The user can delete their reminders.
Organisation Managers can delete organisation reminders.
When the delete icon is clicked a pop up modal is evoked prompting if the user is sure of the actions they wish to take.

![instr_delete_reminder](../img/delete_reminder.png)

*   __1. Delete Confirmation Title__: Title pointing to what the modal is.
*   __2. Delete Button__: when clicked deletes the reminder.
