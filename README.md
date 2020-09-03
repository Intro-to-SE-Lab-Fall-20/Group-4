# Group-4
Intro to SE Lab Section 03 Group 4


## Polymail
### Description
Polymail is a user-friendly web-based email client which seamlessly interfaces with multiple email service providers (gmail, yahoo, etc.). Polymail provides the user with the ability to quickly compose, edit, send, and forward emails to any email address. Emails can be formatted before sending by including italicized and bold text, as well as non-ASCII characters. Emails can also be supplemented with attachments of various media types including common document, audio, and video formats. Efficient searching through emails is also integrated through the use of user-provided keywords. Finally, Polymail is presented in an intuitive browser-based user interface to maximize user productivity and satisfaction.


### Objective
Polymail aims to be a reinvention of the popular email systems that are used by applications such as Gmail, Yahoo.com, and Outlook. Users at any experience level should be able to use Polymail, so our UI should be intuitive and easy to navigate around received and sent emails and different email functionalities, including composing, editing, sending, and forwarding emails as well as adding attachments. Polymail navigation will be aided by a search bar, which will assist users in quickly finding specific emails. 


### Features
##### Email account authentication for Google users
Google account holders will be able to sign in to Polymail securely by using the OAuth2 protocol. Persistent login during a user's session is required to prevent having to repeatedly login, and automatic sign out after a period of inactivity will also be available to avoid unauthorized users accessing Polymail on someone else's machine.

##### Compose, edit, send, and forward email messages
Polymail allows users to use basic email functionality including composing new messages, editing existing messages or drafts, and sending and forwarding emails to other email accounts including those outside of Polymail's supported email providers. Within these emails, Polymail will allow utilization of special characters beyond ASCII as well as bold and italicized text.

##### Search for matching emails
A search box will be available above the inbox where users can search for emails fitting the criteria that they fill into the field. The emails will be filtered by using a keyword search algorithm, and the resulting emails will be displayed in a list format for easy access and viewing.

##### Email attachments
While editing emails, an "Add attachment" option will be displayed in the window which will allow users to add an attachment from their local machine to the email. Various file types will be available for attachment including common text, image, audio, and video formats. This attachment will be bundled with the message and sent to the user alongside it. For emails with attachments, the send feature will wait for the attachments to finish uploading to send the email to avoid sending incomplete packages. This feature will be integrated with Windows and macOS file browsers for reliable image selection and attachment.
