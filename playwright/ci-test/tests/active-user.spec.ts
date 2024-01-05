import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test.describe('admin operations', () => {
    test.beforeEach(async ({ page }) => {
      // Go to the starting url before each test.
      await page.goto(url);
    });

    test('add data', async ({ page }) => {

        await page.locator('#dropdownMenu').click();

        await page.getByRole('link', { name: 'Django Admin' }).click();

        await page.waitForURL('**/admin/');

        // Add Province
        await page.getByRole('link', { name: 'Provinces' }).click();
        await page.waitForURL('**/admin/property/province/');
        await page.getByRole('link', { name: 'Add Province' }).click();
        await expect(page.getByLabel('Name:')).toBeVisible();
        await page.getByLabel('Name:').fill('Gauteng');
        await page.getByRole('button', { name: 'Save', exact: true }).click();

        // Add organisation
        await page.getByRole('link', { name: 'Organisations' }).click();
        await page.waitForURL('**/admin/stakeholder/organisation/');
        await page.getByRole('link', { name: 'Add Organisation' }).click();
        await expect(page.getByLabel('Name:')).toBeVisible();
        await page.getByLabel('Name:').fill('Cape');
        //await page.getByLabel('Short code:').fill('GACA0002');
        await page.getByLabel('National:').selectOption('true');
        await page.getByLabel('Province:').selectOption('1');
        await page.getByRole('button', { name: 'Save', exact: true }).click();

        // Add population estimation
        await page.getByRole('link', { name: 'Population Estimate Categories' }).click();
        await page.waitForURL('**/admin/population_data/populationestimatecategory/');
        await page.getByRole('link', { name: 'Add Population Estimate Category' }).click();
        await expect(page.getByLabel('Name:')).toBeVisible();
        await page.getByLabel('Name:').fill('Rough guess (guesstimate)');
        await page.getByRole('button', { name: 'Save', exact: true }).click();

        //Add taxa
        await page.getByRole('link', { name: 'Taxa' }).click();
        await page.getByRole('link', { name: 'Add Taxon' }).click();
        await page.getByLabel('Scientific name:').fill('Panthera leo');
        await page.getByLabel('Common name verbatim:').fill('Lion');
        await page.getByLabel('Colour variant:').selectOption('true');
        await page.getByLabel('Taxon rank:').selectOption('1');
        await page.getByLabel('Show on front page').check();
        await page.getByLabel('Is selected').check();
        await page.getByRole('button', { name: 'Save', exact: true }).click();
    });

    test('update admin roles', async ({ page }) => {

        const initialURL = page.url();

        await page.locator('#dropdownMenu').click();

        await page.getByRole('link', { name: 'Django Admin' }).click();

        await page.waitForURL('**/admin/');

        await page.getByRole('link', { name: 'Users', exact: true }).click();

        await page.getByRole('link', { name: 'admin', exact: true }).click();

        //await page.getByTitle('Click to choose all groups at once.').click();

        //await page.getByText('User permissions:').click();

        //await page.getByTitle('Click to choose all user permissions at once.').click();

        //await page.locator('#user_profile-0').getByText('User role type id:').selectOption('5');

        await page.locator('#user_profile-0').getByText('Current organisation:').click();

        await page.getByLabel('×Cape').locator('b').click();

        await page.getByRole('option', { name: 'Cape' }).click();

        await page.getByRole('button', { name: 'Save', exact: true }).click();

        const finalURL = page.url();

        expect(finalURL).not.toBe(initialURL);
    });
});
