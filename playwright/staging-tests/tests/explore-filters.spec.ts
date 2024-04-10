import { test, expect } from '@playwright/test';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto('https://sawps.sta.do.kartoza.com/');
  await page.getByRole('button', { name: 'Explore' }).click();
  await expect(page.getByRole('tab', { name: 'FILTERS' })).toBeVisible();
  await expect(page.getByLabel('Map')).toBeVisible();
  await expect(page.locator('#left-sidebar-container')).toContainText('Search place');
  await expect(page.locator('#left-sidebar-container')).toContainText('Clear All');
  await expect(page.getByPlaceholder('Search place')).toBeEmpty();
  await page.getByPlaceholder('Search place').click();
  await page.getByPlaceholder('Search place').fill('limpopo');
  await page.getByRole('option', { name: 'Limpopo, South Africa' }).click();
  await expect(page.getByLabel('Zoom out')).toBeVisible();
  await expect(page.locator('#left-sidebar-container')).toContainText('Species');
  await expect(page.locator('#combo-box-demo')).toBeEmpty();
  await page.locator('#combo-box-demo').click();
  await page.locator('#combo-box-demo').fill('pant');
  await page.getByRole('option', { name: 'Panthera leo' }).click();
  await expect(page.getByText('Panthera leo population (2023)')).toBeVisible();
  await expect(page.locator('#left-sidebar-container')).toContainText('Organisation');
  await expect(page.locator('nav').filter({ hasText: 'Organisations selected' }).getByRole('combobox')).toBeEmpty();
  await page.locator('label').filter({ hasText: 'Select All' }).locator('path').click();
  await page.getByLabel('Select All').check();
  await page.getByRole('button', { name: 'Close' }).click();
  await expect(page.locator('#left-sidebar-container')).toContainText('Property');
  await expect(page.locator('nav').filter({ hasText: 'Properties selected' }).getByRole('combobox')).toBeEmpty();
  await page.getByRole('button', { name: 'Close' }).click();
  await expect(page.locator('#left-sidebar-container')).toContainText('Year');
  await expect(page.locator('.MuiSlider-track')).toBeVisible();
  await expect(page.locator('#left-sidebar-container')).toContainText('Activity');
  await expect(page.getByPlaceholder('Select').nth(1)).toBeEmpty();
  await page.getByRole('button', { name: 'Close' }).click();
  await expect(page.locator('#left-sidebar-container')).toContainText('Spatial filters');
  await expect(page.locator('#sidebarArrowsBox')).toContainText('Critical Biodiversity Area');
  await expect(page.getByLabel('Map')).toBeVisible();
  await page.getByLabel('Zoom out').click();
  await page.getByLabel('Zoom in').click();
  await page.getByLabel('Toggle 3D view').click();
  await expect(page.getByLabel('Map')).toBeVisible();
  await page.getByLabel('Toggle 3D view').click();
  await page.getByLabel('Toggle Dark Mode').click();
  await page.getByLabel('Toggle Light Mode').click();
});