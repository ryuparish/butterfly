from tkinter import *
from PIL import ImageTk,Image
import sqlite3
import os
from random import choice

# I have no idea what the heck this is, but it fixes the no $DISPLAY problem
if os.environ.get('DISPLAY', '') == '':
    #print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


# Initial almighty tkinter window object
root = Tk()
root.title('Time to b 1337')
width = root.winfo_screenwidth()
height = root.winfo_screenheight() - 70
root.geometry(f"{width}x{height}+0+0")

# Long live Solaire
background_image = PhotoImage(file='butterfly_perfect1.png')
background_label = Label(root, image=background_image)
background_label.place(x=185, y=0, relwidth=1, relheight=.4)

# Checking to see if there is a database and creating one if there is not 
conn = sqlite3.connect('clothes.db')
c = conn.cursor()
# Create table
c.execute("""CREATE TABLE IF NOT EXISTS clothes (
		cloth_name text,
		section text,
		season text,
		outerwear bool,
		classic_number integer,
		condition text
		)""")

# Create Update function to update a record
# Auxillary function that does not show a window, only updates the sql database
def update():

	# Create a database or connect to one
	conn = sqlite3.connect('clothes.db')
        
	# Create cursor
	c = conn.cursor()

	record_id = edit_box.get()

	c.execute("""UPDATE clothes SET
		cloth_name = :cloth_name,
		section = :section,
		season = :season,
		outerwear = :outerwear,
		classic_number = :classic_number,
		condition = :condition 

		WHERE cloth_name = :target_cloth""",
		{
		'cloth_name': cloth_name_editor.get(),
		'section': section_editor.get(),
		'season': season_editor.get(),
		'outerwear': outerwear_editor.get(),
		'classic_number': classic_number_editor.get(),
		'condition': condition_editor.get(),
		'target_cloth': target_cloth
		})


	#Commit Changes
	conn.commit()

	# Close Connection and editor window
	conn.close()
	editor.destroy()

# Create function to mark the chosen clothes dirty
def mark_dirty(con, generator, dirty_clothes):
    c = con.cursor()
    c.execute("""UPDATE clothes SET
        condition = 1
        WHERE cloth_name IN (:top, :bottom, :sock)""",
    {
            'top': dirty_clothes[0],
            'bottom': dirty_clothes[1],
            'sock': dirty_clothes[2]
    })
    con.commit()
    generator.destoy()

    
# At this point, all this does it close the moment it is done updating.
# Create Edit function to update a record (this creates a second window)
def edit():
       global editor
       editor = Tk()
       editor.title('Update Clothing')
       editor.geometry("400x300")
       # Create a database or connect to one
       conn = sqlite3.connect('clothes.db')
       # Create cursor
       c = conn.cursor()
       
       global target_cloth
       target_cloth = edit_box.get()
       # Query the database
       c.execute("SELECT * FROM clothes WHERE cloth_name = :target_cloth", {"target_cloth": target_cloth})
       clothing = c.fetchall()
       
       #Create Global Variables for text box names
       global cloth_name_editor
       global section_editor
       global season_editor
       global outerwear_editor
       global classic_number_editor
       global condition_editor
       
       # Create Text Boxes
       cloth_name_editor = Entry(editor, width=30)
       cloth_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
       section_editor = Entry(editor, width=30)
       section_editor.grid(row=1, column=1)
       season_editor = Entry(editor, width=30)
       season_editor.grid(row=2, column=1)
       outerwear_editor = Entry(editor, width=30)
       outerwear_editor.grid(row=3, column=1)
       classic_number_editor = Entry(editor, width=30)
       classic_number_editor.grid(row=4, column=1)
       condition_editor = Entry(editor, width=30)
       condition_editor.grid(row=5, column=1)
       
       # Create Text Box Labels
       cloth_name_label = Label(editor, text="Clothing Name")
       cloth_name_label.grid(row=0, column=0, pady=(10, 0))
       section_label = Label(editor, text="Section")
       section_label.grid(row=1, column=0)
       season_label = Label(editor, text="Season")
       season_label.grid(row=2, column=0)
       outerwear_label = Label(editor, text="Outerwear")
       outerwear_label.grid(row=3, column=0)
       classic_outfit_label = Label(editor, text="Classic Number")
       classic_outfit_label.grid(row=4, column=0)
       condition_label = Label(editor, text="Condition")
       condition_label.grid(row=5, column=0)
       
       # Display the cloth to be edited
       for cloth in clothing:
        cloth_name_editor.insert(0, cloth[0])
        section_editor.insert(0, cloth[1])
        season_editor.insert(0, cloth[2])
        outerwear_editor.insert(0, cloth[3])
        classic_number_editor.insert(0, cloth[4])
        condition_editor.insert(0, cloth[5])
       
       
       # Does nothing currently with the settings above 
       # Create a Save Button To Save edited record
       edit_btn = Button(editor, text="Update Cloth", command=update)
       edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

# Redo the query with different random numbers
def redo(con, generator):
    con.close()
    generator.destroy()
    generate(outerwear_choice.get())


# If there are no clean clothes
def no_clean_clothes():
    ew = Tk()
    ew.title('Do your Laundry')
    ew.geometry("500x500")
    nasty = Label(ew, text="You have no clean clothes you stinker!")
    nasty.place(relx=.5, rely=.5, anchor="center")


# Generate the clothing and ask again if disapproved. If approved mark dirty.
def generate(outerwear_choice):
    global generator
    generator = Tk()
    generator.title('Produced Clothing')
    # Full Screen vvvvvvv
    #generator.geometry(f"{width}x{height}+0+0")
    generator.geometry("400x300")
    # Create a database or connect to one
    conn = sqlite3.connect('clothes.db')
    # Create cursor
    c = conn.cursor()
    
    # Query the database for clean clothes 
    c.execute("SELECT * FROM clothes WHERE condition == 0")
    clothing = c.fetchall()
    if not clothing:
        conn.close()
        no_clean_clothes()
        generator.destroy()
        return

    ### TODO ###
    # Implement the "Classic Outfits" option. (changing the query may be more efficient than looping)
    
    # Perhaps we should think about choosing between showing partial outfits if certain sections of clothing are all dirty. Or 
    # just completely denying if there are no clothes to suggest for any section. (there will be an error if we try to use random.choice)

    # Getting the names for one of each Outerwear, Top, Undies, Bottom, Socks.
    # Outerwear and Outfit specification are optional.
    
    # If outerwear is selected, then you should run "choice", if not, just set outerwear to ""
    # The outerwear_choice variable will be equal to the STRING "None" if it is not selected.
    if(outerwear_choice != "None"):
        outerwear = choice([cloth[0] for cloth in clothing if cloth[1] == outerwear_choice])
    else:
        outerwear = "No Outerwear"

    top = choice([cloth[0] for cloth in clothing if cloth[1] == "Top"])
    undies = choice([cloth[0] for cloth in clothing if cloth[1] == "Undies" ])
    bottom = choice([cloth[0] for cloth in clothing if cloth[1] == "Bottom" ])
    sock = choice([cloth[0] for cloth in clothing if cloth[1] == "Socks"])
    
    # Create Text Labels
    outerwear_name_label = Label(generator, text=outerwear)
    outerwear_name_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))
    top_name_label = Label(generator, text=top)
    top_name_label.grid(row=1, column=0, columnspan=2)
    bottom_name_label = Label(generator, text=bottom)
    bottom_name_label.grid(row=2, column=0, columnspan=2)
    undies_name_label = Label(generator, text=undies)
    undies_name_label.grid(row=3, column=0, columnspan=2)
    sock_name_label = Label(generator, text=sock)
    sock_name_label.grid(row=4, column=0, columnspan=2)
    
    # Create a Save Button To Save edited record
    # You MUST use a lambda function when setting the command for some reason, or else it will run the command function,
    # even without pressing any of the buttons.
    approve_btn = Button(generator, text="Approve?", command=lambda : mark_dirty(conn, generator, (top, bottom, sock)))
    approve_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=125)
    disapprove_btn = Button(generator, text="Disapprove?", command=lambda : redo(conn, generator))
    disapprove_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=115)


# Create Function to Delete A Record
def delete():
	# Create a database or connect to one
	conn = sqlite3.connect('clothes')
	# Create cursor
	c = conn.cursor()

	# Delete a record
	c.execute("DELETE from clothes WHERE cloth_name = " + remove_box.get())

	delete_box.delete(0, END)

	#Commit Changes
	conn.commit()

	# Close Connection 
	conn.close()


# This is the initially open window
# Create Submit Function For database
def submit():
	# Create a database or connect to one
	conn = sqlite3.connect('clothes.db')
	# Create cursor
	c = conn.cursor()

	# Insert Into Table
	c.execute("INSERT INTO clothes VALUES (:cloth_name, :section, :season, :outerwear, :classic_number, :condition)",
			{
				'cloth_name': cloth_name.get(),
				'section': section.get(),
				'season': season.get(),
				'outerwear': outerwear.get(),
				'classic_number': classic_number.get(),
				'condition': condition.get()
			})


	#Commit Changes
	conn.commit()

	# Close Connection 
	conn.close()

	# Clear The Text Boxes
	cloth_name.delete(0, END)
	section.delete(0, END)
	season.delete(0, END)
	outerwear.delete(0, END)
	classic_number.delete(0, END)
	condition.delete(0, END)

# Not very useful right now
# Create Query Function
#def query():
#
#	# Create a database or connect to one
#	conn = sqlite3.connect('clothes.db')
#
#	# Create cursor
#	c = conn.cursor()
#
#	# Query the database
#	c.execute("SELECT * FROM clothes")
#	records = c.fetchall()
#	print(records)
#
#        ### TODO ###
#        # Temporarily commenting this out so I can see which indexes I should access before I display them
#	# Loop Thru Results
#	#print_records = ''
#	#for record in records:
#	#	print_records += str(record[0]) + " " + str(record[1]) + " " + "\t" +str(record[6]) + "\n"
#
#	#query_label = Label(root, text=print_records)
#	#query_label.grid(row=12, column=0, columnspan=2)
#
#	#Commit Changes
#	conn.commit()
#
#	# Close Connection 
#	conn.close()



# Q's: What is the delete box doing on both the text entries and the labels?
# Create Text Boxes
cloth_name = Entry(root, width=30)
cloth_name.grid(row=0, column=1, padx=20, pady=(10, 0))
section = Entry(root, width=30)
section.grid(row=1, column=1)
season = Entry(root, width=30)
season.grid(row=2, column=1)
outerwear = Entry(root, width=30)
outerwear.grid(row=3, column=1)
classic_number = Entry(root, width=30)
classic_number.grid(row=4, column=1)
condition = Entry(root, width=30)
condition.grid(row=5, column=1)

# Make remove_box and edit_box
remove_box = Entry(root, width=30)
remove_box.grid(row=8, column=1, pady=5)
edit_box = Entry(root, width=30)
edit_box.grid(row=10, column=1, pady=5)



# Create Text Box Labels
cloth_name_label = Label(root, text="Clothing Name")
cloth_name_label.grid(row=0, column=0, pady=(10, 0))
section_label = Label(root, text="Section")
section_label.grid(row=1, column=0)
season_label = Label(root, text="Season")
season_label.grid(row=2, column=0)
outerwear_label = Label(root, text="Outerwear")
outerwear_label.grid(row=3, column=0)
classic_number_label = Label(root, text="Classic Number")
classic_number_label.grid(row=4, column=0)
condition_label = Label(root, text="Condition")
condition_label.grid(row=5, column=0)
remove_box_label = Label(root, text="Delete Cloth Name")
remove_box_label.grid(row=8, column=0, pady=5)
edit_box_label = Label(root, text="Edit Cloth Name")
edit_box_label.grid(row=10, column=0, pady=5)

# Value to be passed into the generate clothes function for optional functionality
# This outerwear_choice pyvar must be "getted" ie. outerwear_choice.get()
outerwear_choice = StringVar()
outerwear_choice.set(None)

# Create Radio Buttons
hoodie_radio = Radiobutton(root, text="Hoodie?", variable=outerwear_choice, value="Hoodie")
hoodie_radio.grid(row=12, column=0, columnspan=2, pady=5, padx=10)
jacket_radio = Radiobutton(root, text="Jacket?", variable=outerwear_choice, value="Jacket")
jacket_radio.grid(row=13, column=0, columnspan=2, pady=5, padx=10)

# Ordering:
   # Add
   # Remove
   # Edit
   # Generate
# ipadx means *inner* padding of the button (x-axis-wise)

# Create Submit Button
submit_btn = Button(root, text="Add Clothes To Database", command=lambda : submit())
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#Create A Delete Button
delete_btn = Button(root, text="Remove Clothing from Database", command=lambda : delete())
delete_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=75)

# Create an Edit Button
edit_btn = Button(root, text="Edit Clothing", command=lambda : edit())
edit_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=140)

# Create a Generate Button
generate_btn = Button(root, text="Generate Clothes to Wear", command=lambda : generate(outerwear_choice.get()))
generate_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=98)



#Commit Changes
conn.commit()

# Close Connection 
conn.close()

root.mainloop()
