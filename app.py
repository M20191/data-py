import flet as ft
import PyPDF2
from PIL import Image

def e_image(image:str) -> dict[str,str]:
	"""Returns the metadata of an image
	Args:
		image (str): Image to open
	Returns:
		simple_metadata (str): all data collected
	"""
	
	# read the image data using PIL
	image = Image.open(image)
	# extract other basic metadata
	simple_metadata = {"Filename": image.filename,"Image Size": image.size,"Image Height": image.height,"Image Width": image.width,"Image Format": image.format,"Image Mode": image.mode,"Image is Animated": getattr(image, "is_animated", False),"Frames in Image": getattr(image, "n_frames", 1)}
	try:
		del image.info['exif']
		simple_metadata |= image.info
	except:
		simple_metadata |= image.info

	return simple_metadata

def e_pdf(pdf_name:str) -> dict[str,str]:
	"""Returns the metadata of a pdf
	Args:
		pdf_name (str): pdf to open
	Returns:
		pdf_info (dict): all data collected
	"""

	# read the pdf file
	pdf = PyPDF2.PdfReader(open(pdf_name,"rb"))
	return pdf.metadata


def main(page: ft.Page):
	# Configuraciones
	page.title = "Data-Py"
	page.window_width = 600
	page.window_max_height = page.window_height
	page.window_max_width = page.window_width
	page.window_minimized = False

	# Load the metadata table
	def table():
		"""Load the Columns of the table"""

		# Name and extensions available
		name = str(path.split(".")[-1]).lower()
		img_allowed = ["png","jpge","jpg","gif","ico","tga","jpeg"]
		metadata_table = []

		# Image vie
		if name in img_allowed:
			# Img metadata
			simple_metadata = e_image(path)
			[metadata_table.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value)),ft.DataCell(ft.Text(data))])) for value,data in simple_metadata.items()]

		# Pdf metadata
		elif name == "pdf":
			simple_metadata = e_pdf(path)
			[metadata_table.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value.replace("/",""))),ft.DataCell(ft.Text(data))])) for value,data in simple_metadata.items()]

		# Error in file
		else:
			metadata_table = ft.DataRow(cells=[ft.DataCell(ft.Text(f"Error, Error, this extension is not contemplated")),ft.DataCell(ft.Text(f"Error, this extension is not contemplated"))]),

		return metadata_table

	# Save file
	def save_file_result(e: ft.FilePickerResultEvent):global path; path = e.path;load() if e.path != None else page.go()

	# Load page
	def load():page.views.clear();page.update();page.go("/table")

	def route_change(route):
		"""Main app"""
		# Main controls
		bar = ft.AppBar(title=ft.Text("Table Scan"), bgcolor=ft.colors.SURFACE_VARIANT)
		data_py = ft.Container(ft.Text("Data-Py\nExtract Metadata",text_align="center",size=50), width=600,margin=50)
		picker = ft.FilePicker(on_result=save_file_result)
		Container_picket = ft.Container(picker, height=50)
		bottom = ft.Container(ft.ElevatedButton("Open File",icon=ft.icons.FILE_UPLOAD_OUTLINED,on_click=lambda _: picker.save_file(),disabled=page.web),alignment=ft.alignment.center)
		support = ft.Container(ft.Text(f"Formats support\npng, jpge, jpg, gif, ico, tga...",text_align="center"),width=600)
		wm = ft.Container(ft.Text("By: M20191",text_align="center"),width=600,margin=240)

		all_controls = ft.Column([data_py,picker,bottom,support,wm])

		# Append menu view
		page.views.append(ft.View("/",[all_controls]))

		# Change route
		if page.route == "/table":
			# Create metadata table
			metadata_list = ft.ListView(expand=1, spacing=10, padding=20)
			metadata_list.controls.append(ft.DataTable(columns=[ft.DataColumn(ft.Text("Key")),ft.DataColumn(ft.Text("Data"))],rows=table()))
			# View
			page.views.append(ft.View("/table",[bar,metadata_list]))



	# Change route
	def view_pop(view):
		page.views.pop()
		top_view = page.views[-1]
		page.go(top_view.route)

	page.on_route_change = route_change
	page.on_view_pop = view_pop
	page.go(page.route)

# Core
ft.app(target=main,assets_dir="assets")