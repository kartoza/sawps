import { test, expect } from '@playwright/test';

let url = '/';


test.describe('login and authentication ', () => {
  test.beforeEach(async ({ page }) => {
    // Go to the starting url before each test.
    await page.goto(url);
  });

  test('log in button', async ({page}) => {
    const buttonSelector = 'div.landing-page-banner-text-btns button:text("LOGIN")';

    await page.waitForSelector(buttonSelector, {timeout: 2000});

    const initialURL = page.url();

    await page.click(buttonSelector);

    await page.waitForURL('**/accounts/login/');

    await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();

    await page.getByPlaceholder('E-mail address').fill('admin@example.com');
    
    await page.getByPlaceholder('Password').fill('admin');
    
    await page.getByRole('button', { name: 'LOGIN' }).click();

    await page.waitForURL('**/accounts/two-factor/authenticate/');

    const finalURL = page.url();

    expect(finalURL).not.toBe(initialURL);
    
  });
});
