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

  /*await page.getByLabel('Map').click({
    position: {
      x: 618,
      y: 284
    }
  });*/
  
  await page.getByLabel('Toggle Dark Mode').click();

  await page.getByLabel('Toggle Light Mode').click();

  await page.getByLabel('Zoom in').click();

  /*await page.getByLabel('Map').click({
    position: {
      x: 297,
      y: 351
    }
  });*/

  await page.getByLabel('Zoom out').click();
  
  await page.getByLabel('Reset bearing to north').click();

  const finalURL = page.url();

  expect(finalURL).not.toBe(initialURL);
  
});