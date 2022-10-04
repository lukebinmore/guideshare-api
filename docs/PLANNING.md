# [**Go Back**](https://github.com/lukebinmore/guideshare-api)

# **Table Of Contents**
- [**Go Back**](#go-back)
- [**Table Of Contents**](#table-of-contents)
- [**Planning Phase**](#planning-phase)
  - [**API Purpose**](#api-purpose)
  - [**Propsed Features**](#propsed-features)
  - [**Development Management**](#development-management)
    - [**Development Process**](#development-process)
    - [**Testing Methodologies**](#testing-methodologies)
    - [**Periodic Reviews**](#periodic-reviews)
    - [**Epics / User Stories**](#epics--user-stories)

***

# **Planning Phase**

This document outlines the planning phase of this project, including the following:

 - The purpose of this API.
 - The core proposed features of the API.
 - The methodologies that will be implemented during development.

## **API Purpose**

The purpose of this API is to provide a functional backend for the [GuideShare Site](https://github.com/lukebinmore/guideshare). This API will responsible for the following:

 - Providing data from database requested by site.
 - Inserting data sent from site into database.
 - Performing final validations before inserting data into database.
 - Provide an admin site for data administration.

***

## **Propsed Features**

Based on the goals of the GuideShare site, the features and requirements of this API have been outlined below. These features have been given MoSCoW priority based on their corresponding site features requirements. These features may be expanded should additional features in the react site project require it.

 - MOSCOW Key:
   - M - Must
   - S - Should
   - C - Could
   - W - Wont

| Feature | MOSCOW |
|---|---|
| Admin Control Panel | M |
| User Authentication | M |
| User Registration | M |
| Basic Profile Serializer | S |
| Full Profile Serializer | M |
| Basic Post Serializer | S |
| Full Post Serializer | M |
| Comment Serializer | M |

***

## **Development Management**

### **Development Process**

This project will be developed in conjunction with the react based GuideSite project, utilizing the same iterative Agile process. The same project used to manage the React project will be used to manage this API's development.

Similarly to the react project, Github's Milestones will be used to track Epics, and Issues will be used to track User Stories.

***

### **Testing Methodologies**

The development of this API will follow the same testing methodologies as the GuideShare react project. Manual testing will be carried out during each iteration of development, with any bugs or issues being reported via the commit message "Bug Fix" with details of the found resolution in the commit notes.

For bugs / issues found and fixed during development of this project, please [Click Here](https://github.com/search?q=repo%3Alukebinmore%2Fguideshare-api+%22Bug+Fix+-+%22&type=commits).

***

### **Periodic Reviews**

Each iteration of development will span the same one week period as this projects coutnerpart, with the same review being held at the end of each iteration. Incomplete Epics and User Stories will be moved back into the backlog, and tasks will be assigned for the next iteration.

To view the project (KanBan) for this site, please [Click Here](https://github.com/users/lukebinmore/projects/7/views/1).

***

### **Epics / User Stories**

For Epics relating to this project, please [Click Here](https://github.com/lukebinmore/guideshare-api/milestones?state=open).

For User Stories relating to this project, please [Click Here](https://github.com/lukebinmore/guideshare-api/issues?q=label%3A%22User+Story%22+).

***