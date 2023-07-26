from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt

# report lab dependencies
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import traceback

# New Import
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import requests

import json
import os
from django.conf import settings
import base64


# CONSTANT FOR USE
PAGE_WIDTH = 450
Y_LIMIT = 80


@csrf_exempt
def PDFConverterAPI(request):
    try:
        # Register the TTF font file
        font_path = os.path.join(settings.BASE_DIR, "media","fonts", "ScalaSansPro-Regular.ttf")
        font_name = "ScalaSansPro"
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        font_path = os.path.join(settings.BASE_DIR, "media","fonts", "ScalaSansPro-Bold.ttf")
        font_name = "ScalaSansProBold"
        pdfmetrics.registerFont(TTFont(font_name, font_path))

        # Collect All JSON Data and save them into some variables
        data = json.loads(request.body)
        json_data = json.loads(data['profile_data'])

        name = json_data['name']
        headline = json_data['headline']
        user_location = json_data['location']

        current_company = ""

        PDF_FILE_NAME = name
        # Logic for Getting the Current Company Name
        experience_for_current_company = json_data.get('experience')
        if experience_for_current_company is not None and len(experience_for_current_company) > 0:
            for experience in experience_for_current_company:
                current_company = experience.get('company') or ""
                break
        
        if current_company != "":
            PDF_FILE_NAME += "(" + current_company + ")"

        file_path = os.path.join(settings.BASE_DIR, "media", PDF_FILE_NAME)
        
        company = ''
        date_range = ''
        duration = ''
        location = ''
        description = ''
        school = ''
        degree = ''
        field_of_study = ''
        date = ''
        title = ''
        proficiency = ''
        line = ''
        summary = ''
        summary = json_data.get('summary')
        experience = json_data.get('experience')
        education = json_data.get('education')
        languages = json_data.get('languages')
        # Create a new PDF document
        pdf = canvas.Canvas(file_path, pagesize=letter)

        # Name and Heading and Logo

        # Set up some basic information
        title = PDF_FILE_NAME
        author = "Talentor"
        # Set the document title and author
        pdf.setTitle(title)
        pdf.setAuthor(author)

        # Add Logo And Footer
        page_number = 1
        addNewPage(pdf,page_number,new_page=False)

        # Add User Image
        addLogoToRight(pdf,json_data["imgURL"])

        # Name
        pdf.setFont("ScalaSansPro", 22)
        pdf.setFillColor(HexColor("#232464"))
        pdf.drawString(75, 650, name)
        
        ####################### headline new logic #####################################
        lines = []

        y = 625
        if headline is not None:
            headline_lines = headline.split('\n')
            for line in headline_lines:
                line = line.strip()
                if line != "":
                    lines.append(line)

            if len(lines) > 0:  
                print(lines)              
                x = 75
                height = 500
                for line in lines:
                    total_lines = getTotalLines(pdf,line, PAGE_WIDTH-150 , "ScalaSansPro", 16) 
                    max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 16,5,y) 
                    print('aftery', afterY)             
                    if afterY < Y_LIMIT:
                        y = 670                
                        page_number += 1
                        addNewPage(pdf, page_number, new_page=True)
                        max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 16,5,y)
                    
                    pdf.setFillColor(HexColor("#232464"))
                    write_long_string(pdf, total_lines, x, y, height, "ScalaSansPro", 16, 5)
                    y = afterY - 10
                # This is gap after headline prints
                y -= 8
            else:
                y = y - 30

        
        ################################ user location ############################################
        print("y after headline=",y)
        pdf.setFont("ScalaSansPro", 11)
        pdf.setFillColor(HexColor("#898383"))
        pdf.drawString(75, y, user_location)
        y = y - 30

        ################################ Summary ############################################
     
        if(y > 565):
            y = 575
        if summary is not None:
            print('y in summary', y)
            pdf.setFont("ScalaSansPro", 16)
            pdf.setFillColor(HexColor("#232464"))
            pdf.drawString(75, y, "Summary")
        
     
            lines = []
            if summary is not None:
                summary_lines = summary.split('\n')
                for line in summary_lines:
                    line = line.strip()
                    if line != "":
                        lines.append(line)

            # This is gap for summary headline with its content
            y -= 20     
            x = 105
            
            height = 700
            for line in lines:
                total_lines = getTotalLines(pdf,line, PAGE_WIDTH, "ScalaSansPro", 10) 
                max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 10,3,y)
                if afterY < Y_LIMIT:
                    y = 670                
                    page_number += 1
                    addNewPage(pdf, page_number, new_page=True)
                    max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 10,3,y)

                pdf.setFillColor(HexColor("#5e5959"))
                write_long_string(pdf, total_lines, x, y, height, "ScalaSansPro", 10, 3)
                y = afterY - 15
            y -= 30

        ############################## Experience ####################################################
     
        # Experience        
        # y total 85
        y_total = 85
        if y - y_total < Y_LIMIT:
            y = 670
            page_number += 1
            addNewPage(pdf, page_number, new_page=True)

        if experience is not None and len(experience) > 0:
            pdf.setFillColor(HexColor("#232464"))
            pdf.setFont("ScalaSansPro", 16)
            pdf.drawString(75, y, "Experience")
            for experience in json_data.get('experience'):
                position = experience.get('position') or ""
                company = experience.get('company') or ""
                date_range = experience.get('dateRange') or ""
                duration = experience.get('duration') or ""
                location = experience.get('location') or ""
                description = experience.get('description') or ""

                # afterYPrinting =calculateExperienceY(pdf,y,description)
                afterYPrinting = calculateExperienceYForOtherData(pdf,y,position,company,date_range,duration,location)

                # Add New Page Logic
                print(afterYPrinting)                
                if afterYPrinting < Y_LIMIT:
                    y = 690
                    page_number += 1
                    addNewPage(pdf, page_number, new_page=True)
                         
                pdf.setFont("ScalaSansProBold", 11)
                pdf.setFillColor(HexColor("#232464"))


                # new logic for position and company
                string_value = ""

                if position:
                    string_value += position

                if company:
                    if string_value:
                        string_value += ", "
                    string_value += company

                if string_value:
                    y -= 20
                    x = 105
                    # pdf.drawString(75, y, string_value)

                    # break title string
                    height = 500
                    total_lines = getTotalLines(pdf,string_value, PAGE_WIDTH, "ScalaSansProBold", 11)
                    max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansProBold", 10,5,y)
                    pdf.setFillColor(HexColor("#232464"))
                    write_long_string(pdf, total_lines, x, y, height, "ScalaSansProBold", 11, 5)

                    pdf.setFillColor(HexColor("#232464"))
                    pdf.setFont("ScalaSansPro", 9)
                    pdf.setFillColor(HexColor("#898383")) 
                    y = afterY - 15

                    print('string value',string_value)
                # new logic for position and company
                pdf.setFillColor(HexColor("#232464"))
                pdf.setFont("ScalaSansPro", 9)
                pdf.setFillColor(HexColor("#898383"))

                if date_range:
                    pdf.drawString(105, y, date_range)

                pdf.setFont("ScalaSansPro", 9)
                pdf.setFillColor(HexColor("#a59e9e"))

                if date_range and duration:
                    x_offset = 108 + pdf.stringWidth(date_range, "ScalaSansPro", 9)
                    duration = duration.replace("mos", "months").replace("yrs", "years").replace("yr", "year")
                    if 'months' not in duration:
                        duration = duration.replace("mo","month")
                    pdf.drawString(x_offset, y, "(" + duration + ")")

                pdf.setFont("ScalaSansPro", 11)
                pdf.setFillColor(HexColor("#746e6e"))

                if location != "":
                    y -= 20
                    pdf.drawString(105, y, location)  # empty                 
                
    #################################### description new logic part 1#########################################
                lines = []
                if description is not None and len(description) > 0:
                    description_lines = description.split('\n')
                    for line in description_lines:
                        line = line.strip()
                        if line != "":
                            lines.append(line)
                
                if len(lines) > 0:
                    y -= 20
                    x = 105
                    height = 500
                    for line in lines:
                        total_lines = getTotalLines(pdf,line, PAGE_WIDTH, "ScalaSansPro", 10)
                        print("total_lines=",total_lines) 
                        
                        max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 10,5,y)
                        
                        if afterY < Y_LIMIT:
                            y = 670                
                            page_number += 1
                            addNewPage(pdf, page_number, new_page=True)
                            max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 10,5,y)
                        
                        pdf.setFillColor(HexColor("#746e6e"))
                        write_long_string(pdf, total_lines, x, y, height, "ScalaSansPro", 10, 5)
                        y = afterY - 15
                else:
                    y = y - 10


        ############################## Education ####################################################
        
        if education is not None and len(education) > 0:           
            y = y - 40        
            #Education   
            print('y in education', y)     
            if y  < Y_LIMIT:
                y = 670
                page_number += 1
                addNewPage(pdf, page_number, new_page=True)

            pdf.setFillColor(HexColor("#232464"))
            pdf.setFont("ScalaSansPro", 16)
            pdf.drawString(75, y, "Education")  
            education_data = json_data.get('education',[])
            school = education_data[0].get('school') or ""
            degree = education_data[0].get('degree') or ""
            field_of_study = education_data[0].get('fieldOfStudy') or ""
            date = education_data[0].get('date') or ""
            afterYPrinting = calculateEducationY(pdf,y,school,degree,field_of_study,date)
            if afterYPrinting < Y_LIMIT:
                    y = 670
                    page_number += 1
                    addNewPage(pdf, page_number, new_page=True)
            
            for education in json_data.get('education', []):
                school = education.get('school') or ""
                degree = education.get('degree') or ""
                field_of_study = education.get('fieldOfStudy') or ""
                date = education.get('date') or ""    
                afterYPrinting = calculateEducationY(pdf,y,school,degree,field_of_study,date)

                if afterYPrinting < Y_LIMIT:
                    y = 670
                    page_number += 1
                    addNewPage(pdf, page_number, new_page=True)
                    
                
                ############ Old logic for school ###################

                # pdf.setFont("ScalaSansProBold", 11)
                # pdf.setFillColor(HexColor("#232464"))
                y -= 20
                #if school != '':
                    #pdf.drawString(75, y, school)
                    #y-=15

                
                ############ New logic for school ###################
                lines = []
                if school != '' or school is not None:
                    school_lines = school.split('\n')
                    for line in school_lines:
                        line = line.strip()
                        if line != "":
                            lines.append(line)

                if len(lines) > 0:                
                    x = 105
                    height = 300
                    for line in lines:
                        total_lines = getTotalLines(pdf,line, PAGE_WIDTH , "ScalaSansProBold", 11) 
                        
                        max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansProBold", 11,5,y)              
                        if afterY < Y_LIMIT:
                            y = 670                
                            page_number += 1
                            addNewPage(pdf, page_number, new_page=True)
                            max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 10,5,y)
                        
                        pdf.setFillColor(HexColor("#232464"))
                        write_long_string(pdf, total_lines, x, y, height, "ScalaSansProBold", 11, 5)
                        y = afterY - 10
                    y -= 8
                else:
                    y = y - 8

                output_string = None
                if degree != "":
                    output_string = degree
                    if field_of_study != "":
                        output_string += " - " + field_of_study
                    elif field_of_study == "" and date != "":
                        output_string += " , " + date
                elif degree == "" and field_of_study != "":
                    output_string = field_of_study
                    if date != "":
                        output_string += " , " + date
                elif degree == "" and field_of_study == "" and date != "":
                    output_string = date
                    
                 

                # ############## New logic for degree, field of study and date#############
                lines = []
                if output_string is not None:
                    output_string_lines = output_string.split('\n')
                    for line in output_string_lines:
                        line = line.strip()
                        if line != "":
                            lines.append(line)

                if len(lines) > 0:                
                    x = 105
                    height = 300
                    for line in lines:
                        total_lines = getTotalLines(pdf,line, PAGE_WIDTH, "ScalaSansPro", 10) 
                        
                        max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 10,5,y)              
                        if afterY < Y_LIMIT:
                            y = 670                
                            page_number += 1
                            addNewPage(pdf, page_number, new_page=True)
                            max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 10,5,y)
                        
                        pdf.setFillColor(HexColor("#746e6e"))
                        write_long_string(pdf, total_lines, x, y, height, "ScalaSansPro", 10, 5)
                        y = afterY - 10
                    #y -= 30
                else:
                    y = y - 10
                                
                 
       
        # Languages
        if languages is not None and len(languages) > 0:
            y = y - 40
            y_total = 20
            if y - y_total < Y_LIMIT:
                y = 670
                page_number += 1
                addNewPage(pdf, page_number, new_page=True)

            pdf.setFillColor(HexColor("#232464"))
            pdf.setFont("ScalaSansPro", 16)
            pdf.drawString(75, y, "Languages")

            user_languages = json_data.get('languages', [])
            user_languages_length = len(user_languages)
            count = 0
        
            for language in json_data.get('languages', []):
                count += 1
                title = language.get('title') or ""
                proficiency = language.get('proficiency') or ""    
                pdf.setFont("ScalaSansProBold", 11)
                pdf.setFillColor(HexColor("#232464"))
                y -= 20
                if title!='':
                    pdf.drawString(105, y, title)
                    y -= 15
                pdf.setFont("ScalaSansPro", 9)
                pdf.setFillColor(HexColor("#746e6e"))
                if proficiency!='':
                    pdf.drawString(105, y, proficiency)
                    y -= 8
                if y < Y_LIMIT and count < user_languages_length:
                    y = 670
                    page_number += 1
                    addNewPage(pdf,page_number,True)

        # Save the PDF File
        pdf.save()
        # Read the PDF file
        with open(file_path, 'rb') as file:
            pdf_data = file.read()

        # Generate the base64-encoded string
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        return JsonResponse({'status': 200, 'message': "success", 'pdf_url': pdf_base64})

        #return JsonResponse({'status': 404, 'error': "Not Found"})
    except Exception as e:
            print(str(e))
            traceback.print_exc()
            return JsonResponse({"status": 500,"message":"not working", "error": str(e)})


def calculateEducationY(pdf,y,school,degree,field_of_study,date):

    y -= 20
    
    ############ New logic for school ###################
    lines = []
    if school != '' or school is not None:
        school_lines = school.split('\n')
        for line in school_lines:
            line = line.strip()
            if line != "":
                lines.append(line)

    if len(lines) > 0:                
        x = 105
        height = 300
        for line in lines:
            total_lines = getTotalLines(pdf,line, PAGE_WIDTH , "ScalaSansProBold", 11)             
            max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansProBold", 11,5,y)
            y = afterY - 10
        y -= 10
    else:
        y = y - 10

    output_string = None
    if degree != "":
        output_string = degree
        if field_of_study != "":
            output_string += " - " + field_of_study
        elif field_of_study == "" and date != "":
            output_string += " , " + date
    elif degree == "" and field_of_study != "":
        output_string = field_of_study
        if date != "":
            output_string += " , " + date
    elif degree == "" and field_of_study == "" and date != "":
        output_string = date
    
    # ############## New logic for degree, field of study and date#############
    lines = []
    if output_string is not None:
        output_string_lines = output_string.split('\n')
        for line in output_string_lines:
            line = line.strip()
            if line != "":
                lines.append(line)

    if len(lines) > 0:                
        x = 105
        height = 300
        for line in lines:
            total_lines = getTotalLines(pdf,line, PAGE_WIDTH, "ScalaSansPro", 10) 
            max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 10,5,y)              
            y = afterY - 10
    else:
        y = y - 10
                                
    return y            


def calculateExperienceY(pdf,y,description):
    lines = []
    if description is not None and len(description) > 0:
        description_lines = description.split('\n')
        for line in description_lines:
            line = line.strip()
            if line != "":
                lines.append(line)
    
    if len(lines) > 0:
        y -= 20
        x = 105
        height = 500
        for line in lines:
            total_lines = getTotalLines(pdf,line, PAGE_WIDTH, "ScalaSansPro", 10) 
            max_lines, afterY = getCalculateYForLines(pdf,total_lines,height,f"ScalaSansPro", 10,5,y)
            y = afterY - 20
    else:
        y = y - 10

    return y

def calculateExperienceYForOtherData(pdf,y,position,company,date_range,duration,location):
    # new logic for position and company
    string_value = ""

    if position:
        string_value += position

    if company:
        if string_value:
            string_value += ","
        string_value += company

    if string_value:
        y -= 20
        y -= 15

    if location != "":
        y -= 20

    return y

def calculateLanguagesY(pdf,y,title,proficiency):
    pass


def addNewPage(pdf, page_no, new_page=False):
    try:
        footer_text1 ='Confidential candidate information'
        footer_text2 = 'Talentor Finland Oy - Aleksanterinkatu 15 B, 00100 Helsinki, Telephone +358 (9) 681 8250, www.talentor.fi'''

        if new_page:
            pdf.showPage()
        header_image = os.path.join(settings.BASE_DIR, "media", "logo4.jpg")
        # Add header image

        pdf.drawImage(header_image, 45, 710, width=138, height=36)
        
        pdf.setFont("ScalaSansPro", 11)
        pdf.setFillColor(HexColor("#a59e9e"))
        # pdf.drawRightString(550, 60, str(page_no) + " " + footer_text)
        lines = getTotalLines(pdf,footer_text1,450,"ScalaSansPro", 8)
        
        write_long_string(pdf,lines,105,40,100,"ScalaSansPro", 8,5)
        lines = getTotalLines(pdf,footer_text2,450,"ScalaSansPro", 9)
        
        write_long_string(pdf,lines,105,30,100,"ScalaSansPro", 8,5)

        pdf.setFont("ScalaSansProBold", 9)        
        pdf.setFillColor(HexColor("#a59e9e"))
        pdf.drawString(550,40,str(page_no))
        
    except:
        pass


def addLogoToRight(pdf,img_url):
    try:
        if(img_url):
            response = requests.get(img_url)
            if response.status_code == 200:
                img_reader = ImageReader(img_url)
                # Draw the image on the canvas
                pdf.drawImage(img_reader, 430, 610, width=126, height=128)
    except:
        pass


def getTotalLines(canvas,text, width, font_name, font_size):
    lines = []
    words = text.split()
    if len(words) > 0:
        line = words[0]
        for word in words[1: ]:
            if canvas.stringWidth(line + ' ' + word, font_name, font_size) < width:
                line += ' ' + word
            else:
                lines.append(line)
                line = word
        lines.append(line)    #part one
    else:
        lines.append(" ")
    return lines

def write_long_string(canvas, lines, x, y, height, font_name, font_size, line_spacing):
    canvas.setFont(font_name, font_size)

    line_height = font_size + line_spacing
    max_lines = int(height / line_height)
    
    for i, line in enumerate(lines[:max_lines]):
        canvas.drawString(x, y - i * line_height, line)

    return len(lines) > max_lines


def getCalculateYForLines(canvas,lines,height,font_name,font_size,line_spacing,y):

    canvas.setFont(font_name, font_size)
    canvas.setFillColorRGB(0, 0, 0)  # Set text color (black in this case)
    canvas.setStrokeColorRGB(0, 0, 0)  # Set stroke color (black in this case)

    line_height = font_size + line_spacing
    max_lines = int(height / line_height)

    index = 0
    for i, line in enumerate(lines[:max_lines]):
        index = i
    y = y - index * line_height
    return max_lines, y

