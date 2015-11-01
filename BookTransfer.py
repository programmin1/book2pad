#!/usr/bin/env python
# Simple Drag-drop GUI by Luke Bryan
# Based on the GTK3 drag-drop examples, and using the GPL Book2Pad transfer script.

from gi.repository import Gtk, GdkPixbuf, Gdk
import urllib
TARGET_TYPE_URI_LIST = 80

class BookWindow():
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("MainWin.glade")
		self.window = self.builder.get_object("mainwin")
		self.window.connect('drag_data_received', self.on_drag_data_received)	
		self.window.drag_dest_set( Gtk.DestDefaults.MOTION|
						  Gtk.DestDefaults.HIGHLIGHT | Gtk.DestDefaults.DROP,
						  [Gtk.TargetEntry.new("text/uri-list", 0, 80)], Gdk.DragAction.COPY)
			
	@staticmethod
	def get_file_path_from_dnd_dropped_uri(uri):
		# get the path to file
		path = ""
		if uri.startswith('file:\\\\\\'): # windows
			path = uri[8:] # 8 is len('file:///')
		elif uri.startswith('file://'): # nautilus, rox
			path = uri[7:] # 7 is len('file://')
		elif uri.startswith('file:'): # xffm
			path = uri[5:] # 5 is len('file:')

		path = urllib.url2pathname(path) # escape special chars
		path = path.strip('\r\n\x00') # remove \r\n and NULL

		return path

	def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp):
		if target_type == TARGET_TYPE_URI_LIST:
			uri = selection.get_data().strip('\r\n\x00')
			self.builder.get_object('droppableLabel').set_text("Please wait...")
			#print 'uri', uri
			uri_splitted = uri.split() # we may have more than one file dropped
			url_splitted = [ self.get_file_path_from_dnd_dropped_uri(fixed) for fixed in uri_splitted ]
			#for uri in uri_splitted:
				#path = self.get_file_path_from_dnd_dropped_uri(uri)
				#print 'path to open', path
				#if os.path.isfile(path): # is it file?
					#data = file(path).read()
					#print data
			
			iPadDir = self.get_file_path_from_dnd_dropped_uri( self.builder.get_object("filechooser").get_uri() )
			print 'Transfer to: ' + iPadDir
			import book2pad
			book2pad.addbooks( iPadDir, url_splitted )
			self.builder.get_object('droppableLabel').set_text("Done!")
			
bw = BookWindow()	
bw.window.show_all()
Gtk.main()
