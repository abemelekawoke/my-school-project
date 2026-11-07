# views.py
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import *
from datetime import datetime

def print_leave_request(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Printable Leave Request</title>
        <style>
            .container {{ width: 100%; max-width: 600px; margin: auto; font-family: Arial, sans-serif; position: relative; }}
            .header {{ text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px; }}
            .header img {{ max-width: 100px; }}
            .content {{ border: 1px solid #333; padding: 20px; font-size: 16px; position: relative; z-index: 10; }}
            .watermark {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                opacity: 0.1;
                z-index: 0;
                pointer-events: none;
                max-width: 400px;
                width: 100%;
            }}
            .field {{ margin: 10px 0; }}
            .label {{ font-weight: bold; }}
            .signature {{ margin-top: 40px; text-align: center; }}
            .print-button {{ display: block; margin: 20px auto; padding: 10px 20px; background-color: #0070b8; color: white; text-align: center; border-radius: 5px; text-decoration: none; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 14px; color: #666; }}
            @media print {{
                .print-button {{ display: none; }}
            }}
        </style>
        <script>
            function printPage() {{
                window.print();
            }}
        </script>
    </head>
    <body onload="printPage()">
        <div class="container">
            <div class="header">
                <img src="https://ncee.org.uk/wp-content/uploads/2023/11/gondar.png" alt="Logo">
                <div>Leave Request</div>
            </div>
            <img src="https://ncee.org.uk/wp-content/uploads/2023/11/gondar.png" alt="Watermark" class="watermark">
            <div class="content">
                <div class="field"><span class="label">Employee:</span> {leave_request.employee}</div>
                <div class="field"><span class="label">Leave Type:</span> {leave_request.leave_type}</div>
                <div class="field"><span class="label">Start Date:</span> {leave_request.start_date}</div>
                <div class="field"><span class="label">End Date:</span> {leave_request.end_date}</div>
                <div class="field"><span class="label">Status:</span> {leave_request.status}</div>
                <div class="field"><span class="label">Reason:</span> {leave_request.reason}</div>
                <div class="signature">
                    __________________________<br>
                    Approver's Signature
                </div>
            </div>
            <a href="#" class="print-button" onclick="printPage()">Print</a>
            <div class="footer">
                &copy; {datetime.now().year} Durbete Water & Sewerage Service Enterprise. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html_content)

def print_employee_experience(request, employee_id):
    # Fetch the employee and their experience details
    employee = get_object_or_404(StaffProfile, pk=employee_id)
    experiences = Experience.objects.filter(employee=employee)

    # Create the HTML content for the printable page
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Academic Staff Experience</title>
        <style>
            .container {{
                width: 100%;
                max-width: 800px;
                margin: auto;
                font-family: Arial, sans-serif;
                position: relative;
            }}
            .header {{
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .header img {{
                max-width: 100px;
            }}
            .content {{
                border: 1px solid #333;
                padding: 20px;
                font-size: 16px;
                position: relative;
                z-index: 10;
            }}
            .watermark {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                opacity: 0.1;
                z-index: 0;
                pointer-events: none;
                max-width: 400px;
                width: 100%;
            }}
            .field {{
                margin: 10px 0;
            }}
            .label {{
                font-weight: bold;
            }}
            .signature {{
                margin-top: 40px;
                text-align: center;
            }}
            .print-button {{
                display: block;
                margin: 20px auto;
                padding: 10px 20px;
                background-color: #0070b8;
                color: white;
                text-align: center;
                border-radius: 5px;
                text-decoration: none;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 14px;
                color: #666;
            }}
            @media print {{
                .print-button {{
                    display: none;
                }}
            }}
        </style>
        <script>
            function printPage() {{
                window.print();
            }}
        </script>
    </head>
    <body onload="printPage()">
        <div class="container">
            <div class="header">
                <img src="https://ncee.org.uk/wp-content/uploads/2023/11/gondar.png" alt="Logo">
                <div>Employee Experience</div>
            </div>
            <img src="https://ncee.org.uk/wp-content/uploads/2023/11/gondar.png" alt="Watermark" class="watermark">
            <div class="content">
                <div class="field"><span class="label">Full Name:</span> {employee.full_name_am}</div>
                <div class="field"><span class="label">Gender:</span> {employee.gender}</div>
                <div class="field"><span class="label">Position:</span> {employee.position}</div>
                <div class="field"><span class="label">Employee Status:</span> {employee.get_employee_status_display()}</div>
                
                <div class="field">
                    <span class="label">Experience:</span><br>
                    <ul>
                        {"".join([f"<li>{exp.institution} ({exp.position}) from {exp.from_date} to {exp.to_date} - {exp.net_duration}</li>" for exp in experiences])}
                    </ul>
                </div>
                
                <div class="signature">
                    __________________________<br>
                    Employee's Signature
                </div>
            </div>
            <a href="#" class="print-button" onclick="printPage()">Print</a>
            <div class="footer">
                &copy; {datetime.now().year} UoG Community School. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html_content)

def print_admin_experience(request, admin_id):
    # Fetch the admin and their experience details
    admin = get_object_or_404(AdminStaffProfile, pk=admin_id)
    experiences = Experience.objects.filter(admin=admin)

    # Create the HTML content for the printable page
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin staff Experience</title>
        <style>
            .container {{
                width: 100%;
                max-width: 800px;
                margin: auto;
                font-family: Arial, sans-serif;
                position: relative;
            }}
            .header {{
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .header img {{
                max-width: 100px;
            }}
            .content {{
                border: 1px solid #333;
                padding: 20px;
                font-size: 16px;
                position: relative;
                z-index: 10;
            }}
            .watermark {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                opacity: 0.1;
                z-index: 0;
                pointer-events: none;
                max-width: 400px;
                width: 100%;
            }}
            .field {{
                margin: 10px 0;
            }}
            .label {{
                font-weight: bold;
            }}
            .signature {{
                margin-top: 40px;
                text-align: center;
            }}
            .print-button {{
                display: block;
                margin: 20px auto;
                padding: 10px 20px;
                background-color: #0070b8;
                color: white;
                text-align: center;
                border-radius: 5px;
                text-decoration: none;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 14px;
                color: #666;
            }}
            @media print {{
                .print-button {{
                    display: none;
                }}
            }}
        </style>
        <script>
            function printPage() {{
                window.print();
            }}
        </script>
    </head>
    <body onload="printPage()">
        <div class="container">
            <div class="header">
                <img src="https://ncee.org.uk/wp-content/uploads/2023/11/gondar.png" alt="Logo">
                <div>Admin Staff Experience</div>
            </div>
            <img src="https://ncee.org.uk/wp-content/uploads/2023/11/gondar.png" alt="Watermark" class="watermark">
            <div class="content">
                <div class="field"><span class="label">Full Name:</span> {admin.full_name_en}</div>
                <div class="field"><span class="label">Gender:</span> {admin.gender}</div>
                <div class="field"><span class="label">Job Title:</span> {admin.job_title}</div>
                <div class="field"><span class="label">Employee Status:</span> {admin.get_employee_status_display()}</div>

                <div class="field">
                    <span class="label">Experience:</span><br>
                    <ul>
                        {"".join([f"<li>{exp.institution} ({exp.position}) from {exp.from_date} to {exp.to_date} - {exp.net_duration}</li>" for exp in experiences])}
                    </ul>
                </div>
                
                <div class="signature">
                    __________________________<br>
                    Employee's Signature
                </div>
            </div>
            <a href="#" class="print-button" onclick="printPage()">Print</a>
            <div class="footer">
                &copy; {datetime.now().year} UoG Community School. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html_content)
