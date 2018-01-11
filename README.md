# Attendance and Timetabling System

This is the attendance and timetabling system for International House, the
University of Melbourne.

## Setup

1. Install Python v3.4.3 or greater.
2. Install dependencies using pip:

    ```
    $ pip install -r requirements.txt
    ```

3. Make your configurations in `attendance/config.py`.
4. Open `attendance/__init__.py` in a text editor.
5. Comment out the `init_db` function call on line 87.
6. Run the following commands to create and migrate the database:

    ```
    $ python manage.py db init
    $ python manage.py db migrate
    $ python manage.py db upgrade
    ```

7. Uncomment out line 87 as you did in step 5.

## Running the webserver

To run, use:

```
$ python manage.py runserver
```

The server is up at **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**.

### Setting up a timetable

Here is what you should to do to set up a timetable.

- Sign in as the administrator.
- Ensure your study period is set correctly under the `Admin` tab.
- Create a new timetable under `Manage` > `Timetable`. This should represent a year and semester and version. E.g., a name such as `2018-S1-v1` would represent the first-round timetable for 2018 Semester 1. Subsequent drafts would be set as `v2` and so on.
- Set the current timetable under the `Admin` tab to the one created above.
- Create timeslots under `Manage` > `Timeslots`, and whether or not they are preferred times
- Create rooms and indicate those which have projectors under `Manage` > `Rooms`.
- Map tutors and subjects and the total number of classes for each subject on the `Run Timetabler` tab.
- Select which subjects require projectors by clicking on a subject under `Manage` > `Subjects`, then indicate using the `Needs Projector` dropdown.

### Troubleshooting

Generally there is only one reason that there would not be able to create a timetable, which is that there are not sufficient availabilities for a particular tutor for their allocated classes.

This can be troubleshooted from the `Manage` > `Tutors` tab.
