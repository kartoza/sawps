import { expect } from '@playwright/test';
import { createBdd } from 'playwright-bdd';

const { Given, When, Then } = createBdd();

/* Scenario: Check Explore page */

Given('I am on the landing page {string}', async ({ page }, url) => {
  await page.goto(url);
});

When('I click on {string}', async ({ page }, name) => {
  await page.getByRole('link', { name }).first().click();
});

Then('I should be redirected to {string} view', async ({ page }, url) => {
  //await expect(page).toHaveTitle(new RegExp(keyword));
  await page.waitForURL(url);
});

Then('I should see the map canvas', async ({ page },) => {
  await expect(page.getByRole('tab', { name: 'MAP' })).toBeVisible();
  // Map canvas is visible
  const map = 'canvas.maplibregl-canvas.mapboxgl-canvas';
  await expect(page.locator(map)).toBeVisible();

  // Reports, Charts, Trends tabs are present
  await expect(page.getByRole('tab', { name: 'REPORTS' })).toBeVisible();
  await expect(page.getByRole('tab', { name: 'CHARTS' })).toBeVisible();
  await expect(page.getByRole('tab', { name: 'TRENDS' })).toBeVisible();
  //await expect(page.getByRole('tab', { name: 'CHARTS' })).toBeVisible();
});