import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test.describe('upload data from xlsx file', () => {
  test.beforeEach(async ({ page }) => {
    // Go to the starting url before each test.
    await page.goto(url);
  });

  test('upload xlsx file', async ({ page }) => {
    await page.goto(url);

    await page.getByRole('button', { name: 'Upload your data' }).click();

    await page.waitForURL('**/upload');

    await page.getByText('Select Property').click();

    await page.getByRole('option', { name: 'admin-property2 (GACAAD0002)' }).click();

    await page.getByRole('button', { name: 'UPLOAD DATA' }).click();

    //await page.getByText('Browse').click();

    //await page.locator('div').filter({ hasText: 'Upload DataDrag & drop files' }).nth(1).setInputFiles('2023-integrated-dataset-template-V7_1.xlsx');

    const fileChooserPromise = page.waitForEvent('filechooser');

    await page.getByText('Browse').click();

    const fileChooser = await fileChooserPromise;

    await fileChooser.setFiles('tests/fixtures/2023-integrated-dataset-template-V7_1.xlsx');

    await expect(page.getByText('2023-integrated-dataset-')).toBeVisible();

    await page.getByRole('button', { name: 'UPLOAD FILE' }).click();

    await expect(page.getByRole('alert')).toBeVisible();

    await expect(page.getByText('Success')).toBeVisible();

    await expect(page.getByTestId('SuccessOutlinedIcon')).toBeVisible();

    await page.getByRole('button', { name: 'CLOSE' }).click();
  });

  test('updated data from xlsx file', async ({ page }) => {

    await page.getByRole('button', { name: 'EXPLORE' }).click();

    await page.waitForURL('**/map');

    await page.getByRole('tab', { name: 'REPORTS' }).click();

    await page.waitForURL('**/reports')

    await page.getByPlaceholder('Select').first().click();

    await page.getByRole('option', { name: 'Panthera leo' }).click();

    await page.getByRole('button', { name: 'Close' }).click();

    await page.locator('nav').filter({ hasText: 'Properties selected' }).getByRole('combobox').click();

    await page.locator('label').filter({ hasText: 'Select All' }).locator('path').click();

    await page.getByLabel('admin-property2 (GACAAD0002)').check();

    await page.getByRole('button', { name: 'Close' }).click();

    await expect(page.getByText('Property list: admin-property2')).toBeVisible();

    await expect(page.getByText('admin-property2', { exact: true })).toBeVisible();

  });

});
