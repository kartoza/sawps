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

  await expect(page.getByText('Property').first()).toBeVisible();

  await expect(page.getByRole('img', { name: 'watch image' })).toBeVisible();

  await page.getByText('Year').click();

  await expect(page.getByRole('img', { name: 'Filter image' })).toBeVisible();

  await page.getByText('Spatial filters').isVisible();

  await page.getByPlaceholder('Search place').click();

  await page.getByPlaceholder('Search place').fill('limpopo');

  await page.getByRole('option', { name: 'Limpopo, South Africa' }).click();

  await page.locator('#combo-box-demo').click();

  await page.getByRole('option', { name: 'Panthera leo' }).click();

  await expect(page.getByText('Panthera leo population (2024)')).toBeVisible();
  // filter on map tab only has end year filter, no slider
  await page.getByRole('spinbutton').nth(0).click();

  await page.getByRole('spinbutton').nth(0).fill('2023');

  await page.getByRole('tab', { name: 'REPORTS' }).click();

  // filter on reports tab has slider, start-end year filters
  await page.locator('span').filter({ hasText: '2023' }).nth(1).click();
 
  await page.getByRole('spinbutton').nth(1).click();

  await page.getByRole('spinbutton').nth(1).fill('2022');

  await page.getByRole('button', { name: 'Clear All', exact: true }).click();

  await expect(page.getByRole('img', { name: 'Info image' })).toBeVisible();

});