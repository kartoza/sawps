import { test, expect } from '@playwright/test';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto('https://sawps.sta.do.kartoza.com/');
  await page.getByRole('button', { name: 'Explore' }).click();
  await expect(page.getByRole('tab', { name: 'LAYERS' })).toBeVisible();
  await page.getByRole('tab', { name: 'LAYERS' }).click();
  await expect(page.locator('#checkbox-list-label-2')).toContainText('Rivers');
  await expect(page.locator('#checkbox-list-label-3')).toContainText('Roads');
  await expect(page.locator('#checkbox-list-label-4')).toContainText('Biome type');
  await expect(page.locator('#checkbox-list-label-5')).toContainText('Critical Biodiversity areas');
  await expect(page.locator('#checkbox-list-label-6')).toContainText('Protected areas');
  await expect(page.locator('#checkbox-list-label-7')).toContainText('Cadastral boundaries');
  await expect(page.locator('#checkbox-list-label-8')).toContainText('Place names');
  await expect(page.locator('#checkbox-list-label-9')).toContainText('Properties');
  await expect(page.locator('#checkbox-list-label-10')).toContainText('NGI Aerial Imagery');
  await expect(page.getByLabel('Map')).toBeVisible();
});