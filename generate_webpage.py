import os

# test = "ashby-hmb_07_2015"

# folderTitle is where the photos are (name_month_year)
def generateWebpage(folderTitle):
	# confirmation = input("Are you sure " + folderTitle + " is valid? (write yes/no): ")
	# if confirmation == "no":
	# 	print("EXITING...")
	# 	return -1

	# process title
	name = getName(folderTitle)
	month = getMonth(folderTitle)
	year = getYear(folderTitle)
	if month == -1 or name == -1 or year == -1:
		print("ERROR: INVALID WEBPAGE TITLE")
		return -1

	finishedFile = writeFile(folderTitle)

# word is format: name_month_year
def getName(word):
	firstUnderscore = word.find("_")
	word = word.replace("-", " ", len(word))
	if firstUnderscore == -1:
		return -1
	return word[:firstUnderscore]

# word is format: name_month_year
def getMonth(word):
	firstUnderscore = word.find("_")
	secondUnderscore = word.replace("_", "0", 1).find("_")
	if firstUnderscore == -1 or secondUnderscore == -1:
		return -1
	return word[firstUnderscore+1:secondUnderscore]

# word is format: name_month_year
def getYear(word):
	secondUnderscore = word.replace("_", "0", 1).find("_")
	if secondUnderscore == -1:
		return -1
	return word[secondUnderscore+1:]

def writeFile(folderTitle):
	fileName = os.path.join("html", folderTitle + ".html")
	print(fileName)
	file = open(fileName, "w")
	file.write(headUntilBackgroundImage)
	backgroundImage = "		  background-image: url(\"../covers/" + folderTitle + ".jpg\");\n"

	file.write(backgroundImage)
	file.write(headEnd)
	file.write("<body>" + "\n")
	file.write(navbar)
	file.write(titlePart1 + getName(folderTitle) + titlePart2)
	file.write(getMonth(folderTitle) + "&#8209;" + getYear(folderTitle))
	file.write(titlePart3)
	file.write(gallerySetup)
	writeFigures(file, folderTitle)
	file.write(galleryEnd)
	copyScrollingScript(file)
	file.write(endBodyHTML)
	updateIndex(folderTitle)
	updateMobile(folderTitle)
	file.close()

def copyScrollingScript(webpage):
	script = open("html/scrolling_script.html", "r")
	for line in script:
		webpage.write(line)

def writeFigures(webpage, folderTitle):
	# creates a figure for each picture in photos folder with name folderTitle
	allPhotos = os.listdir("photos/" + folderTitle)
	for photo in allPhotos:
		if photo[0] != ".":
			if not os.path.isfile("thumbnails/" + folderTitle + "/" + photo):
				print("thumbnails/" + folderTitle + "/" + photo)
				print("THUMBNAIL NOT FOUND: " + photo)
				continue
			width, height = get_image_size("photos/" + folderTitle + "/" + photo)
			figure = figurePart1 + "\"../photos/" + folderTitle + "/" + photo + "\""
			figure += figurePart2 + "\"" + str(width) + "x" + str(height) + "\""
			figure += figurePart3 + "\"../thumbnails/" + folderTitle + "/" + photo + "\""
			figure += figurePart4
			webpage.write(figure)

import fileinput
def updateIndex(folderTitle):
	for line in fileinput.FileInput("index.html", inplace=True):
		if "23344929" in line:
			
			albumThumbnail = albumThumnailPart1 + "\"html/" + folderTitle + ".html\""
			albumThumbnail += albumThumnailPart2 + "\"album_thumbnails/" + folderTitle + ".jpg\""
			albumThumbnail += albumThumnailPart3 + getName(folderTitle) + " "
			albumThumbnail += albumThumnailPart4 + "|&nbsp;" + str(getMonth(folderTitle)) + "&#8209;" + str(getYear(folderTitle))
			albumThumbnail += albumThumnailPart5
			line = line.replace(line, line+albumThumbnail)
		print(line),
	line = line.replace(line, line+"hello")

def updateMobile(folderTitle):
	for line in fileinput.FileInput("mobile.html", inplace=True):
		if "23344929" in line:
			albumThumbnail = albumThumnailPart1 + "\"html/" + folderTitle + ".html\""
			albumThumbnail += albumThumnailPart2 + "\"album_thumbnails/" + folderTitle + ".jpg\""
			albumThumbnail += albumThumnailPart3 + getName(folderTitle) + " "
			albumThumbnail += albumThumnailPart4 + "|&nbsp;" + str(getMonth(folderTitle)) + "&#8209;" + str(getYear(folderTitle))
			albumThumbnail += albumThumnailPart5
			line = line.replace(line, line+albumThumbnail)
		print(line),
	line = line.replace(line, line+"hello")

import struct
import imghdr

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height
headUntilBackgroundImage = "<!DOCTYPE html>\n <head> \n <link rel=\"stylesheet\" href=\"../bootstrap-3.3.6-dist/css/bootstrap.min.css\">\n \
	<!-- jQuery library --> \n \
	<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js\"></script> \n \
	<!-- Latest compiled JavaScript --> \n \
	<script src=\"http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js\"></script> \n \
	<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> \n \
	<!-- Core CSS file -->\n \
		<link rel=\"stylesheet\" href=\"../gallery/dist/photoswipe.css\"> \n \
		<!-- Modern Family font -->\n \
	    <link href='https://fonts.googleapis.com/css?family=Raleway:400,100' rel='stylesheet' type='text/css'>	\n \
		<!-- Skin CSS file (styling of UI - buttons, caption, etc.)\n \
		     In the folder of skin CSS file there are also:\n \
	 - .png and .svg icons sprite, \n \
	 - preloader.gif (for browsers that do not support CSS animations) -->\n \
	<link rel=\"stylesheet\" href=\"../gallery/dist/default-skin/default-skin.css\"> \n \
	<!-- Core JS file --> \n \
	<script src=\"../gallery/dist/photoswipe.min.js\"></script> \n \
	<!-- UI JS file -->\n \
	<script src=\"../gallery/dist/photoswipe-ui-default.min.js\"></script> \n \
	<link rel=\"stylesheet\" href=\"pages.css\">\n \
	<style>\n \
		section.section.parallax-2 {\n"

headEnd = "		  background-attachment: scroll; \n \
		} \n \
	</style>\n \
</head>\n"
	
navbar = "	<div class=\"navbar navbar-default nav-collapse navbar-fixed-top\">\n \
 \n \
		<div class=\"container\" id=\"nav\">\n\
 \n \
			<div class=\"navbar-header\">\n \
				<button type=\"button\" class=\"navbar-toggle collapsed\" data-toggle=\"collapse\" data-target=\"#bs-example-navbar-collapse-1\" aria-expanded=\"false\">\n \
		        <span class=\"sr-only\">Toggle navigation</span>\n \
		        <span class=\"icon-bar\"></span>\n \
		        <span class=\"icon-bar\"></span>\n \
		        <span class=\"icon-bar\"></span>\n \
		      	</button>\n \
		      	<a class=\"navbar-brand\" href=\"http://kstukalova.github.io\"><div id=\"name\">Katya Stukalova</div></a>\n \
			</div>\n \
 \n \
			<div class=\"collapse navbar-collapse navbar-right\" id=\"bs-example-navbar-collapse-1\">\n \
				<ul class=\"nav navbar-nav\">\n \
					<li id = \"home-li\" class=\"active\"><div id=\"home\"><a href=\"http://kstukalova.github.io\">Home <span class=\"sr-only\">(current)</span></a></div></li>\n \
					<li id = \"about-li\"><div id=\"about\"><a href=\"http://kstukalova.github.io/#about\">About</a></div></li>\n \
					<li id = \"photos-li\"><div id=\"photos\"><a href=\"http://kstukalova.github.io/#photos\">Photos</a></div></li>\n \
				</ul>\n \
			</div>\n \
		</div>\n \
	</div> <!--navbar navbar-default-->" + "\n"
	
titlePart1 =" 	<section class=\"section parallax parallax-2\">\n\
	  <div class=\"container_temp\">\n\
	  	<div id=\"hide\"></div>\n\
	  	<h2 id=\"title\">"

titlePart2 = " &nbsp;<span class=\"date\">|&nbsp;&nbsp;"

titlePart3 = " </span></h2>\n\
	  </div>\n\
	</section>\n"

gallerySetup = "	<div id=\"gallery\">\n\
	<div class=\"container\">\n\
	<div class=\"my-gallery\" itemscope itemtype=\"http://schema.org/ImageGallery\">\n\
	<div class=\"row\">\n\n"

galleryEnd = "	</div>\n\
	</div>\n\
	</div>\n\
	</div>\n\n\n"

figurePart1 = "	    <figure itemprop=\"associatedMedia\" itemscope itemtype=\"http://schema.org/ImageObject\">\
	        <a href="

figurePart2 = "itemprop=\"contentUrl\" data-size="

figurePart3 = ">\n\
	        <div class=\"col-xs-4 col-md-2\" >\n\
	        <div class=\"thumbnail\">\n\
	            <img src="

figurePart4 = "itemprop=\"thumbnail\" alt=\"Image description\"/>\n\
	            </div></div>\n\
	        </a>\n\
	    </figure>\n\n"


endBodyHTML = "</body>\
</html>"

albumThumnailPart1 = "										<div class=\"col-xs-6 col-md-3\">\n\
											<div class=\"thumbnail\">\n\
												<a href="

albumThumnailPart2 = " style=\"text-decoration: none\"><img src="											
albumThumnailPart3 = ">\n\
												<div class=\"caption\">"
albumThumnailPart4 = "<span class=\"date\">"
albumThumnailPart5 = "</span></div></a>\n\
											</div>\n\
										</div>\n\n"
# generateWebpage(test)
# updateIndexMobile(test)
# writeFigures(test)
generateWebpage("biking_06_2015") #biking
generateWebpage("ashby-hmb_07_2015") # ashby and hmb
generateWebpage("ggp_07_2015") # ggp
generateWebpage("carmel_07_2015") # carmel
generateWebpage("napa_07_2015") # napa
generateWebpage("sf_07_2015") # sf (07)
generateWebpage("hmb_08_2015") # hmb (08)
generateWebpage("hawaii_11_2015") # hawaii
generateWebpage("park_12_2015") # park
generateWebpage("tahoe_12_2015") # tahoe
generateWebpage("zoo_01_2015") # sf zoo
generateWebpage("stanford_01_2015") # stanford
generateWebpage("sf_02_2016") # sf (02)
generateWebpage("sf_05_2016") # sf(05)