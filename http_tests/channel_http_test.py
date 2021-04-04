import pytest
import requests
import json
from src.config import url
from src.other import SECRET
import jwt

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
allMems = 'all_members'
Name    = 'name'
dmName  = 'dm_name'
fName   = 'name_first'
lName   = 'name_last'
chans   = 'channels'
token   = 'token'
dmID    = 'dm_id'
handle  = 'handle_string'
ownMems = 'owner_members'

#* Fixture that clears and registers the first user
@pytest.fixture
def user1():
    requests.delete(f"{url}clear/v1")    
    response = requests.post(f"{url}auth/register/v2", json={
        "email": "first@gmail.com",
        "password": "password",
        "name_first": "User",
        "name_last": "1"
    })
    return response.json()

#* Fixture that registers a second user
@pytest.fixture
def user2():
    response = requests.post(f"{url}auth/register/v2", json={
        "email": "second@gmail.com",
        "password": "password",
        "name_first": "User",
        "name_last": "2"
    })
    return response.json()

#* Fixture that registers a third user
@pytest.fixture
def user3():
    response = requests.post(f"{url}auth/register/v2", json={
        "email": "third@gmail.com",
        "password": "password",
        "name_first": "User",
        "name_last": "3"
    })
    return response.json()

#* Fixture that registers a fourth user
@pytest.fixture
def user4():
    response = requests.post(f"{url}auth/register/v2", json={
        "email": "fourth@gmail.com",
        "password": "password",
        "name_first": "User",
        "name_last": "4"
    })
    return response.json()

#* Fixture that returns a JWT with invalid u_id and session_id
@pytest.fixture
def invalid_token():
    return jwt.encode({'session_id': -1, 'user_id': -1}, SECRET, algorithm='HS256')

def test_http_channel_invite(user1, user2, user3):
    
    responseChannel = requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": 'Channel1',
        "is_public": True}
    )
    #* Test 1: Invite user2 into channel1 should be successful
    channel1 = responseChannel.json()
    requests.post(f"{url}channel/invite/v2", json={
        "token": user1[token],
        "channel_id": channel1[cID],
        "u_id": user2[AuID]}
    )
    response = requests.get(f"{url}channel/details/v2", params={
        'token': user1[token],
        'channel_id': channel1[cID]}
    )
    details = response.json()
    assert {
        fName: 'User', 
        lName: '2', 
        'email': "second@gmail.com", 
        'handle_str': "user2",
        uID: user2[AuID],
    } in details[allMems]

    #* Test 2: Channel id not valid raises inputerror
    response2 = requests.post(f"{url}channel/invite/v2", json={
        "token": user1[token],
        "channel_id": -1,
        "u_id": user2[AuID]}
    )

    assert response2.status_code == 400

    #* Test 3: user id not valid raises inputerror
    response3 = requests.post(f"{url}channel/invite/v2", json={
        "token": user1[token],
        "channel_id": user1[token],
        "u_id": -1}
    )

    assert response3.status_code == 400

    #* Test 4: user not in chnanel raises accesserror
    response4 = requests.post(f"{url}channel/invite/v2", json={
        "token": user3[token],
        "channel_id": channel1[cID],
        "u_id": user2[AuID]}
    )

    assert response4.status_code == 403

def test_http_channel_details(user1, user2):

    responseChannel = requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": 'Channel1',
        "is_public": True}
    )
    channel1 = responseChannel.json()

    #* Test 1: expected channel details
    expected = {'name': "Channel1",
        'is_public': True, 
        'owner_members':[{
            'u_id': user1[AuID],
            'name_first': "User",
            'name_last': '1',
            'email': 'first@gmail.com',
            'handle_str': 'user1',
        }],
        'all_members':[{
            'u_id': user1[AuID], 
            'name_first': "User",
            'name_last': '1',
            'email': 'first@gmail.com',
            'handle_str': 'user1',
        }]
    }

    responseUser = requests.get(f"{url}channel/details/v2", params = {'token': user1[token], 'channel_id': channel1[cID]})

    assert responseUser.json() == expected

    #* Test 2: InputERRor when, channel id not a valid id
    response1 = requests.get(f"{url}channel/details/v2", params = {'token': user1[token], 'channel_id': -1})

    assert response1.status_code == 400

    #* Test 3 : AccessError when user not in channel
    responseUser2 = requests.get(f"{url}channel/details/v2", params = {'token': user2[token], 'channel_id': channel1[cID]})

    assert responseUser2.status_code == 403


def test_http_channel_leave(user1, user2, user3, user4):
    pass

def test_http_channel_join(user1, user2, user3, user4):
    c1 = requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": "TrumpPence",
        "is_public": True
    })
    c2 = requests.post(f"{url}channels/create/v2", json={
        "token": user2[token],
        "name": "BidenHarris",
        "is_public": False
    })
    requests.post(f"{url}channel/join/v2", json={
        "token": user3[token],
        "channel_id": c1.json()['channel_id']
    })
    assert requests.get(f"{url}channel/details/v2", params={'token': user3[token], 'channel_id': c1.json()['channel_id']}).json() == {
        "name": "TrumpPence",
        "is_public": True,
        "owner_members": [
            {
                uID: user1[AuID],
                'email': "first@gmail.com",
                fName: "User",
                lName: "1",
                'handle_str': "user1"
            }
        ],
        "all_members": [
            {
                uID: user3[AuID],
                'email': "third@gmail.com",
                fName: "User",
                lName: "3",
                'handle_str': "user3"
            }
        ]
    }

def test_http_channel_addowner(user1, user2, user3, user4):

    responseChannel = requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": 'Channel1',
        "is_public": True}
    )
    channel1 = responseChannel.json() 

    #* Test 1: Succesfully add owner

    requests.post(f"{url}channel/addowner/v1", json={
        "token": user1[token],
        "channel_id": channel1[cID],
        "u_id": user2[AuID]}
    )

    response = requests.get(f"{url}channel/details/v2", params={
        'token': user1[token],
        'channel_id': channel1[cID]}
    )
    details = response.json()

    assert {
        uID: user2[AuID],
        fName: 'User',
        lName: '2',
        'email': 'second@gmail.com',
        'handle_str': 'user2',
    } in details[allMems]
    assert {
        uID: user2[AuID],
        fName: 'User',
        lName: '2',
        'email': 'second@gmail.com',
        'handle_str': 'user2',
    } in details[ownMems]

    #* Test 2: Input error for invalid Channel iD

    response2 = requests.post(f"{url}channel/addowner/v1", json={
        "token": user1[token],
        "channel_id": -1,
        "u_id": user3[AuID]}
    )

    assert response2.status_code == 400

    #* Test 3: Input error when user is already an owner
    response3 = requests.post(f"{url}channel/addowner/v1", json={
        "token": user1[token],
        "channel_id": channel1[cID],
        "u_id": user2[AuID]}
    )

    assert response3.status_code == 400

    #* Test 4: Access error when user not owner or owner of channel

    response4 = requests.post(f"{url}channel/addowner/v1", json={
        "token": user3[token],
        "channel_id": channel1[cID],
        "u_id": user4[AuID]}
    )

    assert response4.status_code == 403

def test_http_channel_removeowner(user1, user2, user3, user4):
    
    responseChannel = requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": 'Channel1',
        "is_public": True}
    )
    channel1 = responseChannel.json() 
    #* Test 1 : see if successfully removed member from owner not all members
    requests.post(f"{url}channel/addowner/v1", json={
        "token": user1[token],
        "channel_id": channel1[cID],
        "u_id": user2[AuID]}
    )

    requests.post(f"{url}channel/removeowner/v1", json={
        "token": user2[token],
        "channel_id": channel1[cID],
        "u_id": user1[AuID]}
    )

    response = requests.get(f"{url}channel/details/v2", params={
        'token': user2[token],
        'channel_id': channel1[cID]}
    )
    details = response.json()

    assert {
        uID: user1[AuID],
        fName: 'User',
        lName: '1',
        'email': 'first@gmail.com',
        'handle_str': 'user1',
    } not in details[ownMems]
    assert {
        uID: user1[AuID],
        fName: 'User',
        lName: '1',
        'email': 'first@gmail.com',
        'handle_str': 'user1',
    } in details[allMems]

    #* Test 2: Input Error for channel ID not valid

    requests.post(f"{url}channel/addowner/v1", json={
        "token": user2[token],
        "channel_id": channel1[cID],
        "u_id": user1[AuID]}
    )
    response2 = requests.post(f"{url}channel/removeowner/v1", json={
        "token": user1[token],
        "channel_id": -1,
        "u_id": user2[AuID]}
    )

    assert response2.status_code == 400

    #* Test 3: Input error when user is not an owner
    response3 = requests.post(f"{url}channel/removeowner/v1", json={
        "token": user1[token],
        "channel_id": channel1[cID],
        "u_id": user3[AuID]}
    )

    assert response3.status_code == 400

    #* Test 4: Input error when user is only owner
    requests.post(f"{url}channel/removeowner/v1", json={
        "token": user2[token],
        "channel_id": channel1[cID],
        "u_id": user1[AuID]}
    )

    response4 = requests.post(f"{url}channel/removeowner/v1", json={
        "token": user2[token],
        "channel_id": channel1[cID],
        "u_id": user2[AuID]}
    )

    assert response4.status_code == 400

    #* Test 5: Access Error when user is not owner of dreams
    responseChannel2 = requests.post(f"{url}channels/create/v2", json={
        "token": user2[token],
        "name": 'Channel2',
        "is_public": True}
    )
    channel2 = responseChannel2.json() 
    requests.post(f"{url}channel/addowner/v1", json={
        "token": user2[token],
        "channel_id": channel2[cID],
        "u_id": user1[AuID]}
    )
    response5 = requests.post(f"{url}channel/removeowner/v1", json={
        "token": user4[token],
        "channel_id": channel2[cID],
        "u_id": user2[AuID]}
    )

    assert response5.status_code == 403
