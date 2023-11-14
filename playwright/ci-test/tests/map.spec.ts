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

  await page.getByRole('tab', { name: 'REPORTS' }).click();

  await page.waitForURL('**/reports');

  await page.getByRole('tab', { name: 'CHARTS' }).click();

  await page.waitForURL('**/charts');

  await page.getByRole('tab', { name: 'TRENDS' }).click();

  await page.waitForURL('**/trends');

  const finalURL = page.url();

  expect(finalURL).not.toBe(initialURL);
  
});