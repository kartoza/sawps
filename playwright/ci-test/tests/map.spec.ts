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
  await expect(page.getByLabel('Map')).toBeVisible();
  await page.getByLabel('Map').click({
    position: {
      x: 458,
      y: 278
    }
  });
  await page.getByLabel('Zoom in').click();
  await page.getByLabel('Zoom out').click();
  await page.getByLabel('Map').click({
    position: {
      x: 495,
      y: 95
    }
  });

  await page.getByRole('tab', { name: 'REPORTS' }).click();

  await page.waitForURL('**/reports');

  await page.getByRole('tab', { name: 'CHARTS' }).click();

  await page.waitForURL('**/charts');

  await page.getByRole('tab', { name: 'TRENDS' }).click();

  await page.waitForURL('**/trends');

  const finalURL = page.url();

  expect(finalURL).not.toBe(initialURL);
  
});