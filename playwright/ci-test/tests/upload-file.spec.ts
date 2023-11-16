import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('upload geojson', async ({ page }) => {

  test.setTimeout(250000)
  
  await page.goto(url);

  //const initialURL = page.url();

  await page.getByRole('link', { name: 'UPLOAD DATA' }).click();

  await page.getByRole('button', { name: 'CREATE A NEW PROPERTY' }).click();
  
  await page.locator('#input_propertyname').fill('admin-property');

  await page.getByRole('row', { name: 'Open/Closed System ​' }).getByLabel('​').click();
  
  await page.getByRole('option', { name: 'Closed' }).click();

  await page.getByRole('row', { name: 'Property Type ​' }).getByLabel('​').click();

  await page.getByRole('option', { name: 'Provincial' }).click();

  await page.screenshot({ path: 'playwright-report/data-upload-step-1.png', fullPage: true });

  await page.getByRole('button', { name: 'SAVE PROPERTY INFORMATION' }).click();

  await page.getByRole('button', { name: 'Create Property Boundary'}).isVisible();

  const upload = page.getByRole('button', { name: 'UPLOAD' });

  await upload.click();

  const uploadPromise = page.getByRole('button', { name: 'Upload' });

  await expect(uploadPromise).toBeVisible();

  await page.getByText('Uploaded Files').isVisible();

  await expect(page.getByRole('heading', { name: 'Supported formats: zip, json, geojson, gpkg, kml (CRS 4326)' })).toBeVisible();

  const fileChooserPromise = page.waitForEvent('filechooser');

  await page.getByText('Browse').click();

  const fileChooser = await fileChooserPromise;

  await fileChooser.setFiles('tests/fixtures/parcel.geojson');

  await expect(page.getByText('parcel.geojson')).toBeVisible();

  await page.getByRole('button', { name: 'UPLOAD FILES' }).click();

  await page.getByRole(
    'button', { name: 'PROCESSING FILES...' }).screenshot({ animations: 'disabled' });

  const saveBoundary = page.getByRole('button', { name: 'SAVE BOUNDARY' });

  await page.screenshot({ path: 'playwright-report/data-upload-step-2.png', fullPage: true });

  await saveBoundary.isEnabled({timeout: 250000});

  await uploadPromise.isHidden();

  await saveBoundary.click();

  await page.getByText('Upload Species Population Data').isVisible({timeout: 60000});

  await page.getByRole('button', { name: 'ONLINE FORM' }).click();

  await page.waitForURL('**/upload-data/**')

  //expect(finalURL).not.toBe(initialURL);
});