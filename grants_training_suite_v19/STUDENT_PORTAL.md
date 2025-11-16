# Student Portal - Grants Training Suite

## Overview

A simple student portal that allows students to register, login, and access their courses. This portal provides a user-friendly interface for students to manage their learning journey.

## Features

### 1. **Public Pages**
- **Home Page** (`/grants`): Landing page with registration and login options
- **Course Catalog** (`/grants/courses/catalog`): Browse all available courses
- **Course Details** (`/grants/courses/<id>`): View detailed information about a specific course
- **Student Registration** (`/grants/register`): Registration form for new students

### 2. **Student Portal (Authenticated)**
- **Dashboard** (`/my/student`): Personal dashboard showing:
  - Student information
  - Learning progress
  - Quick actions
  - Recent course sessions
  
- **My Courses** (`/my/courses`): List of enrolled courses
- **Course Details** (`/my/courses/<id>`): Detailed view of a specific course session
- **My Certificates** (`/my/certificates`): View and download earned certificates

## Student Registration Process

1. Navigate to `/grants/register`
2. Fill out the registration form with:
   - Personal information (name in English and Arabic, email, phone)
   - Birth date, gender, nationality
   - Language information (native language, English level)
   - Certificate information (if applicable)
   - Preferred course (optional)
3. Submit the form
4. System creates:
   - Student record
   - Portal user account
   - Welcome email is sent

## Login Process

Students can login using:
- Email as username
- Password (set during account creation or via password reset)
- Access their dashboard at `/my/student`

## Security

### Access Control
- Portal users can only view their own data
- Record rules ensure data isolation
- Students can:
  - Read and update their student profile
  - Read their course sessions (no write)
  - Read their certificates (no write)
  - Read their homework attempts (no write)
  - Browse active course integrations

### Portal Security Rules
- Students can only see records associated with their email
- All active course integrations are visible (public catalog)

## Routes

### Public Routes
- `/grants` - Home page
- `/grants/register` - Registration form
- `/grants/register/submit` - Registration submission (POST)
- `/grants/login` - Login (redirects to Odoo login)
- `/grants/courses/catalog` - Public course catalog
- `/grants/courses/<int:course_id>` - Public course detail

### Authenticated Routes (require login)
- `/my/student` - Student dashboard
- `/my/courses` - My courses list
- `/my/courses/<int:session_id>` - Course session detail
- `/my/certificates` - My certificates

## Installation & Setup

1. Ensure the module dependencies are installed:
   - `portal`
   - `website`
   - `website_slides`

2. Install the module: `grants_training_suite_v19`

3. The portal will be automatically available

4. Access the portal at: `http://your-domain/grants`

## Configuration

### Email Templates
- Welcome email is sent automatically upon registration
- Template: `grants_training_suite_v19.email_template_student_welcome`
- Can be customized in Settings > Technical > Email Templates

### Course Setup
- Active course integrations appear in the catalog
- Configure courses in: Grants Training > Configuration > Course Integrations

## Usage

### For Students
1. **Register**: Go to `/grants/register` and complete the registration form
2. **Check Email**: Receive welcome email with account details
3. **Login**: Use `/grants/login` or click Login from home page
4. **Dashboard**: View your progress and access courses
5. **Browse Courses**: Explore available courses
6. **Track Progress**: Monitor your learning journey

### For Administrators
1. **Manage Students**: View all registered students
2. **Assign Agents**: Assign agents to students
3. **Configure Courses**: Set up course integrations
4. **Monitor Progress**: Track student enrollment and completion

## Technical Details

### Controllers
- `main.py`: Main landing page controller
- `student_portal.py`: All portal functionality including registration, dashboard, courses

### Templates
- `portal_templates.xml`: All portal view templates
- Uses Bootstrap 5 for responsive design
- Extends `portal.portal_layout` for authenticated pages
- Extends `website.layout` for public pages

### Models Used
- `gr.student`: Student records
- `gr.course.session`: Course sessions
- `gr.certificate`: Certificates
- `gr.course.integration`: Course catalog
- `gr.homework.attempt`: Homework submissions

## Customization

### Styling
Templates use standard Odoo website/portal styling and can be customized through:
- Website > Themes
- Custom CSS in templates
- Bootstrap classes

### Adding New Pages
1. Add route in `student_portal.py`
2. Create template in `portal_templates.xml`
3. Update navigation as needed

### Email Templates
Customize welcome email and add new templates as needed in:
- `data/portal_email_templates.xml`

## Support

For issues or questions:
1. Check the logs for errors
2. Verify security rules are applied
3. Ensure portal users are correctly created
4. Test with demo data

## Troubleshooting

### Common Issues

#### Issue 1: Module fails to load
If the module fails to load, check the Odoo logs for specific errors. Common issues include:
- Missing dependencies (ensure `portal`, `website`, `website_slides` are installed)
- Database needs upgrade: `odoo-bin -u grants_training_suite_v19 -d your_database`

#### Issue 2: Portal pages show 404 errors
- Ensure the module is properly installed
- Check that website is enabled
- Verify controllers are loaded (check `__init__.py` imports)

#### Issue 3: Students can't see their data
- Verify portal security rules are applied
- Check that student email matches portal user email
- Ensure portal access rights are in ir.model.access.csv

### Field Name Compatibility Note

**Important:** The `res.groups` model uses `category_id` (not `category`) in the current Odoo version. If you see an error about "Invalid field 'category'", the security groups file is correctly using `category_id`.

In future Odoo versions, this may change to just `category`. Always check your specific Odoo version's documentation.
#### Common Warnings

**Duplicate field labels (WARNING)**

## Future Enhancements

Potential additions:
- Course enrollment from portal
- File upload for assignments
- Discussion forums
- Progress tracking visualizations
- Mobile app integration
- Social login integration
- Payment integration for paid courses
