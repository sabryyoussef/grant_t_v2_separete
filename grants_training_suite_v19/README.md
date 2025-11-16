# Grants Training Suite - Odoo 19 Version

## Overview
This is the Odoo 19 compatible version of the Grants Training Suite (t66) module. The module provides comprehensive training center management from grant intake to certification.

## Version Information
- **Odoo Version**: 19.0
- **Module Version**: 19.0.1.0.0
- **Previous Version**: 18.0.1.13.0

## Key Changes from Odoo 18 to Odoo 19

### View Improvements
- All views use modern `list` views instead of deprecated `tree` views
- Modern attribute syntax (`invisible=`, `readonly=`, `required=`) instead of deprecated `attrs` and `states`
- Updated UI components for Odoo 19 compatibility

### Technical Updates
- Updated module version to 19.0.1.0.0
- Created migration scripts for smooth upgrade from Odoo 18
- All models, views, and security rules are Odoo 19 compatible

## Module Features

### Core Functionality
1. **Grant Intake Management**
   - Daily grant intakes and eligibility assessment
   - Automated batch processing
   - CSV import with field mapping

2. **Student Management**
   - Complete student lifecycle tracking
   - Progress tracking and monitoring
   - Document management

3. **Course & Session Management**
   - E-learning integration via Odoo Slides
   - Session templates and scheduling
   - Attendance tracking

4. **Assessment & Homework**
   - Assignment creation and submission
   - Automated grading with history tracking
   - Homework attempt management

5. **Certification System**
   - Automated certificate generation
   - Custom certificate templates
   - Rule-based certificate automation

6. **Reporting & Analytics**
   - Training dashboard with KPIs
   - Progress tracking and notifications
   - Integration reports

## Installation

1. Copy this module to your Odoo 19 addons directory
2. Update the apps list in Odoo
3. Install the module from the Apps menu

## Upgrade from Odoo 18

If upgrading from the Odoo 18 version:
1. Backup your database before upgrading
2. Update Odoo to version 19
3. The migration scripts will automatically handle data migration
4. Verify all data after migration

## Dependencies

Required Odoo modules:
- base
- mail
- portal
- contacts
- sale
- crm
- website
- survey
- website_slides
- documents
- certificate

## Configuration

After installation:
1. Configure security groups in Settings → Users & Companies
2. Set up sequence numbers in Settings → Technical → Sequences
3. Configure email templates for notifications
4. Set up cron jobs for automated tasks

## Support

For issues or questions:
- Check the documentation in the `docs/` directory
- Review the user guide: `user_guide.md`
- Consult the development guide: `docs/development/README.md`

## License

OEEL-1 (Odoo Enterprise Edition License)

## Author

Your Company
https://www.yourcompany.com

