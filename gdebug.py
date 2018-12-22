#!/usr/bin/env python3
#
#	gDebug
#	by arcticf0x
#	Shitty debugger
#

#import libs
import sys, os
try:
	from capstone import *
except:
	print("It looks like capstone isn't installed.")
	sys.exit(1)

try:
	from tkinter import *
	import tkinter.filedialog
except:
	print("It looks like tkinter isn't installed.")
	sys.exit(1)

#print disassembled file
def print_disassembly(dis):
	for i in dis:
		print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
	
#disassemble file
def disassemble(filename):
	arch=archselection.get(ACTIVE)
	mode=modeselection.get(ACTIVE)
	allowed_arch = {"CS_ARCH_ARM": CS_ARCH_ARM, "CS_ARCH_ARM64": CS_ARCH_ARM64, "CS_ARCH_X86": CS_ARCH_X86}
	
	if(arch not in allowed_arch):
		print("You need to use an architecture that is in this list:\n" + allowed_arch)
		return []
	
	if(arch == "CS_ARCH_X86"):
		allowed_mode = {"CS_MODE_16": CS_MODE_16, "CS_MODE_32": CS_MODE_32, "CS_MODE_64": CS_MODE_64}
		
	if(arch == "CS_ARCH_ARM"):
		allowed_mode = {"CS_MODE_ARM": CS_MODE_ARM, "CS_MODE_THUMB": CS_MODE_THUMB}
		
	if(arch == "CS_ARCH_ARM64"):
		allowed_mode = {"CS_MODE_ARM": CS_MODE_ARM}
	
	if(mode not in allowed_mode):
		print("You need to use one of these modes:\n" + allowed_mode)
		return []
	
	arch = allowed_arch[arch]
	mode = allowed_mode[mode]
	try:
		with open(filename, 'rb') as f:
			content = f.read()
	except:
		print("Error opening " + filename)
		return []
	
	try:
		md = Cs(arch, mode)
		final = md.disasm(content, 0x00)
		#uncomment if you want, it breaks shit though
		#print_disassembly(final) 
	except:
		print("Error disassembling " + filename)
		return []
		
	return final

#write ASM to file
def prepare_assembly(t, filename):
	try:
		t = t.strip()
		with open(filename, 'w') as f:
			f.write(t)
	except:
		print("Error writing to file " + filename)

#load file
def loadClick():
	text = ""
	filename = tkinter.filedialog.askopenfilename()
	if(filename == None):
		return
	print("Disassembling " + filename)
	disassembly = disassemble(filename)
	if(disassembly == []):
		filenamebox.delete()
		filenamebox.insert("Error loading!")
	for i in disassembly:
		text = text + i.op_str + "\n"
	textbox.delete(1.0, END)
	textbox.insert(END, text)

#save file
def saveClick():
	text = textbox.get(1.0, END)
	filename = tkinter.filedialog.asksaveasfilename(defaultextension = ".asm")
	print("Saving " + filename + ".asm")
	if(filename != None and text != ""):
		print("Deleting " + filename + " if it exists...")
		try:
			os.remove(filename)
		except OSError:
			pass
		print("Saving...")
		prepare_assembly(text, filename)

#setup window
text = ""
root = Tk()
top = Frame(root)
bottom = Frame(root)
top.pack(side=TOP)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
archselection = Listbox(root, exportselection=0, height=3)
archselection.pack(in_=top, side=LEFT)
for i in ["CS_ARCH_ARM", "CS_ARCH_ARM64", "CS_ARCH_X86"]:
	archselection.insert(END, i)
modeselection = Listbox(root, exportselection=0, height=3)
modeselection.pack(in_=top, side=LEFT)
#filenamebox = Entry(root)
#filenamebox.pack(in_=top, side=LEFT)
loadbutton = Button(root, command=loadClick, text="Load Executable")
loadbutton.pack(in_=top, side=LEFT)
savebutton = Button(root, command=saveClick, text="Export ASM")
savebutton.pack(in_=top, side=LEFT)
textbox = Text(root, height=600, width=300, maxundo=10)
textbox.pack(in_=bottom, side=LEFT, fill=BOTH, expand=True)
global last
last = ""
def refreshmode():
	global last
	if(archselection.get(ACTIVE) != last):
		modeselection.delete(0, END)
		if(archselection.get(ACTIVE) == "CS_ARCH_ARM"):
			for i in ["CS_MODE_ARM", "CS_MODE_THUMB"]:
				modeselection.insert(END, i)
		if(archselection.get(ACTIVE) == "CS_ARCH_ARM64"):
			for i in ["CS_MODE_ARM"]:
				modeselection.insert(END, i)
		if(archselection.get(ACTIVE) == "CS_ARCH_X86"):
			for i in ["CS_MODE_16", "CS_MODE_32", "CS_MODE_64"]:
				modeselection.insert(END, i)
		last = archselection.get(ACTIVE)
	root.after(250, refreshmode)

refreshmode()

root.mainloop()
