import { expect } from '@playwright/test';
import { createBdd } from 'playwright-bdd';

const { Given, When, Then } = createBdd();

/* Scenario: Check title */

Given('I am at {string}', async ({ page }, url) => {
  await page.goto(url);
});

//When('I click {string}', async ({ page }, name) => {
//  await page.getByRole('link', { name }).click();
//});

Then('The title is {string}', async ({ page }, keyword) => {
  await expect(page).toHaveTitle(new RegExp(keyword));
});

Then('I check if {string} and {string} are both visible', async ({ page }, explore, uploadData) => {
  await expect(page.getByRole('button', { explore }).first()).toBeVisible();
  await expect(page.getByRole('button', { uploadData }).first()).toBeVisible();
});
