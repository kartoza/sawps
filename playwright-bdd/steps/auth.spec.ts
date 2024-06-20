import { expect } from '@playwright/test';
import { createBdd } from 'playwright-bdd';

const { Given, When, Then } = createBdd();

/* Scenario: Check title */

Given('I am at {string}', async ({ page }, url) => {
  await page.goto(url);
  await page.getByRole('link', { name: "LOGIN" } ).click();
  await page.getByPlaceholder('E-mail address').fill('admin@example.com');
  await page.getByPlaceholder('Password').fill('admin');
  await page.getByRole('button', { name: 'LOGIN' }).click();
});

//When('I click {string}', async ({ page }, name) => {
//  await page.getByRole('link', { name }).click();
//});

Then('The title is {string}', async ({ page }, keyword) => {
  await expect(page).toHaveTitle(new RegExp(keyword));
});

Then('I check if {string} and {string} are both visible', async ({ page }, explore, uploadData) => {
  await expect(page.getByRole('button', { name: explore }).first()).toBeVisible();
  await expect(page.getByRole('button', { name: uploadData }).first()).toBeVisible();
});
