import { test, expect } from '@playwright/test';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto('https://sawps.sta.do.kartoza.com/');
  await page.getByRole('button', { name: 'Explore' }).click();
  await expect(page.getByRole('tab', { name: 'CHARTS' })).toBeVisible();
  await expect(page.getByLabel('Map')).toBeVisible();
  await page.getByRole('tab', { name: 'CHARTS' }).click();
  await expect(page.locator('#left-sidebar-container')).toContainText('Species');
  await expect(page.getByText('Ready to explore?')).toBeVisible();
  await expect(page.getByText('Choose a species to view the')).toBeVisible();
  await expect(page.locator('#combo-box-demo')).toBeEmpty();
  await page.locator('#combo-box-demo').click();
  await page.locator('#combo-box-demo').fill('panth');
  await page.getByRole('option', { name: 'Panthera leo' }).click();
  await expect(page.locator('div').filter({ hasText: /^SAWPS SUMMARY REPORT$/ })).toBeVisible();
  await expect(page.getByRole('img', { name: 'Species image', exact: true })).toBeVisible();
  await expect(page.getByLabel('CHARTS').getByRole('img', { name: 'Organisation image' })).toBeVisible();
  await expect(page.getByLabel('CHARTS').getByRole('img', { name: 'Property image' })).toBeVisible();
  await expect(page.getByRole('img', { name: 'Clock image' })).toBeVisible();
  await expect(page.getByRole('img', { name: 'Activity image' })).toBeVisible();
  await expect(page.locator('#charts-container')).toContainText('Species list: Panthera leo');
  await expect(page.locator('#left-sidebar-container')).toContainText('Organisation');
  await page.locator('nav').filter({ hasText: 'Organisations selected' }).getByRole('combobox').click();
  await page.locator('label').filter({ hasText: 'Select All' }).locator('path').click();
  await page.getByRole('option', { name: 'CapeNature' }).getByTestId('CheckBoxOutlineBlankIcon').click();
  await page.getByRole('button', { name: 'Close' }).click();
  await expect(page.locator('#charts-container')).toContainText('Organisation list: CapeNature');
  await expect(page.locator('#left-sidebar-container')).toContainText('Year');
  await expect(page.locator('.MuiSlider-track')).toBeVisible();
  await expect(page.locator('#left-sidebar-container')).toContainText('Activity');
  await page.getByPlaceholder('Select').nth(1).click();
  await page.locator('label').filter({ hasText: 'Select All' }).getByTestId('CheckBoxOutlineBlankIcon').click();
  await page.getByRole('button', { name: 'Close' }).click();
  await expect(page.locator('#charts-container')).toContainText('Activity list: Other, Planned Euthanasia/DCA, Planned Hunt/Cull, Translocation (Intake), Translocation (Offtake), Unplanned/Illegal Hunting');
  await expect(page.locator('#left-sidebar-container')).toContainText('Spatial filters');
  await expect(page.locator('#sidebarArrowsBox')).toContainText('Critical Biodiversity Area');
  await expect(page.locator('div').filter({ hasText: /^Number of properties per population category \(count\) of Panthera leo for 2023$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div:nth-child(2) > .ChartContainerBox')).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Number of properties per categories of area \(ha\) for Panthera leo for 2023$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div:nth-child(4) > .ChartContainerBox')).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Total count of Panthera leo per province for 2023$/ }).nth(2)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Activity count as % of total population of Panthera leo for 2023$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Total count per population estimate category of Panthera leo for 2023$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Mean and standard deviation of age classes of Panthera leo for 2023$/ }).nth(1)).toBeVisible();
});