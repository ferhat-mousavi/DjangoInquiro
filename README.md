# DjangoInquiro

**DjangoInquiro** is an open-source Q&A platform developed with Django, inspired by Stack Overflow. This project allows users to post questions, answer questions, and add comments to both questions and answers. The structure is designed to support modular development and expandability.

## Project Structure

- **answers**: This app manages answers for the questions. Each answer is related to a specific question and includes fields for content, author, and timestamps.
- **comments**: This app handles comments on both questions and answers, allowing users to add brief comments for further discussion.
- **django_inquiro**: The main project configuration and settings are stored here. This app serves as the core of the project, managing overall configurations and root URL routing.
- **home**: Contains views and templates for the homepage and other general views. The homepage displays the latest questions and allows easy navigation.
- **profiles**: Manages user profiles and stores information about each user’s activity on the platform, such as their questions, answers, and comments.
- **questions**: This app is responsible for managing the questions posted by users. Each question is associated with a user (author) and contains fields for the title, content, and timestamp.

## Getting Started

### Prerequisites
- Python 3.13
- Django 5.1.2
- Virtual environment setup (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ferhat-mousavi/DjangoInquiro.git
   cd DjangoInquiro
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Open your browser and navigate to `http://127.0.0.1:8000/admin` to access the Django admin panel. Log in with the superuser account you created earlier.

8. In the admin panel, go to the **Profiles** section. Here, create a profile for the superuser by linking it to the corresponding user. This profile setup will ensure the user can fully interact with the platform, including asking questions, answering, and commenting.

9. Then, navigate to `http://127.0.0.1:8000/` to access the main platform.

## Features

- **Question Posting**: Users can post questions with detailed descriptions.
- **Answer Submission**: Users can provide answers to questions and engage with other users’ inquiries.
- **Commenting**: Comments can be added to both questions and answers, facilitating further discussions.
- **User Profiles**: Each user has a profile page displaying their activity, including the questions they've asked and answered.
- **Admin Panel**: Django’s built-in admin interface for managing users and content.

## Contributing

Contributions are welcome! If you’d like to contribute to this project, please fork the repository and submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/YourFeature`)
3. Commit your Changes (`git commit -m 'Add YourFeature'`)
4. Push to the Branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU License.
