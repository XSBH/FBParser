from Tkinter import *
import urllib

def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

if __name__ == "__main__":
    f = open('view-source www.facebook.com.html')

    # Find the HTML code with 'InitialChatFriendsList'
    for piece in read_in_chunks(f):
        if "InitialChatFriendsList" in piece:
            source = piece.split(",")
            break;
        
    # Strip away the useless HTML code in source and leave only fb id
    for piece in source:
        if piece.startswith("{\"list\":"):
            i = source.index(piece)
    source = source[i:i + 10]
    id_list = []
    id_list.append(source[0][10:-3])
    for id in source[1:]:
        id_list.append(id.strip("\"")[:-2])
    
    # Use id to log onto the person's fb page and look for person's name
    user_list = []
    for id in id_list:
        source_code = urllib.urlopen("http://facebook.com/" + str(id))
        for piece in read_in_chunks(source_code):
            if "id=\"pageTitle\"" in piece:
                i = piece.find("pageTitle")
                i2 = piece.find("</title")
                # If the persons profile is private then it will display
                # page not found instead of their name
                if piece[i+11:i2-11] == "Page Not Found":
                    user_list.append(id)
                else:
                    user_list.append(piece[i+11: i2-11])
                break;

    # Create the interface
    root = Tk()
    root.pack_propagate(0)
    root.config(height="335", width="200")
    l1 = Label(root, text="Your fb creepers:", bd=15, font=10)
    l1.pack()
    for i in range(len(user_list)):
        l2 = Label(root, text=str(i+1) + ". " + user_list[i], bd=5)
        l2.pack()
    root.mainloop()
