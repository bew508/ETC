# ETC

ETC is my Final Project for Harvard Class S-33a.

It is also a website for the school club ETC (Event Tech Crew). After submission as a final project, I will likely continue work on this and attempt to implement it into the club.

## Installation

Create a new folder. Drop the .zip file into it and unzip it. Then run the following commands.

Windows:

```bat
python -m venv env

python install -r requirements.txt

run.bat
````

Mac:

```bash
python3 -m venv env

python3 install -r requirements.txt

source run.sh
```

Now create a file called .env in the same file as the settings are in. In there, write the following code:

```env
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

Now fill in each value with your email account's information.

## License

[MIT](https://choosealicense.com/licenses/mit/)

# App Modules

## Global

### Templates

`layout.html`: The base layout for all html files in the project. It creates the navbar, imports the logo image, sets the favicon, and imports the global styling file as well as [purecss.io](https://purecss.io). It also creates two blocks: one for heading files such as styling or scripts, the other for the page body. The nav-bar links to common pages of the application such as *Home*, *Events*, and *About Us*. It also links to the *Log In*/*Log Out* page, depending on the authentication status of the user.

### Static

`layout.css`: Global styling file. Imported via *layout.html*. Sets styling for the navbar, the body, and form error messages. Also handles mobile friendliness of the website by increasing text size and stretching the nav-bar vertically.

`images`: Contains the logo image and will contain future images that are required to be accessed in several apps.

---

## Home

### Views

`index`: This view returns the home page of the website.

### Templates

`index.html`: HTML file for the home page. Gives a quick blurb about what the ETC is.

---

## Users

### Models

`User`: Extends the *AbstractUser* model. Modifies the *AbstractUser* model by setting a custom model manager *UserManager*, setting the default username field to be the email field, and deleting the username field. This website only allows it's member to join as users so every User account is created by an administrator and must be activated by the user on the first log-in. This status is tracked by the *activated* field. Additionally, two choice fields (one required, one unique) create the options for roles users can have. A user must have one common role--assigned upon account creation by the administrator--and may have a unique role in addition--assigned in the same way.

### Managers

`UserManager`: This custom manager for the custom *User* model extends the *BaseUserManager*. It only overrides the *create_user()* method and changes it to require a first name, last name, and email instead of it needing a username. It also creates the password inside the method by splicing the first and last name together with a seperating period. It makes use of the *set_password()* method for password hashing.

### Views

`index`: Returns the HTML for the user's account page. 

`login_view`: First, this view redirects any already logged in users back to the home page. Then it presents a form for the user to log in with their email address and password. On submission of this form, a user is identified. Should the user's account not yet be activated, i.e. this is their first log-in, the user is then shown another form where they must put in a new password and confirm it. This password is validated by the django default password validator function. All errors are passed back to the user. Upon successful password creation, the user is logged in and redirected to the home page.

`logout_view`: This view logs the user out and redirects them to the home page. Obviously, this page is protected via *login_required* decorator.

`list`: Returns an HTML page filled with all user information. This user information is passed to the website. This page is protected with a custom *unique_role_required* decorator.

`create_account`: The creation of accounts is only accessible to users that have a unique role. A list of available unique roles and common roles is passed on to the HTML so that all available options can be properly displayed. Once the administrator creates the account, an email is sent to the email associated with the account containing log-in information. The account registration process automatically identifies if an email is already registered to an account and provides the user with the error message.

`remove`: POST requests only. Also requires a unique role. Deletes the model entry for the user.

### Decorators

`minimum_role_required`: This custom decorator extends the *login_required* decorator by checking not only if the user is authenticated but also if the user posesses at minimum a certain role which the function takes as an argument. There is a ranking of roles with unique roles being valued higher than common roles. The decorator performs several checks to ensure that the user has either the role in question or any role that is valued more.

`unique_role_required`: This custom decorator simplifies the functionality of the *minimum_role_required* decorator by calling the aforementioned with the lowest unique role. This ensures that anyone with a unique role will pass this decorator.

### Templates

`activate.html`: Activation page for new accounts. Has a form with a field for a new password and a confirmation to retype the password. Also includes a hidden field to pass the user id on. Displays errors with *error* class at the top.

`create_account.html`: Site for the creation of a new account. Has *input* elements for First Name, Last Name, Email as well as *select* elements for unique role and common role. The unique role field will be hidden if there are no more unique roles available. The common role automatically selects a role while the unique role has a default value of None. All other values of unique and common roles are passed through django. The page also informs the administrator of the login information for the account they are creating should they want to pass this on to the user.

`index.html`: User page. Displays information about the user such as their full name and role(s).

`login.html`: Requires an email and a password to be filled into the form so the user can be logged in. All error messages are displayed at the top of the page once they occur.

`user_list.html`: Lists all users that currently exist in a table format as well as information about them such as their user id, first and last name, email, roles, and whether or not this account was activated yet.  This information is passed through django. This page also allows the viewer to remove a certain user. Should the button be pressed, a pop-up window appears asking for confirmation. At the bottom of the page, there is also a button to add a new account which redirects to the *create_account* view. Furthermore, there is a description at the top of the page on how new users can log in to their account should everyone have forgotten.

### Static

`user_list.css`: Adds formatting for the pop-up window by placing it in the middle of the page and creating the box it appears in. Also adds formatting to stretch the user list vertically instead of horizontally.

`user_list.js`: Is responsible for creating the pop-up window and managing the buttons on it. A function is assigned to each Remove User button. Upon press, all buttons on the page will be disabled. Then a template present in the *user_list.html* file is retrieved that contains the HTML code for the pop-up. This template is copied and placed on the page and the linked css file takes over the formatting. Additionally, the page is darkened and functions are added to the buttons in the pop-up. Should the positive confirmation button be clicked, a csrf token is retrieved and a fetch POST request is sent to the appropriate view containing the user to be deleted. Then the background color is reset, all buttons are reactivated, and the pop-up window container is deleted. The latter part of this is also done if the user choose to cancel the removal.

---

## Events

### Models

`EventCoordinator`: This model is meant to store information about a person that wants to request technical assistance at an event also referred to as an Event Coordinator. This model keeps track of a first name, last name, as well as email to contact them under.

`Happening`: A model to keep track of any rehearsals or performances that occur by linking the datetime field together with the duration.

`Event`: This model keeps track of every event registered on the website. It stores basic information such as the creation date, creation time, title, location, and category of the event. Additionally, it uses *ForeignKey* fields to keep track of the event's coordinator and manager (who will always be a *User*). Several events may be tied to the same coordinator or manager respectively. It also keeps track of the entire team that is assigned to an event in a *ManyToMany* field since a *User* may be involved in multiple events and events may involve multiple team members. All rehearsals and performances are stored in *Happening* model entries. New *Happening* entries are created for each performance or rehearsal that is added to an event.

### Views

`index`: Is only accessible to users that are logged in and will redirect to the Event Request Form otherwise. If the user is logged in, this view will load a list of all events a user is involved in as a team member. Information visible is the title and coordinator of the event in the title, when the event was registered, as well as the manager, team members, location, category, rehearsal dates and times, and performance dates and times of the event.If the user has a unique role, the view passes this information on the template. Additionally, a user with a unique role is able to see all events that exist, not just ones that they are involved in. Events passed to the template are divided into past and upcoming events. This division is decided based on the status of the *archived* field in the *Event* model.

`form`: The view for the event request form. On a GET request, this returns the form page. Should the user be logged in, first name, last name, and email are automatically filled in from the user's account. On a POST request, the *post* function is called. It attempts to find a coordinator match so that no duplicate coordinators are created. If the email does not match either of the names, an error is called. If a coordinator with this email does not exist, one is created. Next, rehearsals and performances are created as *Happening* objects. Finally, all created or found objects are combined with the remaining information in the request and an *Event* object is created. Any errors that occur throughout the process are returned to the user. After the form is succesfully processed, it redirects the user to a form review page.

`event_complete`: This view requires a POST method and a user with a unique role. It marks the event provided in the request as archived and then redirects to the initial events page.

`add_event_manager`: This view requires a POST method and a user with a unique role. It finds an event and user that match the respective id's provided in the request and adds the user as a manager to the event.

`add_team_member`: Once more, this view requires a POST method and a user with a unique role. It behaves very similiarly to the previous view by finding an event and users that match the respective id's provided in the request and adds the users as team members to the event.

### Templates

`form_review.html`: A page for the user to review their form. It shows them all relevant information which they inputted previously so that they can confirm for themselves it was correct.

`form.html`: The full html of the Event Request Form. All errors are displayed at the top of the page, directly below information regarding time zones. The first, last, and email fields are filled in automatically if the information is passed from the view. The *category* field options are also passed in from the view and are set as options in a *select* menu. The *location* field is a regular input linked to a *datalist* to provide some suggestive options for the location. Rehearsals and performances are in their own sections and have buttons to allow the user to decide the amount of each. If the form is reloaded due to an error, all inputted information, including the amount of rehearsals and performances, is kept and the error is displayed at the top of the page.

`index.html`: This page has three seperate section. The uppermost section provides a link to the Event Request Form to anyone that is logged in and wants to fill it out. The remaining two sections take the information submitted to the page by the view to display all events. Unique roles can also get access to buttons for each event with which they can archive it, add an event manager, or add a team member. If there are no events in a category, a message stating such is provided.

### Template Tags

`date.py`: This custom template tag takes a datetime object as input and returns a formatted version. This was required for the form review to make sure the formatting of the date were properly displayed.

`index.py`: This custom template tag allows the user to find specialiced indices of a list or other indexable object.

### Static

`form.js`: Manages all buttons in the Event Request Form. If there are no performance slots, it creates one. It also makes sure all buttons are disabled and enabled when they should be with the *checkButtons* function. The buttons should not allow there to be less than one performance, negative rehearsals, or more than 10 of either. Once a button is clicked, a rehearsal or performance slot is either added or removed by targeting the container and cloning a template into it.

`index.js`: Houses the code that allows the viewer to add an event manager or team members. The functions are already linked to the buttons in the HTML file. Once they are clicked, the container is targeted and the section with the input field is revealed and the original button is hidden using CSS style manipulation.

---

## ETC

### Settings

At the beginning of the document, I load a .env file with the respective django module (see installation above). I then set the email settings near the bottom of the document from this file to enable the sending of login information to the user. I have also set the timezone settings to be CET.
