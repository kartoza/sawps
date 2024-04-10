import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {

  await page.goto(url);

  const initialURL = page.url();

  await page.getByRole('button', { name: 'Explore' }).click();

  await page.waitForURL('**/map/');

  const map = 'canvas.maplibregl-canvas.mapboxgl-canvas';

  await expect(page.locator(map)).toBeVisible();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.locator('div').filter({ hasText: /^Activity$/ }).first()).toBeVisible();

  await page.locator('nav').filter({ hasText: 'Select' }).last().getByLabel('Open').click();

  await expect(page.getByLabel('Map')).toBeVisible();
  
  await page.getByLabel('Map').click({
    position: {
      x: 458,
      y: 278
    }
  });
  await page.getByLabel('Zoom in').click();

  await page.getByLabel('Zoom out').click();

  // 3D view on
  await page.getByLabel('Toggle 3D view').click();

  // 3D view off
  await page.getByLabel('Toggle 3D view').click();

  await page.getByLabel('Map').click({
    position: {
      x: 495,
      y: 95
    }
  });

  await page.getByRole('tab', { name: 'REPORTS' }).click();

  await page.waitForURL('**/reports');

  await expect(page.getByText('Report Type')).toBeVisible();

  await page.locator('nav').filter({ hasText: 'Report selected' }).getByLabel('Open').click();

  await page.locator('label').filter({ hasText: 'Select All' }).getByTestId('CheckBoxOutlineBlankIcon').click();

  await page.locator('label').filter({ hasText: 'Select All' }).locator('path').click();

  await page.getByRole('button', { name: 'Close' }).click();

  await expect(page.getByText('Species', { exact: true })).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Organisation$/ })).toBeVisible();

  await expect(page.getByPlaceholder('Select').nth(1)).toBeEmpty();

  await page.getByPlaceholder('Select').nth(1).click();

  await expect(page.locator('div').filter({ hasText: /^Property$/ })).toBeVisible();

  await expect(page.getByText('Year')).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Activity$/ }).first()).toBeVisible();

  await page.getByRole('tab', { name: 'CHARTS' }).click();

  await page.waitForURL('**/charts');

  await page.getByRole('tab', { name: 'TRENDS' }).click();

  await page.waitForURL('**/trends');

  await expect(page.locator('div').filter({ hasText: /^Species$/ })).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Organisation$/ })).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Province$/ })).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Property$/ })).toBeVisible();

  const finalURL = page.url();

  expect(finalURL).not.toBe(initialURL);
  
});
