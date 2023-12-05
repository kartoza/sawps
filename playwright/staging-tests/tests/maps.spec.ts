import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto(url);

  await expect(page.getByText('SOUTH AFRICAN WILDLIFE')).toBeVisible();

  await expect(page.getByTestId('landing-page-banner-image')).toBeVisible();

  await expect(page.getByRole('button', { name: 'About' })).toBeVisible();

  await expect(page.getByRole('button', { name: 'Explore' })).toBeVisible();

  await expect(page.getByRole('button', { name: 'Upload your data' })).toBeVisible();

  await page.getByRole('button', { name: 'Explore' }).click();

  await page.waitForURL('**/map/');

  await expect(page.getByPlaceholder('Search place')).toBeEmpty();

  await expect(page.getByPlaceholder('Select').first()).toBeEmpty();
  
  await expect(page.locator('#left-sidebar-container')).toContainText('Activity');

  await expect(page.locator('#left-sidebar-container')).toContainText('21 Organisations selected');

  await expect(page.locator('.TabHeaders > div:nth-child(2) > div')).toBeVisible();

  await expect(page.getByLabel('Map')).toBeVisible();

  await page.getByLabel('Zoom in').click();

  await page.getByLabel('Map').click({
    position: {
      x: 615,
      y: 144
    }
  });

  await page.getByLabel('Map').click({
    position: {
      x: 302,
      y: 334
    }
  });

  await page.getByLabel('Map').click({
    position: {
      x: 412,
      y: 258
    }
  });

  await page.getByLabel('Map').click({
    position: {
      x: 356,
      y: 86
    }
  });

  await page.getByLabel('Zoom out').click();

  await page.getByLabel('Map').click({
    position: {
      x: 307,
      y: 234
    }
  });

  await page.getByLabel('Map').click({
    button: 'right',
    position: {
      x: 337,
      y: 205
    }
  });

  await page.getByLabel('Map').click({
    button: 'right',
    position: {
      x: 381,
      y: 234
    }
  });

  await page.getByLabel('Toggle Dark Mode').click();

  await page.getByLabel('Toggle Light Mode').click();

  // Updated to 3D
  await page.getByLabel('Toggle 3D view').click();

  await page.getByLabel('Toggle 3D view').click();

  await page.getByPlaceholder('Search place').click();

  await page.getByPlaceholder('Search place').fill('Gauteng');

  await page.getByRole('option', { name: 'Gauteng, South Africa' }).click();

  await page.getByPlaceholder('Select').first().click();

  await page.getByPlaceholder('Select').first().fill('pan');

  await page.getByRole('option', { name: 'Panthera leo' }).click();

  await page.getByLabel('Map').click({
    position: {
      x: 703,
      y: 356
    }
  });

  await page.getByLabel('Map').click({
    position: {
      x: 433,
      y: 476
    }
  });

  await page.locator('nav').filter({ hasText: 'Organisations selected' }).getByLabel('Open').click();

  await page.getByText('Select All').click();

  await page.getByRole('listbox').getByText('CapeNature').click();

  await page.getByRole('button', { name: 'Close' }).click();

  await expect(page.getByText('Panthera leo population (2023)0 - 4646 - 9292 - 138138 - 184184 -')).toBeVisible();
  
  await expect(page.locator('#simple-tabpanel--1')).toContainText('Panthera leo population (2023)');
});