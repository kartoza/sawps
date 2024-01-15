import { expect } from '@playwright/test';
import { createBdd } from 'playwright-bdd';

const { Given, When, Then } = createBdd();

/* Scenario: Check Explore page */

Given('I am on the project landing page {string}', async ({ page }, url) => {
  await page.goto(url);
  await page.getByRole('link', { name: "LOGIN" }).click();
  await page.getByPlaceholder('E-mail address').fill('admin@example.com');
  await page.getByPlaceholder('Password').fill('admin');
  await page.getByRole('button', { name: 'LOGIN' }).click();
});

When('I click on {string} button', async ({ page }, name) => {
  await page.getByRole('link', { name }).first().click();
});

Then('I should be redirected to the {string} view', async ({ page }, url) => {
  //await expect(page).toHaveTitle(new RegExp(keyword));
  await page.waitForURL(url);
});

Then('I should see the map canvas on the page', async ({ page },) => {
  await expect(page.getByRole('tab', { name: 'MAP' })).toBeVisible();
  // Map canvas is visible
  const map = 'canvas.maplibregl-canvas.mapboxgl-canvas';
  await expect(page.locator(map)).toBeVisible();
});

When('I configure filters', async ({ page },) => {
  await expect(page.getByRole('tab', { name: 'MAP' })).toBeVisible();
  // Map canvas is visible
  await page.locator('#combo-box-demo').click();

  await page.getByRole('option', { name: 'Panthera leo' }).click();

  await page.locator('nav').filter({ hasText: 'Organisation selected' }).getByLabel('Open').click();

  await page.getByRole('button', { name: 'Close' }).click();

});

Then('I should see data on the map and legend should be visible', async ({ page },) => {

  await expect(page.getByText('Panthera leo population (2024)')).toBeVisible();

  // Map canvas is visible
  const map = 'canvas.maplibregl-canvas.mapboxgl-canvas';

  await expect(page.locator(map)).toBeVisible();
});
