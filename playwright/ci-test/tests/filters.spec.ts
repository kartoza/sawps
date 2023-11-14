import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('filter tests', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('button', { name: 'Explore' }).click();

  await page.locator('div').filter({ hasText: /^Search place$/ }).getByTestId('SearchIcon').click();

  await page.getByText('Search place').isVisible();

  await page.getByPlaceholder('Search place').click();

  await page.getByRole('img', { name: 'species image' }).click();

  await page.getByText('Species').click();

  await page.locator('#combo-box-demo').isVisible();

  await page.getByText('Activity').isVisible();

  await page.getByRole('img', { name: 'Organisation image' }).isVisible();

  await page.getByText('Organisation', { exact: true }).click();

  await page.getByText('Property').click();

  await page.getByRole('img', { name: 'watch image' }).isVisible();

  await page.getByText('Year').click();

  await page.getByText('19602023').click();

  await page.getByRole('img', { name: 'Filter image' }).isVisible();

  await page.getByText('Spatial filters').isVisible();

  await page.getByRole('tab', { name: 'REPORTS' }).click();

  await page.getByRole('button', { name: 'Clear All', exact: true }).click();

  await page.getByRole('img', { name: 'Info image' }).isVisible();
});