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

  // Zoom in
  const zoomIn = page.getByLabel('Zoom in');

  await zoomIn.click()
  
  // Enable dark mode
  const darkMode = page.getByLabel('Toggle Dark Mode');

  await darkMode.click()

  // Enable light mode
  const lightMode = page.getByLabel('Toggle Light Mode');

  await lightMode.click()

  /*await page.getByLabel('Map').click({
    position: {
      x: 297,
      y: 351
    }
  });*/

  // Zoom out
  const zoomOut = page.getByLabel('Zoom out');

  await zoomOut.click();
  
  // Reset bearing
  const resetBearing = page.getByLabel('Reset bearing to north');

  await resetBearing.click()

  const finalURL = page.url();

  expect(finalURL).not.toBe(initialURL);
  
});