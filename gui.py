import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
from typing import Text
from ds_messenger import *
from file_manager import *
from Profile import *
from ds_client import *
# from ctypes import windll
# server ip: 168.235.86.101

class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None, messages=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self.messages = messages if messages else []
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        # index = int(self.posts_tree.selection()[0])
        # entry = self._contacts[index]
        # if self._select_callback is not None:
        #     self._select_callback(entry)

        # Get the selected item
        item = self.posts_tree.selection()[0]

        # Get the text of the selected item
        username = self.posts_tree.item(item, 'text')
        # Filter self.messages for messages from this user
        user_messages = [msg for msg in self.messages if msg['from'] == username]
        user_messages = sorted(user_messages, key=lambda msg: msg['timestamp'], reverse=True)
        self.entry_editor.delete('1.0', tk.END)
        # Insert the user messages into the entry editor
        for message in user_messages:
            self.insert_contact_message(message['message'], message['timestamp'])

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str, timestamp:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)
    
    def update_messages(self, messages):
        self.messages = messages

    def clear_tree(self):
        for id in self.posts_tree.get_children():
            self.posts_tree.delete(id)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 10, 'italic'))
        self.posts_tree = ttk.Treeview(posts_frame)
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
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5, bg='seashell2')
        self.entry_editor.configure(font=('Helvetica', 14, 'normal'))
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
        save_button = tk.Button(master=self, text="Send", width=20)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        #self.password...
        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()
        

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()

class CreateFileDialog(tk.simpledialog.Dialog):
    def body(self, master):
        self.title("Create a New Profile")

        tk.Label(master, text="Enter a username:").grid(row=0)
        tk.Label(master, text="Enter a password:").grid(row=1)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1  # initial focus

    def apply(self):
        self.result = (self.e1.get(), self.e2.get())  # or return it

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
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!
        self.direct_messenger = DirectMessenger()

        # TODO UNCOMMENT WHEN SERVER IS BACK UP
        # self.messages = self.direct_messenger.retrieve_all() # retrieve all messages from server
        
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        # self.body.insert_contact("studentexw23") # adding one example student.

    def send_message(self):
        # You must implement this!
        pass

    def add_contact(self):
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        name = tk.simpledialog.askstring("Add Contact", "Enter the name of the new contact")
        self.body.insert_contact(name)
        self.profile.add_friend(name)
        self.profile.save_profile(self.path)

    def recipient_selected(self, recipient):
        self.recipient = recipient

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Server", '', '', '')
        if self.username is None and self.password is None:
            self.username = ud.user
            self.password = ud.pwd
        self.server = ud.server
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.
        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)

        # retrieve all messages after configuring server
        # TODO uncomment when server is back up
        # self.messages = self.direct_messenger.retrieve_all()
        if self.profile:
            self.set_profile_server(self.profile)

    def publish(self, message:str):
        # You must implement this!
        pass

    def check_new(self):
        # You must implement this!
        
        # TODO UNCOMMENT WHEN SERVER IS BACK UP
        # new_messages = self.direct_messenger.retrieve_new()
        
        # for message in new_messages:
        #     self.messages.append(message)
        #     self.body.update_messages(self.messages)

        # self.after(5000, self.check_new)
        pass
    
    def create_new_file(self):
        dialog = CreateFileDialog(self.root, "Create New Profile")
        username, password = dialog.result

        if username and password:
            directory = filedialog.askdirectory()

            if directory:
                profile = Profile(None, username, password)
                dsu_file = Path(directory) / f'{username}.dsu'
                dsu_file.touch()
                profile.save_profile(str(dsu_file))
                self.profile = profile
                self.path = str(dsu_file)
                self.open_file(profile)
            else:
                tk.messagebox.showinfo("No Directory Selected", "Please select a directory to save the file.")
        else:
            tk.messagebox.showwarning("Input Error", "All fields must be filled out")


    def open_file(self, profile=None):
        if not profile:
            file_path = filedialog.askopenfilename(filetypes=[("DSU Files", "*.dsu")])
            print(file_path)

            if file_path:
                profile = Profile()
                profile.load_profile(file_path)
                self.profile = profile
                self.path = file_path

            else:
                tk.messagebox.showinfo("No File Selected", "Please select a file to open.")

        # TODO add functionality to load messages from profile, above too
        self.server = profile.dsuserver
        self.username = profile.username
        self.password = profile.password
        self.server = profile.dsuserver
        self.messages = profile.messages
        self.load_friends(profile)
        print(self.messages) # DELETE LATER
        self.body.update_messages(self.messages)

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
        settings_file.add_command(label='Login to Server',
                                  command=self.configure_server)
        tk.messagebox.showinfo("Welcome to DS Messenger", "Please "
                               "create a new profile or open an existing "
                               "one. Before you send a message, "
                               "please configure the server address.")

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected, messages=self.messages)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    style = ttk.Style(main)
    style.theme_use('clam')
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
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
