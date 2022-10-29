# [**Go Back**](https://github.com/lukebinmore/guideshare-api)

# **Table Of Contents**
- [**Go Back**](#go-back)
- [**Table Of Contents**](#table-of-contents)
- [**Features**](#features)
  - [**Implemented Features**](#implemented-features)
  - [**Possible Future Features**](#possible-future-features)

***

# **Features**

## **Implemented Features**

Below is a list of features implemented into the Admin panel of this API.

 - Django Admin Backend
   - Utilizing the Django Admin backend allows for a robust admin panel of all tables in the database, and ensures that the site is responsive.
   - ![Django Admin - Desktop](/docs/images/django-admin-desktop.png)
   - ![Django Admin - Mobile](/docs/images/django-admin-mobile.png)
 - Custom Color Theme
   - Admin panel has been adjusted to utilize GuideShare Green and orange color scheme.
 - Individually adjusted table pages for each Django Model
   - Ensures that the filters and search options are relevent to the page being viewed.
   - ![Django Admin Filters](/docs/images/django-admin-filters.png)
 - Relevent API endpoints
   - Only relevent API endpoints have been created to ensure that the api is only providing the information neccessary.
 - JWT Tokens
   - API has been configured to use JSON Web Tokens to imporve security.

***

## **Possible Future Features**

Below is a list of possible future features that could be implemented to improve the API.

 - Social Signon Itentegration
   - Would allow users to sign up and in with social accounts, to improve user experience.
 - Email or Username login Option
   - Allowing user to enter username or password, and use that to authenticate would simplify viewed experience.

**