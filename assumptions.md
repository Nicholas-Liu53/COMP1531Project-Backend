#########################################################################################
###                                                                                   ###
###                                    Assumptions                                    ###
###                                                                                   ###
#########################################################################################

#########################################################################################
###                                                                                   ###
###  W13B Cactus - Ethan Kwong, Jeffrey Meng, Nicholas Lam, Nicholas Liu, Vincent Le  ###
###                 z5308489     z5311921      z5310204      z5310207      z5310000   ###
###                                                                                   ###
#########################################################################################

In src/auth.py,
    For auth_register_v1:
        - Apart from "@" and " ", all characters can be in valid names
            e.g.      "Kim Jong-un"        is a valid name
                        "Ja'mie"           is a valid name
                 "Shai Gildrous-Alexander" is also a valid name
                       "X Æ A-12"          is also a valid name
        - Aside from the length of the password is greater than 5, no other requirements 
          for a valid password
        - Apart from "@" and " ", all characters may appear in handle strings
    For auth_login_v1:
        - Nothing much

In src/channel.py,
    For channel_messages_v1:
        - messages_send_v1 has been properly implemented 
           (even though we still in iteration one)
    For channel_invite_v1:
        - Regardless of it is a private or public channel, as long as the authorised user
           (i.e. the user inviting) is in the channel, the invitee will join the channel
        - If the invitee is already in the channel, then nothing happens 
           (i.e. no Exception raised, or anything printed out)
    For channel_details_v1:
        - Only prints out public details of a channel (see more in channel_join_v1)
           (i.e. ignores passwords of users in the channel)
    For channel_join_v1:
        - Assumes that the id being entered is of a member that isn't already in the 
          channel

In src/channels.py,
    For channels_create_v1:
        - At this stage, can't delete a channel from the database
        - The user who creates the channel automatically joins it and becomes the
          owner member
    For channels_list_v1:
        - If the list is empty, you don't return an empty dictionary inside the list
    For channels_listall_v1:
        - If the list is empty, you don't return an empty dictionary inside the list        