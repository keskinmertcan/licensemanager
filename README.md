
# License Manager

License Manager is a desktop application built using Python and Tkinter for managing users, servers, and license information. It is intended to help administrators manage licenses and servers in a convenient GUI.

## Features

- **User Management**: Add, edit, and search users. Users can be set as active or inactive, and their permissions can be managed effectively.
- **Server Management**: Add, edit, and search servers associated with users. Check server limits based on user licenses.
- **Admin Functionality**: Only root users can access certain functionalities like viewing logs and managing other admins.
- **User Authentication**: A login screen ensures that only authorized users can access the system. Admin users have additional privileges.
- **Configurable Database**: The application reads the database connection information from a `config.ini` file, making it easy to configure for different environments.

## Requirements

- Python 3.x
- Tkinter
- mysql-connector-python
- ConfigParser

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/keskinmertcan/license-manager.git
   ```
2. Install the required Python libraries:
   ```bash
   pip install mysql-connector-python
   ```
3. Create a `config.ini` file in the root directory of the project and provide the database configuration:
   ```ini
   [database]
   host = your-database-host
   user = your-database-user
   password = your-database-password
   database = your-database-name
   ```
4. Run the application:
   ```bash
   python licensemanager.py.py
   ```

## Usage

- On running the application, the login screen will prompt for a username and password.
- Once logged in, users with sufficient privileges can manage other users, servers, and view logs.
- The menu bar provides access to various management functions such as adding and updating users or servers.
- Admin users have an additional menu for admin-specific functions like managing other administrators and viewing system logs.

## Screens

1. **Login Screen**: Allows users to authenticate themselves.
2. **User Management**: Add, update, or search for users.
3. **Server Management**: Manage servers associated with users.
4. **Admin Management (Root Users Only)**: View and manage other administrators.

## Configurations

- **Database Configuration**: All database details are fetched from the `config.ini` file.

## Security

- The system enforces role-based access, where root users have privileges that regular users do not have.
- Passwords are stored securely, and inactive users cannot access the system.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any queries, reach out to:
- **Mertcan Keskin** - Software Developer at Eray Teknoloji A.Ş.

## Contributing

Feel free to submit pull requests or raise issues if you would like to contribute to the project. Any help is welcome!

---

This project is a collaborative effort, and its goal is to provide a reliable solution for managing licenses and servers, especially for  Mobile Reports.

### Notes

- **Root User Only Features**: Only root users can view logs and manage other admin users.
- **Multi-Language Support**: Currently, the application is in English, but future versions may include multiple language support.
