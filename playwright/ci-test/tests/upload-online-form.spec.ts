import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json',
  viewport: {
    height: 680,
    width: 1200
  }
});

test.describe('navigation', () => {
  test.beforeEach(async ({ page }) => {
    // Go to the starting url before each test.
    await page.goto(url);
  });

  test('Add property data', async ({ page }) => {
    await page.goto(url);

    await page.getByRole('button', { name: 'Upload your data' }).click();

    await page.waitForURL('**/upload');

    await page.getByLabel('Select Property').click();
    await page.getByRole('option', { name: 'admin-property (GACAAD0001)' }).click();

    await page.waitForLoadState('domcontentloaded');
    await page.getByRole('link', { name: 'ONLINE FORM', exact: true }).click();
    await page.waitForURL('**/upload-data/**/');
    await page.waitForLoadState('domcontentloaded');
    await expect(page.getByText('DATA UPLOAD')).toBeVisible();

    await page.getByLabel('Scientific Name *').click();
    await page.getByRole('option', { name: 'Panthera leo' }).click();

    await expect(page.getByText('Scientific Name *')).toBeVisible();
    await expect(page.getByText('Common Name')).toBeVisible();

    await expect(page.getByText('Year of Count *')).toBeVisible();
    await page.getByPlaceholder('YYYY').click();
    page.once('dialog', dialog => {
      console.log(`Dialog message: ${dialog.message()}`);
      dialog.dismiss().catch(() => {});
    });
    await page.getByPlaceholder('YYYY').fill('2024');

    await page.getByLabel('Survey Method *').click();

    await page.getByRole('option', { name: 'Estimate' }).click();
    await expect(page.getByText('Survey Method *')).toBeVisible();
    await page.getByLabel('Adult Males', { exact: true }).click();
    await page.getByLabel('Adult Males', { exact: true }).fill('13');
    await page.getByLabel('Adult Females', { exact: true }).click();
    await page.getByLabel('Adult Females', { exact: true }).fill('12');
    await page.getByLabel('Subadult Males').click();
    await page.getByLabel('Subadult Males').fill('12');
    await page.getByLabel('Subadult Females').click();
    await page.getByLabel('Subadult Females').fill('12');
    await page.getByLabel('Juvenile Males').click();
    await page.getByLabel('Juvenile Males').fill('11');
    await page.getByLabel('Juvenile Females').click();
    await page.getByLabel('Juvenile Females').fill('05');
    await page.getByLabel('Area available to species *').click();
    await page.getByLabel('Area available to species *').fill('20');

    // Next tab
    await page.getByRole('button', { name: 'NEXT' }).click();
    await page.waitForLoadState("domcontentloaded");
    await page.getByLabel('Population Estimate Category *').click();
    await page.getByText('Rough guess (guesstimate)').click();
    await page.getByText('0', { exact: true }).click();
    await page.getByText('7', { exact: true }).click();
    await expect(page.getByRole('heading', { name: 'Population Estimate Certainty' })).toBeVisible();
    await page.getByRole('button', { name: 'Submit' }).click();

    await page.getByRole('button', { name: 'NEXT' }).click();
    await page.waitForLoadState("domcontentloaded");
    await expect(page.getByRole('button', { name: 'ACTIVITY DETAIL' })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Introduction/Reintroduction' })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Off-take' })).toBeVisible();
    await page.locator('#intake_adult_male').click();
    await page.locator('#intake_adult_male').fill('03');
    await page.locator('#intake_adult_female').click();
    await page.locator('#intake_adult_female').fill('02');
    await page.locator('#intake_juvenile_male').click();
    await page.locator('#intake_juvenile_male').fill('02');
    await page.locator('#intake_juvenile_female').fill('05');
    await page.locator('#intake_juvenile_female').click();
    await expect(page.locator('#intake_adult_male-label')).toBeVisible();
    await expect(page.locator('#intake_adult_female-label')).toBeVisible();
    await page.locator('#intake-activity-select').click();
    await page.getByRole('option', { name: 'Translocation (Intake)' }).click();
    await page.getByLabel('Source *').click();
    await page.getByLabel('Source *').fill('Park');
    await page.locator('#offtake_adult_male').click();
    await page.locator('#offtake_adult_male').fill('02');
    await page.locator('#offtake_adult_female').click();
    await page.locator('#offtake_adult_female').fill('01');
    await page.locator('#offtake_juvenile_male').click();
    await page.locator('#offtake_juvenile_female').click();
    await page.locator('#offtake_juvenile_female').fill('01');
    await page.getByRole('combobox', { name: 'Event ​', exact: true }).click();
    await page.getByRole('option', { name: 'Translocation (Offtake)' }).click();
    await expect(page.locator('#offtake_permit-label')).toBeVisible();
    await expect(page.locator('#intake_permit-label')).toBeVisible();

    // Next tab
    await page.getByRole('button', { name: 'NEXT', exact: true }).click();
    await expect(page.getByRole('heading', { name: 'Species Detail' })).toBeVisible();
    await expect(page.getByText('Scientific Name')).toBeVisible();
    await expect(page.getByText('Common Name')).toBeVisible();
    await expect(page.getByText('Year of Count')).toBeVisible();
    await expect(page.getByText('Species Present on Property')).toBeVisible();
    await expect(page.getByText('Survey Method')).toBeVisible();
    await expect(page.getByText('Sampling Effort Coverage')).toBeVisible();
    await expect(page.getByText('Population Estimate Category')).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Activity Detail' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'SAVE DRAFT' })).toBeVisible();
    
    await expect(page.getByRole('button', { name: 'SUBMIT', exact: true })).toBeVisible();
    await page.getByRole('button', { name: 'SUBMIT', exact: true }).click();
    await expect(page.getByRole('heading', { name: 'Upload Species Data' })).toBeVisible();
    await expect(page.getByRole('paragraph')).toContainText('Your data has been successfully saved!');
    await expect(page.getByRole('button', { name: 'Add another record' })).toBeVisible();
    await expect(page.getByLabel('Upload Species Data').locator('path')).toBeVisible();
    await expect(page.getByRole('button', { name: 'OK' })).toBeVisible();
    await page.getByRole('button', { name: 'OK' }).click();
    // Done updating details by filling forms
  });

  test('Test updated data', async ({ page }) => {
    await page.goto(url);

    await page.getByRole('button', { name: 'Explore' }).click();

    await page.getByRole('tab', { name: 'REPORTS' }).click();

    await page.getByPlaceholder('Select').first().click();

    await page.getByLabel('Panthera leo').check();

    await expect(page.getByText('SAWPS SUMMARY REPORT')).toBeVisible();
    await expect(page.getByRole('img', { name: 'Species image', exact: true })).toBeVisible();
    await expect(page.locator('#dataContainer').getByRole('img', { name: 'Organisation image' })).toBeVisible();
    await expect(page.locator('#dataContainer').getByRole('img', { name: 'Property image' })).toBeVisible();
    await expect(page.getByRole('img', { name: 'Clock image' })).toBeVisible();
    await expect(page.getByRole('img', { name: 'Activity image' })).toBeVisible();


    await expect(page.getByText('Species list: Panthera leo')).toBeVisible();
    await expect(page.getByText('Organisation list: Cape')).toBeVisible();
    await expect(page.getByText('Property list: admin-property')).toBeVisible();

    
    await page.getByRole('tab', { name: 'CHARTS' }).click();
    await page.getByLabel('Open').first().click();
    await page.getByRole('option', { name: 'Panthera leo' }).click();
    await expect(page.getByRole('tab', { name: 'CHARTS' })).toBeVisible();

    await page.waitForLoadState("domcontentloaded");

    await page.locator('div:nth-child(2) > .ChartContainerBox').click();
    await page.locator('div').filter({ hasText: /^Number of properties per population category \(count\) of Panthera leo for 2024$/ }).nth(1).click();
    await expect(page.locator('div:nth-child(2) > .ChartContainerBox')).toBeVisible();
    
    await page.keyboard.press("PageDown");
    await expect(page.locator('div:nth-child(4) > .ChartContainerBox')).toBeVisible();
    await expect(page.locator('div').filter({ hasText: /^Total count of Panthera leo per province for 2024$/ }).nth(2)).toBeVisible();
    await expect(page.locator('div').filter({ hasText: /^Activity count as % of total population of Panthera leo for 2024$/ }).nth(1)).toBeVisible();
    
    await page.keyboard.press("PageDown");
    await expect(page.locator('div').filter({ hasText: /^Total count per population estimate category of Panthera leo for 2024$/ }).nth(1)).toBeVisible();
    
    await page.keyboard.press("PageDown");
    await expect(page.locator('div').filter({ hasText: /^Mean and standard deviation of age classes of Panthera leo for 2024$/ }).nth(1)).toBeVisible();
    
    await expect(page.getByRole('button', { name: 'Download data visualisations' })).toBeVisible();
    await page.getByRole('button', { name: 'Download data visualisations' }).click();
  });

});