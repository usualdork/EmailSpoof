# EmailSpoof
## Email Analyzer & Editor

A modern, responsive web app that lets you hack the very DNA of emails! Transform any .eml file into your digital playground—rewrite history by editing sent emails, forge headers that look legitimate, manipulate rich content, and craft perfect digital deceptions. It's email alchemy that breaks all the rules of digital communications! <br>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3c272e0b-60da-4410-9c8a-62b727832234">
</p> <br>


## Features

- **Dynamic Responsive UI**: Works seamlessly on both mobile and desktop devices
- **Light/Dark Theme Support**: Toggle between light and dark themes
- **Email Header Editing**: Add, modify, or remove email headers
- **Rich Body Editor**: Edit email body with either plain text or rich HTML editor
- **Attachment Management**: View, add, or remove email attachments
- **Live Preview**: See changes in real time with a built-in preview pane
- **Search Functionality**: Find content within the email body
- **Save & Export**: Save modifications back to a new .eml file

## Snapshots
<br>
<p align="center">
    Interface
  <img src="https://github.com/user-attachments/assets/2d1eb56f-b1f1-4ca7-b616-46ee8894a52a">
  <br>
</p>
<br>
<p align="center">
    Play around as much as you like
  <img src="https://github.com/user-attachments/assets/49b366c6-cfd5-4c4d-b6bb-979ed2286822">
  <br>
</p>
<br>
<p align="center">
  <img src="https://github.com/user-attachments/assets/3d8d76c7-7f3a-4821-bfb6-8579fd9bd153">
  <br>
  Dynamic menu for phones
</p>
<br>


## Installation

### Prerequisites

- Python 3.6+
- pip (Python package manager)

### Setup

1. Clone the repository
```bash
git clone https://github.com/usualdork/EmailSpoof
cd EmailSpoof
```
2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```
3. Install dependencies
```bash
pip install flask
```
4. Run the application
```bash
python emailspoof.py
```
5. Open your browser and navigate to:
```bash
http://localhost:5000
```

## Usage
1. **Upload an Email**: Click the "Upload" button and select an .eml file
2. **Edit Headers**: Add, modify, or remove email headers like Subject, From, To, etc.
3. **Edit Body**: Modify the email body using either plain text or rich text editor
4. **Manage Attachments**: View, add, or remove attachments
5. **Preview**: See how your email will look after changes
6. **Save**: Download your modified email as a new .eml file

<p align="center">
  <img src="https://github.com/user-attachments/assets/f6e2ae9e-51f0-4fe3-b977-7f61e0ea1320">
</p> <br>

## Technical Details

### Backend
- **Flask**: Lightweight Python web framework
- **Python email library**: For parsing and manipulating email files
- **Base64 encoding**: For handling email attachments

### Frontend
- **Responsive Design**: Custom CSS with mobile-first approach
- **Dynamic UI**: JavaScript for interactive elements and real-time preview
- **TinyMCE**: Rich text editor integration for HTML emails
- **Theme Switching**: Dynamic theme changes without page reload
<p align="center">
  <img src="https://github.com/user-attachments/assets/26150aea-c6cc-414f-a618-65701524bb7a">
</p> <br>

## Development
To contribute to this project:
  - Fork the repository
  - Create a feature branch
  - Commit your changes
  - Push to the branch
  - Create a new Pull Request

## Future Enhancements
- SMTP integration for sending emails
- Email template library
- Spell checking
- Signature management
- Email validation
- Batch processing of multiple emails

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
1. TinyMCE for the rich text editor
2. Flask for the web framework

## Contact
If you have any questions or suggestions, feel free to open an issue or contact me **@usualdork**
