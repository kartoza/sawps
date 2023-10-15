import { test as setup, expect } from '@playwright/test';
import * as OTPAuth from "otpauth";

let url = '/';

let user_email = process.env.EMAIL;
let password = process.env.PASSWORD;
const secret = process.env.SECRET;
const authFile = 'e2e/.auth/adminAuth.json';


setup.describe('login and 2fa-authentication ', () => {
  // Create a new TOTP object.
  let totp = new OTPAuth.TOTP({
    issuer: "example.com",
    label: "AzureDiamond",
    algorithm: "SHA1",
    digits: 6,
    period: 30,
    secret: secret, // or 'OTPAuth.Secret.fromBase32(secret)'
  });
  


  setup('login and 2fa', async ({page}) => {

    await page.goto(url);

    const buttonSelector = 'div.landing-page-banner-text-btns button:text("LOGIN")';

    await page.waitForSelector(buttonSelector, {timeout: 2000});

    const initialURL = page.url();

    await page.click(buttonSelector);

    await page.waitForURL('**/accounts/login/');

    await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();

    await page.getByPlaceholder('E-mail address').fill(user_email);
    
    await page.getByPlaceholder('Password').fill(password);
    
    await page.getByRole('button', { name: 'LOGIN' }).click();

    await page.waitForURL('**/accounts/two-factor/authenticate/');

    await expect(page.getByRole('heading', { name: 'Two-Factor Authentication' })).toBeVisible();

    let token = totp.generate(); //opt generation

    await page.locator('input[id="id_otp_token"]').fill(token);

    await page.getByRole('button', { name: 'Authenticate' }).click();

    const finalURL = page.url();

    expect(finalURL).toBe(initialURL);

    await page.context().storageState({ path: authFile });
    
  });

});
