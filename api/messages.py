def messages(date, last_name):
    return f"""
      <!DOCTYPE html>
      <html lang='en'>
      <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Appointment Booked</title>
        <style>
          body {{
            background: #181f2a;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            font-family: 'Segoe UI', 'Arial', sans-serif;
          }}
          .booked-card {{
            background: #232b3b;
            border-radius: 22px;
            box-shadow: 0 8px 32px rgba(39,174,96,0.18);
            padding: 48px 32px 36px 32px;
            max-width: 400px;
            width: 95vw;
            text-align: center;
            color: #fff;
            margin: 32px auto;
            animation: popin 0.5s cubic-bezier(.68,-0.55,.27,1.55);
          }}
          .booked-card h2 {{
            color: #27ae60;
            font-size: 2em;
            margin-bottom: 18px;
            font-weight: 700;
            letter-spacing: 0.01em;
          }}
          .booked-card p {{
            font-size: 1.15em;
            color: #bfc9d8;
            margin-bottom: 28px;
            line-height: 1.5;
          }}
          .booked-btn {{
            display: inline-block;
            margin-top: 8px;
            padding: 12px 32px;
            background: #27ae60;
            color: #fff;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1em;
            box-shadow: 0 2px 8px rgba(0,0,0,0.10);
            transition: background 0.18s, color 0.18s, transform 0.15s;
          }}
          .booked-btn:hover {{
            background: #219150;
            color: #fff;
            transform: translateY(-2px) scale(1.03);
          }}
          @keyframes popin {{
            0% {{ transform: scale(0.85); opacity: 0; }}
            100% {{ transform: scale(1); opacity: 1; }}
          }}
        </style>
      </head>
      <body>
        <div class='booked-card'>
          <h2>Appointment Booked!</h2>
          <h3>Dear {last_name}</h3>

          <p>Your appointment has been successfully booked.<br>We look forward to seeing you and your pet!</p>
          <p>Time: {date}
          <a href='index.html' class='booked-btn'>Back to Home</a>
        </div>
      </body>
      </html>
      """