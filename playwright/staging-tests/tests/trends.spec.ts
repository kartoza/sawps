import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('button', { name: 'Explore' }).click();

  await page.getByPlaceholder('Search place').click();

  await page.getByPlaceholder('Search place').fill('limpopo');

  await page.getByRole('option', { name: 'Limpopo, South Africa' }).click();

  await page.getByPlaceholder('Select').first().click();

  await page.getByPlaceholder('Select').first().fill('panthera');

  await page.getByRole('option', { name: 'Panthera leo' }).click();

  await expect(page.getByText('Panthera leo population (2023)0 - 4646 - 9292 - 138138 - 184184 -')).toBeVisible();

  await expect(page.getByLabel('Map')).toBeVisible();

  await expect(page.locator('#simple-tabpanel--1')).toContainText('Panthera leo population (2023)');

  await page.getByRole('tab', { name: 'TRENDS' }).click();

  await expect(page.getByLabel('TRENDS')).toContainText('SAWPS SUMMARY REPORT');

  await expect(page.getByLabel('TRENDS')).toContainText('National');

  await expect(page.locator('div').filter({ hasText: /^Panthera Leo National Population Trend$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Large Panthera Leo Populations$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Total area vs area available to Panthera leo$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Medium Panthera Leo Populations$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Small Panthera Leo Populations$/ }).nth(1)).toBeVisible();

  await expect(page.getByLabel('TRENDS')).toContainText('Provincial');

  await expect(page.locator('div:nth-child(2) > .SectionContainer > div > div:nth-child(2) > div > div > div > div > .ChartContainerBox').first()).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .ChartContainerBox').first()).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^KwaZulu-Natal$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^North West$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Limpopo$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .SectionContainer > div > div:nth-child(2) > div > div:nth-child(2) > div > div > .GroupedGrowthChartContainerBox').first()).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .SectionContainer > div > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(2) > .GroupedGrowthChartContainerBox')).toBeVisible();

  await expect(page.getByLabel('TRENDS')).toContainText('Properties');

  await expect(page.locator('div').filter({ hasText: /^amy test2$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Danang - KTZ1$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Dan - QWER$/ }).nth(1)).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Hluhluwe-Imfolozi Park$/ }).nth(1)).toBeVisible();
  
  await expect(page.locator('div').filter({ hasText: /^Venetia Limpopo NR$/ }).nth(1)).toBeVisible();
});