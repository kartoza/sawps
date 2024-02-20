import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test.describe('navbar-navigation', () => {
  test.beforeEach(async ({ page }) => {
    // Go to the starting url before each test.
    await page.goto(url);
  });

  test('test from about', async ({ page }) => {
    const initialURL = page.url();
    await page.getByRole('link', { name: 'ABOUT' }).click();
    const finalURL = page.url();
    expect(finalURL).not.toBe(initialURL);
    await expect(page.getByText('SOUTH AFRICAN WILDLIFE POPULATION SYSTEM (SAWPS)', { exact: true })).toBeVisible();
    await expect(page.frameLocator('[data-testid="about-page-video-frame"]').locator('.ytp-cued-thumbnail-overlay-image')).toBeVisible();
    await expect(page.getByRole('link', { name: 'Logo', exact: true })).toBeVisible();
    await page.getByRole('link', { name: 'Logo', exact: true }).click();
  });

  // Explore
  test('test from explore', async ({ page }) => {
    const initialURL = page.url();
    await page.locator('#navbarNav').getByRole('link', { name: 'EXPLORE' }).click();
    await page.waitForURL('**/map/');
    const finalURL = page.url();
    expect(finalURL).not.toBe(initialURL);
    await expect(page.getByLabel('Map')).toBeVisible();
    await page.goBack();

    await page.getByRole('link', { name: 'ABOUT' }).click();
    await page.waitForURL('**/about/');
    const aboutURL = page.url();
    expect(aboutURL).not.toBe(initialURL);
    await expect(page.getByText('SOUTH AFRICAN WILDLIFE POPULATION SYSTEM (SAWPS)', { exact: true })).toBeVisible();
    await expect(page.frameLocator('[data-testid="about-page-video-frame"]').locator('div').filter({ hasText: 'SAWPS Testing video' }).nth(4)).toBeVisible();
    await page.goBack();

    await expect(page.getByRole('link', { name: 'UPLOAD DATA' })).toBeVisible();
    await page.getByRole('link', { name: 'UPLOAD DATA' }).click();
    await page.waitForURL('**/upload');
    const uploadURL = page.url();
    expect(uploadURL).not.toBe(initialURL);
    await expect(page.getByText('DATA UPLOAD', { exact: true })).toBeVisible();
    await expect(page.getByPlaceholder('Search place')).toBeEmpty();
    await expect(page.getByRole('button', { name: 'CREATE A NEW PROPERTY' })).toBeVisible();
    await page.goBack();
    
    //await page.getByRole('link', { name: 'EXPLORE' }).click();
    await page.getByRole('link', { name: 'HELP' }).click();
    await page.waitForURL('**/help/');
    const helpURL = page.url();
    expect(helpURL).not.toBe(initialURL);
    await expect(page.getByText('Help', { exact: true })).toBeVisible();
    await page.goBack();
    
    await page.getByRole('link', { name: 'CONTACT' }).click();
    await page.waitForURL('**/contact/');
    const contactURL = page.url();
    expect(contactURL).not.toBe(initialURL);
    await expect(page.getByRole('heading', { name: 'Contact Us' })).toBeVisible();
    await page.getByRole('link', { name: 'Logo', exact: true }).click();
  });

  // Upload data
  test('test from upload data', async ({ page }) => {
    const initialURL = page.url();
    await page.getByRole('link', { name: 'UPLOAD DATA' }).click();
    await page.waitForURL('**/upload');
    const uploadURL = page.url();
    expect(uploadURL).not.toBe(initialURL);
    await expect(page.getByText('DATA UPLOAD', { exact: true })).toBeVisible();
    await expect(page.getByPlaceholder('Search place')).toBeEmpty();
    await expect(page.getByRole('button', { name: 'CREATE A NEW PROPERTY' })).toBeVisible();
    await expect(page.getByLabel('Map')).toBeVisible();
    await page.goBack();

    await page.getByRole('link', { name: 'ABOUT' }).click();
    const aboutURL = page.url();
    expect(aboutURL).not.toBe(initialURL);
    await expect(page.getByText('SOUTH AFRICAN WILDLIFE POPULATION SYSTEM (SAWPS)', { exact: true })).toBeVisible();
    await page.goBack();

    await page.getByRole('link', { name: 'EXPLORE' }).click();
    await page.waitForURL('**/map/');
    const exploreURL = page.url();
    expect(exploreURL).not.toBe(initialURL);
    await expect(page.getByRole('tab', { name: 'MAP' })).toBeVisible();
    await expect(page.getByLabel('Map')).toBeVisible();
    await expect(page.getByRole('tab', { name: 'REPORTS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'CHARTS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'TRENDS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'LAYERS' })).toBeVisible();
    //await page.getByRole('link', { name: 'UPLOAD DATA' }).click();
    await page.goBack();

    await page.getByRole('link', { name: 'HELP' }).click();
    await page.waitForURL('**/help/');
    const helpURL = page.url();
    expect(helpURL).not.toBe(initialURL);
    await expect(page.getByText('Help', { exact: true })).toBeVisible();
    await page.goBack();

    await page.getByRole('link', { name: 'CONTACT' }).click();
    await page.waitForURL('**/contact/');
    const contactURL = page.url();
    expect(contactURL).not.toBe(initialURL);
    await expect(page.getByRole('heading', { name: 'Contact Us' })).toBeVisible();
    await page.getByRole('link', { name: 'Logo', exact: true }).click();
  });

  //Help
  test('test from help', async ({ page }) => {
    const initialURL = page.url();
    await page.getByRole('link', { name: 'HELP' }).click();
    await page.waitForURL('**/help/');
    const helpURL = page.url();
    expect(helpURL).not.toBe(initialURL);
    await expect(page.getByText('Help', { exact: true })).toBeVisible();


    await page.getByRole('link', { name: 'ABOUT', exact: true }).click();
    await page.waitForURL('**/about/');
    const aboutURL = page.url();
    expect(aboutURL).not.toBe(initialURL);
    await expect(page.getByText('SOUTH AFRICAN WILDLIFE POPULATION SYSTEM (SAWPS)', { exact: true })).toBeVisible();
    await expect(page.frameLocator('[data-testid="about-page-video-frame"]').locator('div').filter({ hasText: 'SAWPS Testing video' }).nth(4)).toBeVisible();
    await page.goBack();

    await expect(page.getByRole('link', { name: 'EXPLORE', exact: true })).toBeVisible();
    await page.getByRole('link', { name: 'EXPLORE', exact: true }).click();
    await page.waitForURL('**/map/');
    const exploreURL = page.url();
    expect(exploreURL).not.toBe(initialURL);
    await expect(page.getByRole('tab', { name: 'MAP' })).toBeVisible();
    await expect(page.getByLabel('Map')).toBeVisible();
    await expect(page.getByRole('tab', { name: 'REPORTS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'CHARTS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'TRENDS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'FILTERS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'LAYERS' })).toBeVisible();
    //await page.getByRole('link', { name: 'HELP' }).click();
    await page.goBack();

    await page.getByRole('link', { name: 'UPLOAD DATA', exact: true }).click();
    await page.waitForURL('**/upload');
    const uploadURL = page.url();
    expect(uploadURL).not.toBe(initialURL);
    await expect(page.getByText('DATA UPLOAD', { exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'CREATE A NEW PROPERTY' })).toBeVisible();
    await expect(page.getByLabel('Map')).toBeVisible();
    await expect(page.getByPlaceholder('Search place')).toBeEmpty();
    //await page.getByRole('link', { name: 'HELP' }).click();
    await page.goBack();

    await page.getByRole('link', { name: 'CONTACT', exact: true }).click();
    await page.waitForURL('**/contact/');
    const contactURL = page.url();
    expect(contactURL).not.toBe(initialURL);
    await expect(page.getByRole('heading', { name: 'Contact Us' })).toBeVisible();
    await page.getByRole('link', { name: 'Logo', exact: true }).click();
  });

  // Contact us
  test('test from contact us', async ({ page }) => {
    const initialURL = page.url();
    await page.locator('#navbarNav').getByRole('link', { name: 'CONTACT' }).click();
    await page.waitForURL('**/contact/');
    const contactURL = page.url();
    expect(contactURL).not.toBe(initialURL);
    await expect(page.getByRole('heading', { name: 'Contact Us' })).toBeVisible();
    await expect(page.locator('.account-form')).toBeVisible();
    await page.goBack();

    await page.getByRole('link', { name: 'ABOUT' }).click();
    await page.waitForURL('**/about/');
    const aboutURL = page.url();
    expect(aboutURL).not.toBe(initialURL);
    await expect(page.getByText('SOUTH AFRICAN WILDLIFE POPULATION SYSTEM (SAWPS)', { exact: true })).toBeVisible();
    await expect(page.frameLocator('[data-testid="about-page-video-frame"]').locator('div').filter({ hasText: 'SAWPS Testing video' }).nth(4)).toBeVisible();
    await page.goBack();

    await page.locator('#navbarNav').getByRole('link', { name: 'EXPLORE' }).click();
    await page.waitForURL('**/map/');
    const exploreURL = page.url();
    expect(exploreURL).not.toBe(initialURL);
    await expect(page.getByRole('tab', { name: 'MAP' })).toBeVisible();
    await expect(page.getByLabel('Map')).toBeVisible();
    await expect(page.getByRole('tab', { name: 'REPORTS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'CHARTS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'TRENDS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'FILTERS' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'LAYERS' })).toBeVisible();
    //await page.getByRole('link', { name: 'CONTACT' }).click();
    await page.goBack();

    await page.getByText('UPLOAD DATA').click();
    await page.waitForURL('**/upload');
    const uploadURL = page.url();
    expect(uploadURL).not.toBe(initialURL);
    await expect(page.getByText('DATA UPLOAD', { exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'CREATE A NEW PROPERTY' })).toBeVisible();
    await expect(page.getByLabel('Map')).toBeVisible();
    await expect(page.getByPlaceholder('Search place')).toBeEmpty();
    //await page.getByRole('link', { name: 'HELP' }).click();
    await page.goBack();

    await page.getByRole('link', { name: 'HELP' }).click();
    await page.waitForURL('**/help/');
    const helpURL = page.url();
    expect(helpURL).not.toBe(initialURL);
    await expect(page.getByText('Help', { exact: true })).toBeVisible();
    await page.locator('#navbarNav').getByRole('link', { name: 'CONTACT' }).click();
    await expect(page.getByRole('heading', { name: 'Contact Us' })).toBeVisible();
    await page.getByRole('link', { name: 'Logo', exact: true }).click();
    const finalURL = page.url();
    expect(finalURL).toBe(initialURL);
    await expect(page.getByText('SOUTH AFRICAN WILDLIFE')).toBeVisible();
    await expect(page.getByRole('button', { name: 'About' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Explore' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Upload your data' })).toBeVisible();
  });

});
