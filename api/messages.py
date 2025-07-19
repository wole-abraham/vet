def messages(date, last_name):
    return f"""
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Appointment Confirmation - VetCare Veterinary Center</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f8f9fa;
            }}
            
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            
            .header {{
                background: linear-gradient(135deg, #0d1b3f 0%, #1e3a8a 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            
            .logo {{
                font-size: 2.5rem;
                margin-bottom: 10px;
            }}
            
            .brand-name {{
                font-size: 1.8rem;
                font-weight: 700;
                margin-bottom: 5px;
            }}
            
            .tagline {{
                font-size: 1rem;
                opacity: 0.9;
                font-weight: 300;
            }}
            
            .content {{
                padding: 40px 30px;
            }}
            
            .success-icon {{
                text-align: center;
                margin-bottom: 30px;
            }}
            
            .success-icon .circle {{
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #27ae60, #2ecc71);
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 2.5rem;
                color: white;
                margin-bottom: 20px;
            }}
            
            .greeting {{
                font-size: 1.5rem;
                font-weight: 600;
                color: #0d1b3f;
                margin-bottom: 20px;
                text-align: center;
            }}
            
            .message {{
                font-size: 1.1rem;
                color: #555;
                margin-bottom: 30px;
                text-align: center;
            }}
            
            .appointment-details {{
                background: linear-gradient(135deg, #f7c873, #f39c12);
                border-radius: 15px;
                padding: 25px;
                margin: 30px 0;
                text-align: center;
                color: white;
            }}
            
            .appointment-details h3 {{
                font-size: 1.3rem;
                margin-bottom: 15px;
                font-weight: 600;
            }}
            
            .appointment-date {{
                font-size: 1.2rem;
                font-weight: 700;
                margin-bottom: 10px;
            }}
            
            .reminder {{
                background-color: #e8f4f8;
                border-left: 4px solid #3498db;
                padding: 20px;
                margin: 25px 0;
                border-radius: 8px;
            }}
            
            .reminder h4 {{
                color: #2c3e50;
                margin-bottom: 10px;
                font-size: 1.1rem;
            }}
            
            .reminder ul {{
                list-style: none;
                padding-left: 0;
            }}
            
            .reminder li {{
                margin-bottom: 8px;
                padding-left: 20px;
                position: relative;
            }}
            
            .reminder li:before {{
                content: "✓";
                position: absolute;
                left: 0;
                color: #27ae60;
                font-weight: bold;
            }}
            
            .cta-section {{
                text-align: center;
                margin: 35px 0;
            }}
            
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #f7c873, #f39c12);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 25px;
                font-weight: 600;
                font-size: 1.1rem;
                box-shadow: 0 4px 15px rgba(247, 200, 115, 0.3);
                transition: transform 0.2s ease;
            }}
            
            .cta-button:hover {{
                transform: translateY(-2px);
            }}
            
            .contact-info {{
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 25px;
                margin: 25px 0;
                text-align: center;
            }}
            
            .contact-info h4 {{
                color: #0d1b3f;
                margin-bottom: 15px;
                font-size: 1.1rem;
            }}
            
            .contact-item {{
                margin-bottom: 10px;
                font-size: 1rem;
            }}
            
            .contact-item strong {{
                color: #f39c12;
            }}
            
            .footer {{
                background-color: #0d1b3f;
                color: white;
                padding: 30px;
                text-align: center;
            }}
            
            .footer h4 {{
                margin-bottom: 15px;
                font-size: 1.2rem;
            }}
            
            .social-links {{
                margin: 20px 0;
            }}
            
            .social-links a {{
                display: inline-block;
                margin: 0 10px;
                color: #f7c873;
                text-decoration: none;
                font-size: 1.2rem;
            }}
            
            .footer-text {{
                font-size: 0.9rem;
                opacity: 0.8;
                margin-top: 20px;
            }}
            
            @media (max-width: 600px) {{
                .email-container {{
                    margin: 0;
                    box-shadow: none;
                }}
                
                .header, .content, .footer {{
                    padding: 20px 15px;
                }}
                
                .brand-name {{
                    font-size: 1.5rem;
                }}
                
                .logo {{
                    font-size: 2rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <!-- Header -->
            <div class="header">
                <div class="logo">❤️</div>
                <div class="brand-name">VetCare Veterinary Center</div>
                <div class="tagline">Compassionate Care for Your Beloved Pets</div>
            </div>
            
            <!-- Content -->
            <div class="content">
                <div class="success-icon">
                    <div class="circle">✓</div>
                </div>
                
                <div class="greeting">Appointment Confirmed!</div>
                
                <div class="message">
                    Dear {last_name},<br><br>
                    Your appointment has been successfully scheduled. We're excited to see you and your pet!
                </div>
                
                <!-- Appointment Details -->
                <div class="appointment-details">
                    <h3>📅 Your Appointment</h3>
                    <div class="appointment-date">{date}</div>
                    <p>Please arrive 10 minutes before your scheduled time</p>
                </div>
                
                <!-- Important Reminders -->
                <div class="reminder">
                    <h4>📋 Important Reminders</h4>
                    <ul>
                        <li>Bring your pet's current medications</li>
                        <li>Bring any recent medical records</li>
                        <li>Please keep your pet on a leash or in a carrier</li>
                        <li>Arrive 10 minutes early for check-in</li>
                    </ul>
                </div>
                
                <!-- Contact Information -->
                <div class="contact-info">
                    <h4>📞 Need to Reschedule?</h4>
                    <div class="contact-item">
                        <strong>Phone:</strong> (410) 555-0123
                    </div>
                    <div class="contact-item">
                        <strong>Emergency:</strong> (410) 555-9999
                    </div>
                    <div class="contact-item">
                        <strong>Email:</strong> info@vetcare.com
                    </div>
                </div>
                
                <!-- Call to Action -->
                <div class="cta-section">
                    <a href="https://vetcare.com" class="cta-button">Visit Our Website</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="footer">
                <h4>VetCare Veterinary Center</h4>
                <p>123 Veterinary Drive<br>Upper Vetcare, MD 21201</p>
                
                <div class="social-links">
                    <a href="#">📘</a>
                    <a href="#">🐦</a>
                    <a href="#">📷</a>
                    <a href="#">💼</a>
                </div>
                
                <div class="footer-text">
                    <p>Thank you for choosing VetCare for your pet's healthcare needs.</p>
                    <p>© 2024 VetCare Veterinary Center. All rights reserved.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """