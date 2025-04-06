# ClubConnect

ClubConnect is a web application designed to help manage clubs, events, and announcements. It provides an administrative dashboard for club managers to efficiently organize and communicate with club members.

## Features

- **Club Management**: Create and manage multiple clubs
- **Event Scheduling**: Plan and organize club events
- **Announcements**: Post important updates to club members
- **Admin Dashboard**: Comprehensive administrative interface
- **User Authentication**: Secure login system for administrators

## Technologies Used

- Django
- HTML/CSS
- JavaScript
- Bootstrap
- Font Awesome

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/clubconnect.git
   cd clubconnect
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`

## Usage

- Access the admin dashboard at `/admin/`
- Log in with your superuser credentials
- Manage clubs, events, and announcements through the dashboard

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django framework
- Bootstrap for UI components
- Font Awesome for icons 