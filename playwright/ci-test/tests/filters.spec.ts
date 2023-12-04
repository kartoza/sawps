import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('filter tests', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('button', { name: 'Explore' }).click();

  await page.waitForLoadState('domcontentloaded');

  await page.getByText('Search place').isVisible();

  await expect(page.getByPlaceholder('Search place')).toBeEditable();

  await expect(page.getByRole('img', { name: 'species image' })).toBeVisible();

  await page.getByText('Species');

  await expect(page.locator('#combo-box-demo')).toBeVisible();

  await expect(page.getByText('Activity')).toBeVisible();

  await expect(page.getByRole('img', { name: 'Organisation image' })).toBeVisible();

  await page.getByText('Organisation', { exact: true }).click();

  await page.getByText('Property').click();

  await expect(page.getByRole('img', { name: 'watch image' })).toBeVisible();

  await page.getByText('Year').click();

  await page.getByText('19602023').click();

  await expect(page.getByRole('img', { name: 'Filter image' })).toBeVisible();

  await page.getByText('Spatial filters').isVisible();

  await page.getByRole('tab', { name: 'REPORTS' }).click();

  await page.getByRole('button', { name: 'Clear All', exact: true }).click();

  await expect(page.getByRole('img', { name: 'Info image' })).toBeVisible();
});