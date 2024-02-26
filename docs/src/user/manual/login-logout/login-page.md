---
title: IDS SAWPS
summary: The SANBI Wildlife Protection System is a platform to track the population levels of endangered wildlife.
    - Jeremy Prior
    - Ketan Bamniya
date: 09-11-2023
some_url: https://github.com/kartoza/sawps/
copyright: Copyright 2023, SANBI
contact: PROJECT_CONTACT
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
context_id: FsEuBo8PhBfYJK2fueLWE4
---

# Login Page Documentation

The Login Page is the entry point to access the user's account within the application. This page provides a secure way for users to log in using their credentials. It offers a straightforward interface for entering the user's email address, and password, and includes an optional `Remember Me` checkbox for convenience.

## Login Form

![Login Form](./img/login-page-1.png)

1. **Email**: Enter a user's registered email address in this field. This is the email associated with the user's account.

2. **Password**: Input the user's password in this field. Passwords are case-sensitive, so users must ensure that they enter it correctly.

3. **Remember Me**: Users should check this box if they want the application to remember their login credentials for future sessions. This feature is optional and can be useful for quick and convenient access.

4. **Login Button**: Click the `LOGIN` button to submit the user's credentials and access their account. Upon clicking this button, the user will be redirected to the Two-Factor Authentication (2FA) page, where they need to enter the authentication code. If the user does not have the token generator, they can follow the [documentation](../../quickstart/index) provided to install it. For detailed information on 2FA, please refer to the documentation [here](./login-2fa-page.md).

5. **Register Here**: The `Register Here` link opens the [registration page](../register/register-page.md) for registration.

6. **Forgot Password**: The `Forgot Password` link opens the [forgot password](forgot-password.md) for reset password.

### Remember Me

The `Remember Me` checkbox allows users to opt for the application to remember the user's login information. When checked, users won't need to re-enter their email and password each time they visit the login page. This is particularly convenient for returning users who want a seamless login experience.

### Security

The `Login Page` is designed with security in mind to protect user accounts and sensitive information. It uses encryption protocols and best practices to ensure that users' login credentials are kept secure.

### Logging In

Please ensure that users enter their email and password correctly to access their accounts. After clicking the `LOGIN` button, users will be redirected to the two-factor authentication page within the application.

## Summary
The Login Page serves as the gateway to users' accounts, providing a secure and user-friendly way to access the application's features and functionality.
