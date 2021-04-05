*************************************************************************************************************************************************
** Prior discussion of agenda was done through Facebook Messenge so meeting consisted mainly of co-coding and helping each other finalise code **
*************************************************************************************************************************************************

Iteration 2 begins here:
8/3/21
Attendance: Nick Liu, Ethan Kwong, Jeffrey Meng, Vincent Le and Nick Lam
    Meeting to go through spec together
    Discuss branching system and any changes to be made from iteration 1
    More progress checks 
    Functionalise code that all members can use to make their functions more ‘clean’
    Universal legend for all files

17/3/21 
Attendance: Nick Liu, Ethan Kwong, Jeffrey Meng, Vincent Le and Nick Lam
    Began discussion of iteration 2, delegations of task and how it would work holistically 
    Changing iteration 1: 
        Old functions auth_register_v1→needs to redo the implementation of user_ids
        Old function channel_join_v1 → needs to redo the implementation of channel_ids 
        Everyone those the flask wrap around for the functions they implemented in iteration 1
    Iteration 2 functions:
        Nick Liu - message/send/v2, message/edit/v2, message/remove/v2, channel/leave/v1
        Nick Lam / Ethan Kwong - dm/details/v1, dm/listv1, dm/create/v1, dm/remove/v1, dm/invite/v1, dm/leave/v1, dm/messages/v1, message/senddm/v1
        Vincent Le - message/share/v2, admin/permission/change/v1, channel/addowner/v1, channel/removeowner/v1
        Jeffrey Meng - user/profile/v2, user/profile/setname/v2, user/profile/setemail/v2, user/profile/sethandle/v1, user/all/v1, admin/user/remove/v1
    Began discussing how to implement a data structure to implement the notifications function
        Notifications should be placed within the user data structure
        Each user dictionary should contain a key named notifications containing a list 
        Each time there is a message within a dm or channel the user is a part of, this information will be inserted into the notification data structure within their user dictionary
        When notifications is called, the function returns the first 20 notifications within the list from the back

19/3/21 
Attendance: Nick Liu, Ethan Kwong, Jeffrey Meng, Vincent Le and Nick Lam
    Group meeting where we fixed all pylint errors in order to pass the pipeline. Discussed different tests that would enable use to increase the coverage of our code

Feedback from Xiaocong (Gary)
    Fixtures
    Need comments in testing files
    Labels for taskboard


Release of Results - Iteration 1 (20/03/21)
(list of things to fix for next iteration)
    channels_list and channels_listall
        Change return dictionary key to ‘name’ instead of ‘channel_name’

21/3/21 
Attendance: Nick Liu, Ethan Kwong, Jeffrey Meng, Vincent Le and Nick Lam
Discuss: where to put HTTP functions
Set due date for finishing 80% functions- 28/3/21

28/3/21
Attendance: Nick Liu, Ethan Kwong, Vincent Le and Nick Lam
    Went through dm functions as a group
    Ethan, Nick Lam pair programmed message/senddm and dm/messages

29/3/21
Attendance: Nick Liu, Jeffrey Meng, Vincent Le and Nick Lam
    Helped Jeffrey Meng finish his functions
    Merged his work into master
    Others bug fixed their functions

31/3/21
Attendance: Nick Liu, Ethan Kwong, Vincent Le and Nick Lam
    Fixed up pylint of functions
    Deliverable: Fix up coverage of each person's function
    Discussed notifications_get and search
    Notifications: New list containing dictionary- 1st key- user_id, 2nd key- notification
    Within notification- containing channel id, dm id and message
    Message send, dm send, and share need a tagging function
    Standups where each member talked about their desired method of storing notifications
        The structure the group decided on was to use a dictionary of dictionaries where each key was a u_id corresponding to a list of notifications


3/4/21
Attendance: Nick Liu, Ethan Kwong, Jeffrey Meng, Vincent Le and Nick Lam
    Implemented everyone’s base functions 
    Began discussing HTTP testing and functions
        Each person do their functions http testing
        Set date to finish by next meeting 4/4
    Discussion of persistence 
        JSON vs Pickle
        Weighing up pros and cons of each
        Decided to go with JSON

4/4/21
Attendance: Nick Liu, Ethan Kwong, Jeffrey Meng, Vincent Le and Nick Lam
    Continued working and coding through http tests together 
    Persistence and coverage checkup 
        Progress check
    Discussed everyone's expected deadlines to ensure that iteration 2 would be finished on time

5/4/21
Attendance: Nick Liu, Ethan Kwong, Jeffrey Meng, Vincent Le and Nick Lam
    Finalised everyone’s http tests and did final merge for submission of iteration 2
        Finished working on persistence branch too
    Ensured pylint, coverage and pytests were all passing
    Reread through comments and doc strings to ensure quality
    Pointed out that spec wanted ‘handle_str’ and not ‘handle_string’
        Changed all instances of ‘handle_string’ to ‘handle_str’ and merged it into master
    Wrote up assumptions document
    Discussed things to work on for iteration 3

More details can be found at:
    https://docs.google.com/document/d/1GIzf-JhN33HH3dEVvG0U6j_GUUdKqp4hqIfOrDVuXBA/edit?usp=sharing 
