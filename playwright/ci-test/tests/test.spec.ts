import { test, expect } from '@playwright/test';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto('http://localhost:61100/');
  await page.getByRole('button', { name: 'Explore' }).click();
  await page.getByRole('tab', { name: 'REPORTS' }).click();
  await page.getByPlaceholder('Select').first().click();
});