# JOBPEDIA – Job Portal Web Application

JOBPEDIA is a full-featured **Job Portal Web Application** built with **Django** and **PostgreSQL**, designed for recruiters and applicants to manage job postings and applications efficiently. This project demonstrates authentication, role-based dashboards, application management, and responsive UI using **Tailwind CSS**.

---

## Features

- **User Roles:**
  - **Recruiters** – Post jobs, view applications, update application status.
  - **Applicants** – Browse jobs, apply to jobs, manage applications, upload resumes.
  - **Admin (Superuser)** – Full control via Django admin panel.
  
- **Authentication:**
  - Registration and login with role selection (recruiter or applicant)
  - Logout and role-based redirection
  - User profile view and update

- **Job Management (Recruiters):**
  - Create, update, and delete job postings
  - Set job details: title, company name, location, salary range, type, remote options
  - Track applications and update their status

- **Application Management (Applicants):**
  - Apply to jobs with resume upload
  - View submitted applications
  - Track status: pending, reviewed, accepted, rejected

- **Dashboards:**
  - **Recruiter Dashboard:** View all posted jobs, applications per job
  - **Applicant Dashboard:** View jobs applied to, status of applications

- **Responsive UI:**
  - Tailwind CSS-based theme (**Obsidian Glow**)
  - Dark-themed modern interface
  - Hero sections, cards for jobs, application tables

- **Resume Management:**
  - Upload resumes in PDF format
  - Recruiters can view applicant resumes

---

## Technology Stack

- **Backend:** Python, Django  
- **Frontend:** Tailwind CSS, HTML, Django Templates  
- **Database:** PostgreSQL  
- **Others:** django-widget-tweaks, Pillow (for file uploads)  

---
