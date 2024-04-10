import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('button', { name: 'Explore' }).click();

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
  
});