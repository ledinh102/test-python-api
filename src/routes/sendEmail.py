from fastapi import APIRouter, HTTPException
import asyncio
from src.config.db import prismaConnection
import os
import smtplib
import ssl
from pydantic import BaseModel
from email.message import EmailMessage
from dotenv import load_dotenv
from typing import Optional
import logging

load_dotenv()

email_sender = "dndtranslatesite@gmail.com"
email_password = os.getenv("EMAIL_PASSWORD")


class ComposeEmail(BaseModel):
    toEmail: str
    subject: Optional[str] = None
    url: Optional[str] = None


router = APIRouter()


from fastapi import HTTPException


@router.post("/send-email", tags=["send-email"])
async def sendEmail(sendEmail: ComposeEmail):
    try:
        user = await prismaConnection.prisma.user.find_first(
            where={"email": sendEmail.toEmail}
        )
        if user is None:
            logging.error("User not found")
            raise HTTPException(status_code=404, detail="Email not exist in the system")

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error fetching user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    try:
        message = EmailMessage()
        message["From"] = email_sender
        message["To"] = sendEmail.toEmail
        message["Subject"] = "You have an invitation to a video call!"
        message.set_content(f"Click here to redirect to video calling: {sendEmail.url}")

        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=ssl.create_default_context()
        ) as smtp:
            smtp.login(email_sender, email_password)
            await asyncio.get_event_loop().run_in_executor(
                None, smtp.send_message, message
            )

        return {"message": "Email sent successfully"}
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send email")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
