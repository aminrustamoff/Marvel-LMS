# Project Documentation Instructions

This directory contains all technical documentation for the English Learning Platform.

## Purpose

The goal of this documentation is to keep the project organized, scalable, and easy to understand as it grows.

Every major architectural or functional decision should be documented before implementation whenever possible.

---

# Documentation Rules

* Keep documentation up to date.
* Every document should have a clear title.
* Use Markdown formatting.
* Prefer diagrams and tables when they improve understanding.
* Avoid duplicate information across documents.
* Update the related document whenever the implementation changes.

---

# Folder Structure

## system_design.md

Contains the overall architecture of the platform.

Include:

* High-level architecture
* Component diagram
* Module interactions
* Deployment architecture
* Scalability strategy
* Security overview

---

## database_design.md

Contains database design.

Include:

* Entity Relationship Diagram (ERD)
* Models
* Relationships
* Constraints
* Indexes
* Future schema changes

---

## api_design.md

Contains API documentation.

For every endpoint include:

* URL
* HTTP Method
* Authentication requirement
* Request Body
* Response
* Error Responses
* Permission rules

---

## user_flow.md

Describe how users interact with the platform.

Include separate flows for:

* Teacher
* Student
* Authentication
* Homework workflow
* Reading workflow
* Listening workflow

Flowcharts are encouraged.

---

## roadmap.md

Contains the development roadmap.

Organize work into milestones.

Example:

* MVP
* Beta Release
* Version 1.0
* Mobile Application
* AI Features

Completed tasks should be marked.

---

## features.md

Contains every planned feature.

Each feature should include:

* Description
* User Story
* Priority
* Current Status
* Dependencies

---

# Documentation Standards

Every document should contain:

* Purpose
* Scope
* Last Updated
* Author

---

# Naming Convention

Use lowercase filenames.

Examples:

* system_design.md
* database_design.md
* api_design.md

---

# Diagrams

Whenever possible use Mermaid diagrams.

Example diagrams:

* Flowcharts
* ER diagrams
* Sequence diagrams
* Architecture diagrams

---

# Version Control

Documentation must be committed together with the related code changes.

If a feature changes, update both:

* Source code
* Documentation

---

# Goal

The documentation should be detailed enough that a new developer can understand the project architecture and continue development without requiring additional explanations.
