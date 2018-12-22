#!/usr/bin/env python
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
except:
	print("It looks like tkinter isn't installed.")
	sys.exit(1)

#print disassembled file
def print_disassembly(dis):
	for i in dis:
		print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
	
#disassemble file
def disassemble(filename):
	with open(filename, 'rb') as f:
		content = f.read()
	md = Cs(CS_ARCH_X86, CS_MODE_32)
	final = md.disasm(content, 0x00)
	#uncomment if you want, it breaks shit though
	#print_disassembly(final) 
	return final

#write ASM to file
def prepare_assembly(t, filename):
	t = t.strip()
	with open(filename, 'w') as f:
		f.write(t)

#load file
def loadClick():
	text = ""
	filename = filenamebox.get()
	print("Disassembling " + filename)
	for i in disassemble(filename):
		text = text + i.op_str + "\n"
	textbox.delete(1.0, END)
	textbox.insert(END, text)

#save file
def saveClick():
	text = textbox.get(1.0, END)
	filename = filenamebox.get()
	print("Saving " + filename + ".asm")
	if(filename != ""):
		if(text == ""):
			print("Disassembling " + filename)
			for i in disassemble(filename):
				text = text + i.op_str + "\n"	
		filename = filename + ".asm"
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
filenamebox = Entry(root)
filenamebox.pack(in_=top, side=LEFT)
loadbutton = Button(root, command=loadClick, text="Load Executable")
loadbutton.pack(in_=top, side=LEFT)
savebutton = Button(root, command=saveClick, text="Export ASM")
savebutton.pack(in_=top, side=LEFT)
textbox = Text(root, height=600, width=300, maxundo=10)
textbox.pack(in_=bottom, side=LEFT, fill=BOTH, expand=True)
root.mainloop()
