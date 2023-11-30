import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('button', { name: 'Upload your data' }).click();

  await page.getByText('Select Property').click();

  await page.getByRole('option', { name: 'admin1 (GACAAD0002)' }).click();

  await expect(page.getByLabel('Map')).toBeVisible();

  await expect(page.getByText('Upload Species Population Data')).toBeVisible();

  await expect(page.getByRole('button', { name: 'UPDATE PROPERTY BOUNDARY' })).toBeVisible();

  await page.getByRole('link', { name: 'ONLINE FORM' }).click();

  await expect(page.getByLabel('Map')).toBeVisible();

  await expect(page.locator('#app')).toContainText('DATA UPLOAD');

  await expect(page.locator('#app')).toContainText('1SPECIES DETAIL');

  await page.getByRole('navigation').click();

  await page.getByRole('link', { name: 'UPLOAD DATA' }).click();

  await page.getByRole('button', { name: 'CREATE A NEW PROPERTY' }).click();

  await page.locator('#input_propertyname').click();

  await page.locator('#input_propertyname').fill('test_property');

  await page.locator('#input_propertyname').click();

  await page.getByRole('row', { name: 'Open/Closed System ​' }).getByLabel('​').click();

  await page.getByRole('option', { name: 'Partially Open' }).click();

  await page.getByLabel('​', { exact: true }).click();

  await page.getByRole('option', { name: 'Private' }).click();

  await page.getByRole('button', { name: 'SAVE PROPERTY INFORMATION' }).click();

  await page.locator('#input_propertyname').click();

  await page.locator('#input_propertyname').press('End');

  await page.locator('#input_propertyname').fill('test_property');

  await page.getByRole('button', { name: 'SAVE PROPERTY INFORMATION' }).click();

  await expect(page.getByText('Error! Property with name')).toBeVisible();
  
  await page.getByRole('button', { name: 'Close' }).click();
});