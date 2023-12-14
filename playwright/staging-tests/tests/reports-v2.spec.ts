import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('button', { name: 'Explore' }).click();

  await page.waitForURL('**/map/');

  await page.getByPlaceholder('Search place').click();

  await page.getByPlaceholder('Search place').fill('limpopo');

  await page.getByRole('option', { name: 'Limpopo, South Africa' }).click();

  await page.getByPlaceholder('Select').first().click();

  await page.getByPlaceholder('Select').first().fill('panth');

  await page.getByRole('option', { name: 'Panthera leo' }).click();

  await page.getByRole('tab', { name: 'CHARTS' }).click();

  await expect(page.locator('div').filter({ hasText: /^Number of properties per population category \(count\) of Lion for 2023$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .ChartContainerBox')).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Number of properties per categories of area \(ha\) for Lion for 2023$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Number of properties per categories of area \(ha\) available to Lion for 2023$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Total count of species per province$/ }).nth(2)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Activity count as % of total population$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Total count per population estimate category for Panthera leo year 2023$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Mean and standard deviation of age classes for Panthera leo$/ }).nth(1)).toBeVisible();
  
  await expect(page.locator('#charts-container')).toContainText('SAWPS SUMMARY REPORT');
});