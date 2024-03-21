a5 is a direct messenging chat that uses the dsu server.
When ran, it prompts the user to create a profile, or open
an existing one.

Profiles contain all previous message history for all
friends. When a file is loaded, a user may add a friend
the friend will appear on the left in the treeview, and
the user may now chat with them!

Chats are sent live, but there may be a short 2 second
delay. If a user has received new messages, they will
appear in the treeview when they next open the profile
(even messages from users that weren't on their friends
list previously!) 

The messages are sent using the DirectMessengerClass,
which has 3 methods (send, retrieve_new, and retrieve_all).
Retrieve_new is called every 2 seconds when the program is
running so that messages are updated often, making live chat
possible.

Have fun using the direct messenger!!!