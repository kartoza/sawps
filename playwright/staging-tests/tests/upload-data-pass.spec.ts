import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('button', { name: 'Upload your data' }).click();

  await page.waitForURL('**/upload');

  await page.getByRole('button', { name: 'CREATE A NEW PROPERTY' }).click();
  
  await page.locator('#input_propertyname').click();
  
  await page.locator('#input_propertyname').fill('staging-test');
  
  await page.getByRole('row', { name: 'Open/Closed System ​' }).getByLabel('​').click();
  
  await page.getByRole('option', { name: 'Open', exact: true }).click();
  
  await page.getByLabel('​', { exact: true }).click();
  
  await page.getByRole('option', { name: 'Private' }).click();
  
  await page.getByRole('button', { name: 'SAVE PROPERTY INFORMATION' }).click();
  
  await page.getByRole('button', { name: 'UPLOAD' }).click();
  
  const fileChooserPromise = page.waitForEvent('filechooser');

  await page.getByText('Browse').click();

  const fileChooser = await fileChooserPromise;

  await fileChooser.setFiles('tests/fixtures/parcel.geojson');

  await expect(page.getByText('parcel.geojson')).toBeVisible();
  
  await page.getByRole('button', { name: 'UPLOAD FILES' }).click();

  const closeModalButton = page.getByRole('button', { name: 'CLOSE' });

  await expect(closeModalButton).toBeVisible({timeout: 20000});

  await closeModalButton.click();
  
  const saveBoundary = page.getByRole('button', { name: 'SAVE BOUNDARY' });

  await saveBoundary.isEnabled();

  await saveBoundary.click();

  await page.getByText('Upload Species Population Data').isVisible({timeout: 60000});

  await page.getByRole('link', { name: 'ONLINE FORM' }).click();

  await page.waitForURL('**/upload-data/**')
});