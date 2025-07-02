import re
import smtplib
import ssl
from email.message import EmailMessage
import imaplib
import email
from email import policy
import os
from dotenv import load_dotenv
from colorama import Fore, init

# Initialize colorama
init()

# Native Imports
from kun import known_user_names

# Load environment variables from .env file
load_dotenv()

# Email credentials
EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("SENDER_PASSWORD")

# Establish an SSL context for secure communication
ssl_context = ssl.create_default_context()

def send_mail(prompt):
    """
    Parses the prompt to extract email addresses, subject, and message body, then sends the email(s).
    Returns a tuple (success, message), where success is True if emails were sent, False otherwise.
    """
    
    emails = []
    subject = None
    body = None

    # 1. Extract Email Addresses and ARPA IDs
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', prompt)
    arpa_ids = re.findall(r'\b([A-Z]\d{3})\b', prompt)  # Matches patterns like R001, A001, etc.

    # 2. Map Known Contact Names and ARPA IDs to Emails
    known_contacts = {}
    for user, details in known_user_names.items():
        if details['mail']:  # Check if mail is not empty
            # Add full name
            known_contacts[details['full_name'].lower()] = details['mail']
            # Add call name
            known_contacts[details['call_name'].lower()] = details['mail']
            # Add ARPA ID
            known_contacts[details['arpa_id']] = details['mail']

    # Replace names and ARPA IDs with emails
    for identifier, email in known_contacts.items():
        if re.search(r'\b' + re.escape(identifier) + r'\b', prompt, re.IGNORECASE):
            emails.append(email)

    # Add emails from ARPA IDs
    for arpa_id in arpa_ids:
        for user, details in known_user_names.items():
            if details['arpa_id'] == arpa_id and details['mail']:
                emails.append(details['mail'])

    # Remove Duplicate Emails
    emails = list(set(emails))

    # 3. Validate Number of Recipients
    if len(emails) == 0:
        return False, "Error: No valid email addresses or known contacts found in the prompt."
    if len(emails) > 5:
        return False, "Error: Cannot send to more than 5 email addresses at once."

    # 4. Define Keywords for Subject and Body
    subject_pattern = r'(subject)\s*([\'"])(.*?)\2'
    body_pattern = r'(body|content|message)\s*([\'"])(.*?)\2'

    # 5. Search for Subject and Body
    subject_match = re.search(subject_pattern, prompt, re.IGNORECASE)
    if subject_match:
        subject = subject_match.group(3)

    body_match = re.search(body_pattern, prompt, re.IGNORECASE)
    if body_match:
        body = body_match.group(3)

    # Fallback for Subject or Body if not explicitly found
    if not subject or not body:
        quotes = re.findall(r'(["\'])(.*?)\1', prompt)
        if not subject and len(quotes) > 1:
            subject = quotes[1][1]
        if not body and quotes:
            body = quotes[0][1]

    if not subject:
        return False, "Error: No subject found in the prompt."
    if not body:
        return False, "Error: No message body found in the prompt."

    # HTML Signature
    signature_html = """
    <div style="font-family: 'Courier New', monospace; color: #0000FF;">
        <!-- Divider symbol -->
        <p style="font-size: 12px; color: #0000FF; margin: 8px 0; text-align: left;">~</p>
        <!-- ASCII Logo with reduced font size for compact display -->
        <pre style="font-size: 10px; line-height: 1; margin: 0; text-align: center;">

 ██████  ██████  ███████ ██ ██ ███████  
██    ██ ██   ██ ██      ██ ██ ██       
██    ██ ██████  ███████ ██ ██ █████    
██    ██ ██           ██ ██ ██ ██       
 ██████  ██      ███████ ██ ██ ███████  
        </pre>
        
        <!-- Header text in 12px font size, no max-width restriction -->
        <p style="font-size: 12px; color: #0000FF; margin: 8px 0; text-align: center;">
            A Self-Centered Intelligence (SCI) Prototype<br>
            By ARPA HELLENIC LOGICAL SYSTEMS<br>
            Version: 0.3.79 XP | 01 JUL 2025
        </p>
        
        <!-- Divider symbol -->
        <p style="font-size: 12px; color: #0000FF; margin: 8px 0; text-align: center;">~</p>
        
        <!-- Disclaimer section with left alignment and smaller font size, no width restriction -->
        <p style="font-size: 10px; color: grey; font-style: italic; text-align: left; margin: 0 auto 10px;">
            This message was generated and disseminated by Non-Humanoid Intelligence Units (NHUIs) operating under the auspices of ARPA Corporation.
            All email accounts managed by ARPA's SCI, AA, NHUI, and AI models are part of experimental frameworks and are intended solely for demonstration and authorized operational purposes.
        </p>
        <p style="font-size: 11px; color: grey; font-style: italic; text-align: left; margin: 0 auto;">
            Unauthorized receipt or distribution of this email is strictly prohibited. If you have received this communication in error or are not the intended recipient, 
            you are hereby instructed to permanently delete this email from all systems and notify ARPA Hellenic Logical Systems immediately.
            Sharing, copying, or distributing the contents of this email without explicit written consent from ARPA Corporation is forbidden 
            and may result in disciplinary action.
        </p>
    </div>
    """

    # Combine message body with the signature
    html_body = f"<div>{body}</div><br><br>{signature_html}"

    try:
        # Email configuration
        sender_email = EMAIL
        sender_password = PASSWORD

        if not sender_email or not sender_password:
            return False, "Error: Email credentials not set in environment variables."

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Create the Email Message
        msg = EmailMessage()
        msg['From'] = f'"Opsie by ARPA" <{sender_email}>'
        msg['To'] = ', '.join(emails)
        msg['Subject'] = subject
        msg.set_content(body)  # Plain text fallback
        msg.add_alternative(html_body, subtype='html')  # HTML version with signature

        # Send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True, f"Email sent successfully to {', '.join(emails)}."

    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def fetch_unread_primary_emails():
    """
    Fetches the latest 10 unread emails from the primary inbox only.
    Each email dictionary includes sender, subject, date, and read/unread status.
    """
    inbox = []
    with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")  # Open the primary inbox

        # Fetch only unread emails in the inbox
        result, data = mail.search(None, 'UNSEEN')
        email_ids = data[0].split()[-10:]  # Get up to the last 10 unread emails

        for i, email_id in enumerate(reversed(email_ids), 1):
            result, msg_data = mail.fetch(email_id, "(RFC822)")
            raw_msg = msg_data[0][1]
            msg = email.message_from_bytes(raw_msg, policy=policy.default)

            # Parse email details for display
            sender = email.utils.parseaddr(msg['From'])[1]
            subject = msg.get("Subject", "No Subject")
            date = msg.get("Date")

            inbox.append({
                'index': i,
                'sender': sender,
                'subject': subject,
                'date': date,
                'id': email_id,
                'unread': True  # We are fetching only unread emails
            })

    return inbox

def extract_body(msg):
    """
    Extracts the body from a message, checking for both plain text and HTML parts.
    """
    # Check if the email is multipart
    if msg.is_multipart():
        # Loop through each part and find plain text or HTML
        for part in msg.iter_parts():
            if part.get_content_type() == "text/plain" and part.get_content_disposition() != "attachment":
                return part.get_payload(decode=True).decode()
            elif part.get_content_type() == "text/html" and not part.get_content_disposition() == "attachment":
                # If we don't find plain text, return HTML (with a warning)
                html_body = part.get_payload(decode=True).decode()
                return strip_html_tags(html_body)
    else:
        # If it's not multipart, just return the raw text (we assume it's plain text)
        return msg.get_payload(decode=True).decode()

    return "No readable content found"

def strip_html_tags(html):
    """
    Strips HTML tags from a string and returns plain text.
    """
    clean = re.compile("<.*?>")
    return re.sub(clean, "", html)

def display_unread_inbox(inbox):
    """
    Displays a list of unread emails in the inbox with DNA report-style formatting.
    """
    unread_count = len(inbox)

    print(Fore.LIGHTCYAN_EX + "\n" + "═" * 80)
    print(Fore.LIGHTCYAN_EX + """
    ██ █▄ █ ▀█▀ █▀▀ █▀█ █▀█ █   ▄▀█ █▄ █ █▀▀ ▀█▀ ▄▀█ █▀█ █▄█
    █▄ █ ▀█  █  ██▄ █▀▄ █▀▀ █▄▄ █▀█ █ ▀█ ██▄  █  █▀█ █▀▄  █ 
    
    █▀▄▀█ ▄▀█ █ █     █▀ █▀▀ █▀█ █ █ █ █▀▀ █▀▀
    █ ▀ █ █▀█ █ █▄▄   ▄█ ██▄ █▀▄ ▀▄▀ █ █▄▄ ██▄
                                          
              v0.3.79 XP | ARPA CORP, 2025
    """)
    print(Fore.LIGHTCYAN_EX + "═" * 80)
    
    print(Fore.LIGHTGREEN_EX + "\n[IMS] Primary Inbox Status:")
    print(Fore.LIGHTGREEN_EX + f"[IMS] Unread Messages: {unread_count}")
    print(Fore.LIGHTGREEN_EX + "[IMS] Temporal Window: Last 10 Messages\n")

    print(Fore.LIGHTCYAN_EX + "═" * 80)
    print(Fore.WHITE + "   #  |  STATUS  |     SENDER     |     SUBJECT     |     DATE")
    print(Fore.LIGHTCYAN_EX + "═" * 80)

    for email_info in inbox:
        status = Fore.LIGHTYELLOW_EX + "[UNREAD]" if email_info['unread'] else Fore.GREEN + "[READ]"
        # Truncate long fields for better formatting
        sender = email_info['sender'][:20] + '...' if len(email_info['sender']) > 20 else email_info['sender']
        subject = email_info['subject'][:20] + '...' if len(email_info['subject']) > 20 else email_info['subject']
        
        print(f"{Fore.WHITE}{email_info['index']:3d}  |  {status:8}  |  {Fore.WHITE}{sender:20}  |  {subject:20}  |  {email_info['date']}")
        print(Fore.LIGHTCYAN_EX + "─" * 80)

    print(Fore.LIGHTYELLOW_EX + "\n[IMS] Available Commands:")
    print(Fore.WHITE + "• Enter message number to read.")
    print(Fore.WHITE + "• Type 'exit' to return to main interface")
    print(Fore.LIGHTCYAN_EX + "═" * 80 + "\n")

def read_email(inbox, email_index):
    """
    Displays the selected email with DNA report-style formatting.
    """
    selected_email = inbox[email_index - 1]

    with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        result, msg_data = mail.fetch(selected_email['id'], "(RFC822)")
        raw_msg = msg_data[0][1]
        msg = email.message_from_bytes(raw_msg, policy=policy.default)

        sender_name, sender_email = email.utils.parseaddr(msg['From'])
        subject = msg.get("Subject", "No Subject")
        date = msg.get("Date")
        body = extract_body(msg)

        print(Fore.LIGHTCYAN_EX + "\n" + "═" * 80)
        print(Fore.LIGHTGREEN_EX + "[MESSAGE DETAILS]")
        print(Fore.LIGHTCYAN_EX + "═" * 80)
        
        print(Fore.LIGHTYELLOW_EX + "FROM:")
        print(Fore.WHITE + f"{sender_name} <{sender_email}>")
        
        print(Fore.LIGHTYELLOW_EX + "\nSUBJECT:")
        print(Fore.WHITE + subject)
        
        print(Fore.LIGHTYELLOW_EX + "\nDATE:")
        print(Fore.WHITE + date)
        
        print(Fore.LIGHTCYAN_EX + "\n" + "─" * 80)
        print(Fore.LIGHTYELLOW_EX + "CONTENT:")
        print(Fore.WHITE + body)
        
        print(Fore.LIGHTCYAN_EX + "\n" + "═" * 80)
        print(Fore.LIGHTYELLOW_EX + "[IMS] Available Commands:")
        print(Fore.WHITE + "• Type 'reply' to compose response")
        print(Fore.WHITE + "• Type 'inbox' to return to message list")
        print(Fore.WHITE + "• Type 'exit' to return to main interface")
        print(Fore.LIGHTCYAN_EX + "═" * 80 + "\n")

    return selected_email

def reply_to_email(selected_email):
    """
    Handles email reply with DNA report-style formatting.
    Returns a tuple (success, message) where success is True if email was sent successfully.
    """
    print(Fore.LIGHTCYAN_EX + "\n" + "═" * 80)
    print(Fore.LIGHTGREEN_EX + "[COMPOSE REPLY]")
    print(Fore.LIGHTCYAN_EX + "═" * 80)
    
    print(Fore.LIGHTYELLOW_EX + "TO:")
    print(Fore.WHITE + selected_email['sender'])
    
    print(Fore.LIGHTYELLOW_EX + "\nSUBJECT:")
    print(Fore.WHITE + f"Re: {selected_email['subject']}")
    
    print(Fore.LIGHTYELLOW_EX + "\nMESSAGE:")
    reply_body = input(Fore.WHITE)

    print(Fore.LIGHTCYAN_EX + "\n" + "─" * 80)
    print(Fore.LIGHTYELLOW_EX + "[SYSTEM] Sending reply...")

    reply_msg = EmailMessage()
    reply_msg['From'] = f'"Opsie by ARPA" <{EMAIL}>'
    reply_msg['To'] = selected_email['sender']
    reply_msg['Subject'] = f"Re: {selected_email['subject']}"
    reply_msg.set_content(reply_body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl_context) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(reply_msg)

        print(Fore.LIGHTGREEN_EX + "[SYSTEM] Reply sent successfully.")
        print(Fore.LIGHTCYAN_EX + "═" * 80 + "\n")
        return True, f"Reply sent successfully to {selected_email['sender']} regarding '{selected_email['subject']}'"

    except Exception as e:
        error_msg = f"[ERROR] Failed to send reply: {str(e)}"
        print(Fore.RED + error_msg)
        print(Fore.LIGHTCYAN_EX + "═" * 80 + "\n")
        return False, error_msg

def inbox_interaction():
    """
    Manages interaction with the inbox, allowing reading, replying, and navigating back to conversation mode.
    """
    inbox = fetch_unread_primary_emails()
    display_unread_inbox(inbox)

    while True:
        choice = input(Fore.LIGHTYELLOW_EX + "\n[INPUT] Select email number or 'exit': " + Fore.WHITE)
        if choice.lower() == 'exit':
            print(Fore.LIGHTGREEN_EX + "[SYSTEM] Returning to main interface...")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(inbox):
            email_index = int(choice)
            selected_email = read_email(inbox, email_index)

            while True:
                action = input(Fore.LIGHTYELLOW_EX + "\n[INPUT] Enter command: " + Fore.WHITE)
                if action == 'reply':
                    reply_to_email(selected_email)
                    print(Fore.LIGHTGREEN_EX + "[SYSTEM] Returning to inbox...")
                    display_unread_inbox(inbox)
                    break
                elif action == 'inbox':
                    display_unread_inbox(inbox)
                    break
                elif action == 'exit':
                    print(Fore.LIGHTGREEN_EX + "[SYSTEM] Returning to main interface...")
                    return
                else:
                    print(Fore.RED + "[ERROR] Invalid command. Please try again.")


# comment out ''' ''' to test
'''
def main():
    """
    Main test loop for the email functionality.
    """
    print(Fore.LIGHTCYAN_EX + "\n" + "═" * 80)
    print(Fore.LIGHTGREEN_EX + """
    ╔═══════════════════════════════════════════╗
    ║            IMS Agent Test Loop            ║
    ╚═══════════════════════════════════════════╝
    """)
    
    while True:
        print(Fore.LIGHTYELLOW_EX + "\nAvailable Commands:")
        print(Fore.WHITE + "1. Check Inbox")
        print(Fore.WHITE + "2. Send New Email")
        print(Fore.WHITE + "3. Exit")
        
        choice = input(Fore.LIGHTYELLOW_EX + "\n[INPUT] Enter command number: " + Fore.WHITE)
        
        if choice == "1":
            inbox_interaction()
        elif choice == "2":
            prompt = input(Fore.LIGHTYELLOW_EX + "\n[INPUT] Enter email details (format: email@example.com subject 'Subject' body 'Message'): " + Fore.WHITE)
            success, message = send_mail(prompt)
            print(Fore.LIGHTGREEN_EX if success else Fore.RED + f"\n[SYSTEM] {message}")
        elif choice == "3":
            print(Fore.LIGHTGREEN_EX + "\n[SYSTEM] Exiting email system...")
            break
        else:
            print(Fore.RED + "\n[ERROR] Invalid command. Please try again.")

if __name__ == "__main__":
    main()
    '''