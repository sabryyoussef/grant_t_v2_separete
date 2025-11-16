# Quick Start Guide - Odoo 19 Version

## Module Information
- **Name**: Grants Training Suite (t66)
- **Version**: 19.0.1.0.0
- **Odoo Version**: 19.0
- **Location**: `/grants_training_suite_v19/`

---

## Installation Steps

### 1. For New Installation

```bash
# Module is already in your addons path
# Just restart Odoo (if needed) and update apps list
```

In Odoo:
1. Go to **Apps**
2. Click **Update Apps List**
3. Search for **"t66"** or **"Grants Training Suite"**
4. Click **Install**

### 2. For Upgrade from Odoo 18 Version

⚠️ **Important**: Backup your database first!

```bash
# After upgrading Odoo to version 19
# The module will automatically detect the upgrade
```

In Odoo:
1. Go to **Apps**
2. Remove the "Apps" filter
3. Search for **"t66"**
4. Click **Upgrade**
5. The migration script will run automatically

---

## Post-Installation Configuration

### 1. User Groups
Go to **Settings → Users & Companies → Groups**
- Configure "Training Manager" group
- Configure "Training Officer" group
- Assign users to appropriate groups

### 2. Email Templates
Go to **Settings → Technical → Email → Templates**
- Review notification templates
- Update sender information
- Test email delivery

### 3. Sequences
Go to **Settings → Technical → Sequences & Identifiers → Sequences**
- Review sequence numbers for:
  - Student IDs
  - Certificate numbers
  - Batch numbers
  - Assignment numbers

### 4. Cron Jobs
Go to **Settings → Technical → Automation → Scheduled Actions**
- Enable automated tasks:
  - Certificate generation
  - Progress tracking updates
  - Notification delivery

---

## Module Access

### Main Menu Items

The module adds these menu items to Odoo:

```
Training
├── Dashboard
├── Students
│   ├── All Students
│   ├── Enrollments
│   └── Progress Tracking
├── Courses
│   ├── Training Programs
│   ├── Course Sessions
│   ├── Session Templates
│   └── Course Integrations
├── Intake & Grants
│   ├── Intake Batches
│   └── Document Requests
├── Assignments
│   ├── All Assignments
│   └── Homework Attempts
├── Certificates
│   ├── All Certificates
│   ├── Certificate Templates
│   └── Certificate Automation
├── Reports
│   ├── Training Dashboard
│   ├── Progress Reports
│   └── Integration Reports
└── Configuration
    ├── Settings
    └── Notifications
```

---

## Quick Feature Overview

### 1. Intake Management
**Menu**: Training → Intake & Grants → Intake Batches

- Import CSV files with grant recipients
- Map CSV columns to student fields
- Bulk process eligibility
- Automated student creation

### 2. Student Management
**Menu**: Training → Students → All Students

- Complete student profiles
- Progress tracking
- Document management
- Communication history

### 3. Training Programs
**Menu**: Training → Courses → Training Programs

- Define program structure
- Link e-learning courses
- Set completion criteria
- Track student progress

### 4. Course Sessions
**Menu**: Training → Courses → Course Sessions

- Schedule training sessions
- Manage attendance
- Link to e-learning content
- Session templates

### 5. Assignments & Homework
**Menu**: Training → Assignments

- Create assignments
- Student submissions
- Automated grading
- Grade history tracking

### 6. Certificates
**Menu**: Training → Certificates

- Manual certificate generation
- Automated certificate rules
- Custom templates
- PDF generation

### 7. Dashboard & Reports
**Menu**: Training → Dashboard

- Real-time KPIs
- Student statistics
- Completion rates
- Progress analytics

---

## Common Tasks

### Task 1: Import New Grant Recipients

1. Go to **Training → Intake & Grants → Intake Batches**
2. Click **Create**
3. Upload CSV file
4. Map columns using the wizard
5. Click **Process Batch**
6. Review created students

### Task 2: Enroll Students in Program

1. Go to **Training → Students → All Students**
2. Select students
3. Click **Action → Enroll in Program**
4. Choose program and session
5. Click **Enroll**

### Task 3: Create Certificate Template

1. Go to **Training → Certificates → Certificate Templates**
2. Click **Create**
3. Design template with fields:
   - `${student_name}`
   - `${program_name}`
   - `${completion_date}`
4. Save and test

### Task 4: Set Up Certificate Automation

1. Go to **Training → Certificates → Certificate Automation**
2. Click **Create**
3. Configure rules:
   - Select program
   - Set completion threshold
   - Define requirements
4. Activate automation

### Task 5: View Training Dashboard

1. Go to **Training → Dashboard**
2. Set date range
3. Review KPIs:
   - Total students
   - Enrolled students
   - Completion rate
   - Certificate generation
4. Export analytics if needed

---

## Testing Checklist

After installation, test these features:

- [ ] Create a test student manually
- [ ] Import a CSV file via intake batch
- [ ] Create a training program
- [ ] Enroll a student in the program
- [ ] Create an assignment
- [ ] Submit homework as a student (portal)
- [ ] Generate a certificate manually
- [ ] View the training dashboard
- [ ] Check email notifications
- [ ] Test certificate automation

---

## Demo Data

The module includes demo data for testing:

```bash
# Demo data includes:
- Sample intake batches
- Test students
- Training programs
- Course sessions
- Assignments
- Certificates
- E-learning courses
```

To install with demo data:
1. Make sure demo data is enabled in Odoo settings
2. Install the module
3. Demo data will be created automatically

---

## Troubleshooting

### Issue: Module not visible in Apps
**Solution**: Update the apps list (Apps → Update Apps List)

### Issue: Migration errors
**Solution**: 
1. Check the log file for specific errors
2. Ensure database backup before migration
3. Run in test mode first

### Issue: Email notifications not sending
**Solution**:
1. Check email server configuration (Settings → General Settings → Email)
2. Verify email templates
3. Check cron jobs are active

### Issue: Certificate generation fails
**Solution**:
1. Check certificate template syntax
2. Verify student has completed requirements
3. Review automation rules

---

## File Locations

```
Module Root: grants_training_suite_v19/
├── Models: models/*.py
├── Views: views/*.xml
├── Security: security/*
├── Data: data/*.xml
├── Demo: demo/*.xml
├── Tests: tests/*.py
├── Migrations: migrations/19.0.1.0.0/
└── Docs: docs/
```

---

## Next Steps

1. **Read the full documentation**
   - `README.md` - Module overview
   - `user_guide.md` - Detailed user guide
   - `ODOO19_CONVERSION_NOTES.md` - Conversion details

2. **Explore the interface**
   - Navigate all menu items
   - Try creating test records
   - Explore dashboard and reports

3. **Configure for your needs**
   - Customize certificate templates
   - Set up automation rules
   - Configure email notifications
   - Adjust user permissions

4. **Import your data**
   - Prepare CSV files
   - Test with small batch first
   - Process full data import

5. **Train your users**
   - Share user guide
   - Provide demo environment
   - Conduct training sessions

---

## Support

For detailed information:
- Technical documentation: `docs/development/README.md`
- Implementation guide: `docs/implementation_guide/use_case_scenarios.md`
- Error tracking: `docs/error_tracking/ERROR_TRACKING_SYSTEM.md`

---

**Module Status**: ✅ Ready for Use

**Last Updated**: November 16, 2025

**Odoo Version**: 19.0

