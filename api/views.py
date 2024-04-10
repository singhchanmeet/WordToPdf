from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tempfile import NamedTemporaryFile
import subprocess
import os

@api_view(['POST'])
def convert_docx_to_pdf(request):
    if request.method == 'POST' and request.FILES.get('docx_file'):
        docx_file = request.FILES['docx_file']

        # Define the directory to save temporary DOCX and PDF files
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the uploaded DOCX file to a temporary file in the output directory
        temp_docx_file = NamedTemporaryFile(dir=output_dir, delete=False)
        for chunk in docx_file.chunks():
            temp_docx_file.write(chunk)
        temp_docx_file.close()

        # Convert DOCX to PDF using LibreOffice
        try:
            subprocess.call(['soffice',
                             '--headless',
                             '--convert-to', 'pdf', '--outdir', output_dir, temp_docx_file.name])
            # output = subprocess.check_output(['soffice',
            #                       '--headless',
            #                       '--convert-to', 'pdf', '--outdir', output_dir, temp_docx_file.name],
            #                      stderr=subprocess.STDOUT)  # Capture both stdout and stderr
            # return Response({"Output": output.decode('utf-8')}, status=500)  # Decode byt
        except Exception as e:
            os.unlink(temp_docx_file.name)  # Remove temporary DOCX file
            return Response({'error': str(e)}, status=500)

        # Get the filename without extension
        filename_without_extension = os.path.splitext(os.path.basename(temp_docx_file.name))[0]

        # Get the path to the converted PDF file
        pdf_file_path = os.path.join(output_dir, filename_without_extension + ".pdf")

        # Read the converted PDF file
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        # Remove temporary DOCX file
        os.unlink(temp_docx_file.name)
        os.unlink(pdf_file_path)


        # print(temp_docx_file.name)
        # print(output_dir)
        # print(pdf_file_path)


        # Return the PDF file in the response
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="converted.pdf"'
        return response

    else:
        return Response({'error': 'Please provide a DOCX file in the request.'}, status=400)
