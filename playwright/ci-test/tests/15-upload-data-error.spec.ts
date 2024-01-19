import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test upload data error', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('button', { name: 'Upload your data' }).click();

  await page.getByRole('link', { name: 'UPLOAD DATA' }).click();

  await page.getByRole('button', { name: 'CREATE A NEW PROPERTY' }).click();

  await page.locator('#input_propertyname').click();

  await page.locator('#input_propertyname').fill('admin-property');

  await page.locator('#input_propertyname').click();

  await page.getByRole('row', { name: 'Open/Closed System ​' }).getByLabel('​').click();

  await page.getByRole('option', { name: 'Partially Open' }).click();

  await page.getByRole('row', { name: 'Property Type ​' }).getByLabel('​').click();

  await page.getByRole('option', { name: 'Provincial' }).click();

  await page.getByRole('button', { name: 'SAVE PROPERTY INFORMATION' }).click();

  await expect(page.getByText('Error! Property with name')).toBeVisible();
  
  await page.getByRole('button', { name: 'Close' }).click();
});