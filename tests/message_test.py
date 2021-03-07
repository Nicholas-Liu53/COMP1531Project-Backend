import pytest
from src.message import message_send_v1, message_remove_v1, message_edit_v1
from src.error import InputError, AccessError
import src.channel, src.channels, src.auth

# message_send_v1
# When message is >1000 characters, InputError is raised
# When authorised user is not part of the channel that they are trying to post in, AccessError is raised
# After the function is sucessfully run, ensure that the return value is correct

# message_edit_v1
# When message is >1000 characters, InputError is raised
# If there are no messages with matching message_id, InputError is raised
# Ownership permission tests:
    # Owner of Dreams should be able to edit anything
    # Owner of channels should be able to edit anything in channels they own
    # Non-owner of channels should only be able to edit their own messages
# Test if a message has been edited successfully?

# search_v1
# When query_str is >1000 characters, InputError is raised
# Test that users can only see messages in channels that they have joined
    # Test if a user who has joined no channels can see any messages
