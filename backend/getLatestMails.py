from agno.agent import Agent
from agno.tools.gmail import GmailTools
from agno.tools import tool
import os
import base64


# @tool()
# def save_attachments(service, user_id="me", msg_id=None, download_folder="attachments"):
#     """
#     Download all attachments from a specific Gmail message and save them locally.

#     Args:
#         service: Authorized Gmail API service instance created using googleapiclient.discovery.build.
#         user_id: The user's email address or "me" to indicate the authenticated user. Defaults to "me".
#         msg_id: The ID of the Gmail message from which attachments will be downloaded.
#         download_folder: The local directory where attachments will be saved. Defaults to "attachments".

#     Returns:
#         None. Saves attachments as files in the specified download folder.

#     Raises:
#         googleapiclient.errors.HttpError: If there is an issue with the Gmail API request.
#         FileNotFoundError: If the specified download folder cannot be created.
#         ValueError: If no message ID is provided or the message has no attachments.
#     """
#     if not os.path.exists(download_folder):
#         os.makedirs(download_folder)

#     message = service.users().messages().get(userId=user_id, id=msg_id).execute()

#     # Check for parts (attachments)
#     parts = message.get("payload", {}).get("parts", [])
#     for part in parts:
#         filename = part.get("filename")
#         body = part.get("body", {})
#         attachment_id = body.get("attachmentId")

#         if filename and attachment_id:
#             # Get attachment content
#             attachment = (
#                 service.users()
#                 .messages()
#                 .attachments()
#                 .get(userId=user_id, messageId=msg_id, id=attachment_id)
#                 .execute()
#             )

#             file_data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))

#             # Save locally
#             filepath = os.path.join(download_folder, filename)
#             with open(filepath, "wb") as f:
#                 f.write(file_data)
#             print(f"✅ Downloaded: {filename}")


# agent = Agent(tools=[GmailTools(port=8080),save_attachments])
# agent.print_response("Show me my latest 5 unread emails and give me message ids and download any one with attachment", markdown=True)


from agno.agent import Agent
from agno.tools.gmail import GmailTools
from agno.tools import tool
import os

@tool()
def save_attachments(msg_id: str, download_folder: str = "attachments", gmail: GmailTools | None = None):
    """
    Download all attachments from a specific Gmail message using Agno GmailTools.

    Args:
        msg_id: The Gmail message ID to download attachments from.
        download_folder: Local folder to save attachments. Defaults to 'attachments'.
        gmail: The GmailTools instance passed by the agent.

    Returns:
        list[str]: List of file paths for downloaded attachments.

    Raises:
        ValueError: If no attachments are found for the message.
        OSError: If the download folder cannot be created or written to.
    """
    if gmail is None:
        raise ValueError("GmailTools instance not provided. It must be in the Agent's tools list.")

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Get the message via GmailTools
    message = gmail.get_latest_emails(count=1)  # or get_unread_emails(), etc.
    message = [m for m in message if m['id'] == msg_id]
    if not message:
        raise ValueError(f"No message found with ID: {msg_id}")
    message = message[0]

    saved_files = []

    for part in message.get("payload", {}).get("parts", []):
        filename = part.get("filename")
        body = part.get("body", {})
        attachment_id = body.get("attachmentId")

        if filename and attachment_id:
            filepath = os.path.join(download_folder, filename)
            gmail.download_attachment(msg_id=msg_id, attachment_id=attachment_id, filename=filepath)
            saved_files.append(filepath)
            print(f"✅ Downloaded: {filename}")

    if not saved_files:
        raise ValueError(f"No attachments found for message ID: {msg_id}")

    return saved_files


# Initialize agent
gmail_tool = GmailTools(port=8080)
agent = Agent(tools=[gmail_tool, save_attachments])

agent.print_response(
    "Show me my latest 5 unread emails and download attachments from one of them",
    markdown=True
)



# export GOOGLE_CLIENT_ID="474704076992-iivttmanto6fdtie28u8l7e5m5u0cjkm.apps.googleusercontent.com"
# export GOOGLE_CLIENT_SECRET="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"
# export GOOGLE_PROJECT_ID="steam-bruin-471814-k0"
# export GOOGLE_REDIRECT_URI=http://localhost  # Default value


