import flet as A,time as S,PyPDF2 as C;from PIL import Image as T;from flet import Text as d, DataRow as c, DataCell as f, Container as g, DataColumn as h
def E(D):
	D=T.open(D);A={"Path":D.filename,"Size":D.size,"Height":D.height,"Width":D.width,"Format":D.format,"Mode":D.mode,"Animated":getattr(D,"Is animated",False),"Frames in Image":getattr(D,"Frames",1)}
	try:del D.info['exif'];A|=D.info
	except:A|=D.info
	return A
def W(d):A=C.PdfReader(open(d,"rb"));return(A.metadata)
def J(b):
	b.title,b.window_width,b.window_minimized="Data-Py",600,False
	def e():
		F,G,L=str(M.split(".")[-1]).lower(),{"png","jpge","jpg","gif","ico","tga","jpeg"},[]
		if {F}&G:H=E(M);[L.append(c(cells=[f(d(A)),f(d(B))])) for A,B in H.items()]
		elif F=="pdf":H=W(M);[L.append(c(cells=[f(d(A.replace("/",""))),f(d(B))])) for A,B in H.items()]
		else:L=c(cells=[f(d("Error,this extension is not contemplated")),f(d("Error,this extension is not contemplated"))]),
		return L
	def O(E):global M;M=E.path;P() if E.path!=None else b.go("/") 
	def P():b.views.clear();b.update();b.go("/t")
	def Q(R):
		s=600;R,U,V=A.AppBar(title=d("Scan")),g(d("Data-Py\nExtract Metadata",text_align="center",size=50), width=s,margin=50),A.FilePicker(on_result=O);Container_picket,X=g(V, height=50),g(A.ElevatedButton("Open File",icon=A.icons.FILE_UPLOAD_OUTLINED,on_click=lambda _: V.save_file(),disabled=b.web),alignment=A.alignment.center);Z,wm=g(d("Formats support\npdf, png, jpge, jpg, gif, ico, tga...",text_align="center"),width=s),g(d("By: M20191",text_align="center"),width=s,margin=240);Y=A.Column([U,V,X,Z,wm]);b.views.append(A.View("/",[Y]))
		if b.route=="/t":H=A.ListView(expand=1,spacing=10,padding=20);H.controls=A.DataTable(columns=(h(d("Key")),h(d("Data"))),rows=e()),;b.views.append(A.View("/t",[R,H]));b.update()
	def AA(v):b.views.pop();tw=b.views[-1];b.go(tw.route)
	b.on_route_change=Q;b.on_view_pop=AA;b.go(b.route)
A.app(target=J,assets_dir="assets")