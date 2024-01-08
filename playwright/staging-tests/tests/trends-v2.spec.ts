import { test, expect } from '@playwright/test';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto('https://sawps.sta.do.kartoza.com/');
  await page.getByRole('button', { name: 'Explore' }).click();
  await expect(page.getByRole('tab', { name: 'TRENDS' })).toBeVisible();
  await expect(page.getByLabel('Map')).toBeVisible();
  await page.getByRole('tab', { name: 'TRENDS' }).click();
  await expect(page.getByText('Ready to explore?')).toBeVisible();
  await expect(page.getByText('Choose a species to view the')).toBeVisible();
  await expect(page.locator('#left-sidebar-container')).toContainText('Species');
  await expect(page.getByPlaceholder('Select')).toBeEmpty();
  await page.getByPlaceholder('Select').click();
  await page.getByPlaceholder('Select').fill('pa');
  await page.getByRole('option', { name: 'Panthera leo' }).click();
  await expect(page.locator('div').filter({ hasText: /^SAWPS SUMMARY REPORT$/ })).toBeVisible();
  await expect(page.getByRole('img', { name: 'Species image', exact: true })).toBeVisible();
  await expect(page.getByLabel('TRENDS').getByRole('img', { name: 'Organisation image' })).toBeVisible();
  await expect(page.getByLabel('TRENDS').getByRole('img', { name: 'Property image' })).toBeVisible();
  await expect(page.getByRole('img', { name: 'Clock image' })).toBeVisible();
  await expect(page.getByLabel('TRENDS')).toContainText('Species list: Panthera leo');
  await expect(page.locator('#left-sidebar-container')).toContainText('Organisation');
  await page.locator('nav').filter({ hasText: 'Organisations selected' }).getByRole('combobox').click();
  await page.locator('label').filter({ hasText: 'Select All' }).locator('path').click();
  await page.getByRole('option', { name: 'CapeNature' }).getByTestId('CheckBoxOutlineBlankIcon').click();
  await page.getByRole('button', { name: 'Close' }).click();
  await expect(page.getByLabel('TRENDS')).toContainText('Organisation list: CapeNature');
  await page.locator('div').filter({ hasText: /^Province$/ }).click();
  await expect(page.locator('nav').filter({ hasText: 'Provinces selected' }).getByRole('combobox')).toBeEmpty();
  await page.getByRole('button', { name: 'Close' }).click();
  await expect(page.getByText('National', { exact: true })).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Panthera Leo National Population Trend$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Large Panthera Leo Populations \(>140 Individuals\)$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Total area vs area available to Panthera leo$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Medium Panthera Leo Populations \(20-140 Individuals\)$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Small Panthera Leo Populations \(<20 Individuals\)$/ }).nth(1)).toBeVisible();
  await expect(page.getByText('Provincial')).toBeVisible();
  await expect(page.locator('div:nth-child(2) > .SectionContainer > div > div:nth-child(2) > div > div > div > div > .ChartContainerBox').first()).toBeVisible();
  await expect(page.locator('div:nth-child(2) > .ChartContainerBox').first()).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Western Cape$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^KwaZulu-Natal$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^North West$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Limpopo$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div:nth-child(2) > .SectionContainer > div > div:nth-child(2) > div > div:nth-child(2) > div > div > .GroupedGrowthChartContainerBox').first()).toBeVisible();
  await expect(page.locator('div:nth-child(2) > .SectionContainer > div > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(2) > .GroupedGrowthChartContainerBox')).toBeVisible();
  await expect(page.getByText('Properties', { exact: true })).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^amy test2$/ }).nth(1)).toBeVisible();
  await expect(page.locator('#left-sidebar-container')).toContainText('Property');
});