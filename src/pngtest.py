import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

MAX_LABEL_SIZE=50
isAliased = False
ttfPath=""





class FileChoserWindow(Gtk.Window):

	def __init__(self):

		global isAliased
		global label
		Gtk.Window.__init__(self, title="TTF to SM64 Font")

		mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
		self.add(mainBox)

		fileChooseBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)



		button1 = Gtk.Button("Choose File")
		button1.connect("clicked", self.on_file_clicked)

		label = Gtk.Label(''.join([' ' for i in range(MAX_LABEL_SIZE)]));

		optionsBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)


		button = Gtk.CheckButton("Turn on Antialiasing")
		button.connect("toggled", self.on_alias_toggle)

		fontSizeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)
		fontLabel = Gtk.Label("Font Size: ")
		fontSize = Gtk.Entry()
		fontSize.set_text("20")
		mainBox.pack_start(fileChooseBox,True,True,0)
		fileChooseBox.pack_start(button1,True,True,0)
		fileChooseBox.pack_start(label,True,True,0);
		optionsBox.pack_start(button, True, True,0)
		mainBox.pack_start(optionsBox,True,True,0)

		fontSizeBox.pack_start(fontLabel,True,True,0)
		fontSizeBox.pack_start(fontSize,True,True,0)
		mainBox.pack_start(fontSizeBox,True,True,0)



	def on_alias_toggle(self,widget):
		global isAliased
		isAliased=(not isAliased)
		print(isAliased)

	def on_file_clicked(self, widget):
		global ttfPath
		global label
		dialog = Gtk.FileChooserDialog("Please choose a file", self,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		self.add_filters(dialog)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Open clicked")
			ttfPath = dialog.get_filename()
			label.set_text(str(ttfPath))
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")

		dialog.destroy()

	def add_filters(self, dialog):
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Text files")
		filter_text.add_mime_type("text/plain")
		dialog.add_filter(filter_text)

		filter_py = Gtk.FileFilter()
		filter_py.set_name("Python files")
		filter_py.add_mime_type("text/x-python")
		dialog.add_filter(filter_py)

		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)


win = FileChoserWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()