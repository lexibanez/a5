"""
This module contains the GUI components for a Direct Messaging Chat
application.

It uses the tkinter library for the GUI and the ds_messenger and ds_client
modules for the application's messaging functionality. The main class in this
module is Body, which represents the main chat window. It contains methods for
drawing the window, selecting a chat, and updating the chat display.

This module also contains several other classes for different parts of the GUI,
such as the login window and the contact list.
"""

import json
import time
import tkinter as tk
from tkinter import ttk, filedialog
from ds_messenger import DirectMessenger
from Profile import Profile, Path
from ds_client import join_server

# server ip: 168.235.86.101

# pylint: disable=C0116, W0621, W0622, R0913, R0914, R1710, R0902, W0718
# pylint: disable=W0612, W0613, C0115, E1120, W0611, W0614, R1705


class Body(tk.Frame):
    '''This class is used to create the main chat window.'''
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self.messages = []

        self._draw()

    def node_select(self, event=None):
        self.remove_duplicate_msgs()
        # Get the selected item
        # item = self.posts_tree.selection()[0]

        selected_items = self.posts_tree.selection()
        if not selected_items:
            return
        item = selected_items[0]

        # Get the text of the selected item
        username = self.posts_tree.item(item, 'text')
        # Filter self.messages for messages from this user
        user_messages = [
            msg for msg in self.messages
            if msg.get('from') == username or msg.get('to') == username
        ]
        user_messages = sorted(
            user_messages,
            key=lambda msg: msg['timestamp'],
            reverse=True
        )
        self.entry_editor.delete('1.0', tk.END)
        # Insert the user messages into the entry editor
        for message in user_messages:
            if message.get('from') == username:
                self.insert_contact_message(message['message'], username)
            else:
                self.insert_user_message(message['message'], 'You')
        # scroll to most recent message history
        self.entry_editor.see(tk.END)

        self.after(2000, self.node_select)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str, username: str):
        formatted_message = f"{username}: {message}\n"
        self.entry_editor.insert(1.0, formatted_message, 'entry-right')

    def insert_contact_message(self, message: str, username: str):
        formatted_message = f"{username}: {message}\n"
        self.entry_editor.insert(1.0, formatted_message, 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def update_messages(self, messages):
        self.messages = messages

    def add_new_message(self, message):
        self.messages.append(message)

    def clear_tree(self):
        for id in self.posts_tree.get_children():
            self.posts_tree.delete(id)

    def remove_duplicate_msgs(self):
        message_strs = set(
            json.dumps(m, sort_keys=True) for m in self.messages
        )
        self.messages = [json.loads(s) for s in message_strs]

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.configure(bg='gray9')
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        styletree = ttk.Style()
        styletree.configure(
            "Treeview",
            font=('Helvetica', 10, 'italic'),
            background='gray9',
            fieldbackground='gray9',
            foreground='white'
        )
        self.posts_tree.heading("#0", text="Friends")
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.configure(
            font=('Verdana', 14, 'bold'),
            bg='dark grey',
            fg='white'
        )
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(
            editor_frame,
            width=0,
            height=5,
            bg='seashell2'
        )
        self.entry_editor.configure(
            font=('Verdana', 14, 'normal'),
            bg='gray14',
            fg='white'
        )
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(
            master=self,
            text="Send",
            width=20,
            command=self.send_click,
            bg='midnight blue',
            fg='white'
        )

        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.configure(bg='black', fg='white')
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class CreateFileDialog(tk.simpledialog.Dialog):
    def body(self, master):
        self.title("Create a New Profile")

        tk.Label(master, text="Enter a username:").grid(row=0)
        tk.Label(master, text="Enter a password:").grid(row=1)
        tk.Label(master, text="Enter a server IP:").grid(row=2)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        return self.e1  # initial focus

    def apply(self):
        self.result = (
            self.e1.get(),
            self.e2.get(),
            self.e3.get()
        )


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.profile = None
        self.path = None
        self.messages = None
        self.direct_messenger = DirectMessenger()

        self._draw()

    def send_message(self):
        recipient = self.get_recipient_from_gui()
        if not recipient:
            return
        message = self.body.get_text_entry()

        server_status = self.check_for_server()
        if not server_status:
            return

        status = self.direct_messenger.send(str(message), str(recipient))

        if status:
            self.body.message_editor.delete("1.0", tk.END)
            message_dict = {
                "message": message,
                "to": recipient,
                "timestamp": str(time.time())}
            self.profile.add_message(message_dict)
            self.profile.remove_duplicate_messages()
            self.profile.save_profile(self.path)
            self.messages.append(message_dict)
            self.body.add_new_message(message_dict)
            return
        else:
            tk.messagebox.showerror(
                "Error",
                "Message failed to send. Please try again later."
            )
            return

    def get_recipient_from_gui(self):
        selected_items = self.body.posts_tree.selection()
        if not selected_items:
            tk.messagebox.showerror(
                "Error",
                "No friend selected. Please"
                " select a friend from the contact list."
            )
            return False
        recipient = self.body.posts_tree.item(selected_items[0], 'text')
        return str(recipient)

    def check_for_server(self):
        if self.direct_messenger and self.direct_messenger.dsuserver:
            return True
        else:
            tk.messagebox.showerror(
                "Error",
                "Please configure the server before sending a message."
            )
            return False

    def add_contact(self):
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        name = tk.simpledialog.askstring(
            "Add Contact",
            "Enter the name of the new contact"
        )
        self.body.insert_contact(name)
        self.profile.add_friend(name)
        self.profile.save_profile(self.path)

    def recipient_selected(self, recipient):
        self.recipient = recipient

    def check_new(self):
        # You must implement this!
        if self.direct_messenger.dsuserver:
            new_messages = self.direct_messenger.retrieve_new()
            if new_messages:
                for message in new_messages:
                    self.messages.append(message)
                    self.profile.add_message(message)

                    # check if the sender of the message is in the friends list
                    if message['from'] not in self.profile.friends:
                        self.profile.add_friend(message['from'])
                        self.body.insert_contact(message['from'])

                    self.body.add_new_message(message)
                self.profile.remove_duplicate_messages()
                self.profile.save_profile(self.path)

        self.after(2000, self.check_new)

    def create_new_file(self):
        dialog = CreateFileDialog(self.root, "Create New Profile")
        if not dialog.result:
            return tk.messagebox.showwarning(
                "Please try again",
                "All fields must be filled out"
            )
        username, password, server = dialog.result
        response = join_server(server, 3021, username, password)
        if response.message == 'Invalid password or username already taken':
            return tk.messagebox.showerror(
                "Error",
                "Invalid password or username already taken"
            )

        if username and password:
            directory = filedialog.askdirectory()

            if directory:
                profile = Profile(server, username, password)
                dsu_file = Path(directory) / f'{username}.dsu'
                dsu_file.touch()
                profile.save_profile(str(dsu_file))
                self.profile = profile
                self.path = str(dsu_file)
                self.open_file(profile)
            else:
                tk.messagebox.showinfo(
                    "No Directory Selected",
                    "Please select a directory to save the file."
                )
        else:
            tk.messagebox.showwarning(
                "Input Error",
                "All fields must be filled out"
            )

    def open_file(self, profile=None):
        if not profile:
            file_path = filedialog.askopenfilename(
                filetypes=[("DSU Files", "*.dsu")]
            )

            if file_path:
                profile = Profile()
                profile.load_profile(file_path)
                self.profile = profile
                self.path = file_path

            else:
                tk.messagebox.showinfo(
                    "No File Selected",
                    "Please select a file to open."
                )
                return

        self.server = profile.dsuserver
        self.username = profile.username
        self.password = profile.password
        self.server = profile.dsuserver
        self.messages = profile.messages
        self.direct_messenger = DirectMessenger(
            self.server,
            self.username,
            self.password
        )

        database_messages = self.direct_messenger.retrieve_all()
        self.messages += database_messages
        self.load_friends_from_database()
        self.profile.save_profile(self.path)
        try:
            self.check_new()
        except Exception as e:
            print(e)
            print("No internet connection")
        self.load_friends(profile)
        self.body.update_messages(self.messages)
        self.body.entry_editor.delete('1.0', tk.END)

    def load_friends_from_database(self):
        for message in self.profile.messages:
            sender = message.get('from')
            if sender:
                if sender not in self.profile.friends:
                    self.profile.add_friend(sender)
                    self.body.insert_contact(sender)

    def load_friends(self, profile):
        self.body.clear_tree()
        friends = profile.friends
        for friend in friends:
            self.body.insert_contact(friend)

    def load_messages(self, message):
        self.body.insert_user_message('message1')
        self.body.insert_contact_message('message5')
        self.body.insert_user_message('message2')
        self.body.insert_contact_message('message6')

    def load_friends_from_messages(self, messages):
        senders = set(message['from'] for message in messages)
        senders = list(senders)
        self.profile.configure_friends(senders)

    def set_profile_server(self, profile):
        profile.dsuserver = self.server
        profile.save_profile(self.path)

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.create_new_file)
        menu_file.add_command(label='Open...', command=self.open_file)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        # settings_file.add_command(label='Login to Server',
        #                           command=self.configure_server)
        tk.messagebox.showinfo("Welcome to DS Messenger", "Please "
                               "create a new profile or open an existing "
                               "one. Before you send a message, "
                               "please configure the server address.")

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(
            self.root,
            recipient_selected_callback=self.recipient_selected,
        )
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.configure(bg='black')
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    style = ttk.Style(main)
    style.theme_use('clam')
    main.configure(bg='gray9')
    # windll.shcore.SetProcessDpiAwareness(1)
    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # id = main.after(2000, app.check_new)
    # print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
