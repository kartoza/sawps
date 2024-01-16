import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test.describe('upload files', () => {
  test.beforeEach(async ({ page }) => {
    // Go to the starting url before each test.
    await page.goto(url);
  });

  test('upload geopackages', async ({ page }) => {

    const initialURL = page.url();

    await page.getByRole('link', { name: 'UPLOAD DATA' }).click();

    await page.getByRole('button', { name: 'CREATE A NEW PROPERTY' }).click();

    await page.locator('#input_propertyname').fill('admin-property');

    await page.getByRole('row', { name: 'Open/Closed System ​' }).getByLabel('​').click();

    await page.getByRole('option', { name: 'Closed' }).click();

    await page.getByRole('row', { name: 'Property Type ​' }).getByLabel('​').click();

    await page.getByRole('option', { name: 'Provincial' }).click();

    await page.getByRole('button', { name: 'SAVE PROPERTY INFORMATION' }).click();

    await page.getByRole('button', { name: 'Create Property Boundary' }).isVisible();

    const upload = page.getByRole('button', { name: 'UPLOAD' });

    await upload.click();

    const uploadPromise = page.getByRole('button', { name: 'Upload' });

    await expect(uploadPromise).toBeVisible();

    await page.getByText('Uploaded Files').isVisible();

    await expect(page.getByRole('heading', { name: 'Supported formats: zip, json, geojson, gpkg, kml (CRS 4326)' })).toBeVisible();

    const fileChooserPromise = page.waitForEvent('filechooser');

    await page.getByText('Browse').click();

    const fileChooser = await fileChooserPromise;

    await fileChooser.setFiles('tests/fixtures/plot1.gpkg');

    await expect(page.getByText('plot1.gpkg')).toBeVisible();

    await page.getByRole('button', { name: 'UPLOAD FILES' }).click();

    await page.waitForLoadState('domcontentloaded');

    await expect(uploadPromise).toBeHidden();

    await page.waitForLoadState('domcontentloaded');

    const saveBoundary = page.getByRole('button', { name: 'SAVE BOUNDARY' });

    await expect(saveBoundary).toBeEnabled({ timeout: 20000 });

    await saveBoundary.click();

    await expect(page.getByText('Upload Species Population Data')).toBeVisible({ timeout: 10000 });

    const finalURL = page.url();

    expect(finalURL).not.toBe(initialURL);
  });

  test('upload geojson', async ({ page }) => {

    const initialURL = page.url();

    await page.getByRole('link', { name: 'UPLOAD DATA' }).click();

    await page.getByRole('button', { name: 'CREATE A NEW PROPERTY' }).click();

    await page.locator('#input_propertyname').fill('admin-property2');

    await page.getByRole('row', { name: 'Open/Closed System ​' }).getByLabel('​').click();

    await page.getByRole('option', { name: 'Closed' }).click();

    await page.getByRole('row', { name: 'Property Type ​' }).getByLabel('​').click();

    await page.getByRole('option', { name: 'Provincial' }).click();

    await page.getByRole('button', { name: 'SAVE PROPERTY INFORMATION' }).click();

    await page.getByRole('button', { name: 'Create Property Boundary' }).isVisible();

    const upload = page.getByRole('button', { name: 'UPLOAD' });

    await upload.click();

    const uploadPromise = page.getByRole('button', { name: 'Upload' });

    await expect(uploadPromise).toBeVisible();

    await page.getByText('Uploaded Files').isVisible();

    await expect(page.getByRole('heading', { name: 'Supported formats: zip, json, geojson, gpkg, kml (CRS 4326)' })).toBeVisible();

    const fileChooserPromise = page.waitForEvent('filechooser');

    await page.getByText('Browse').click();

    const fileChooser = await fileChooserPromise;

    await fileChooser.setFiles('tests/fixtures/parcel2.geojson');

    await expect(page.getByText('parcel2.geojson')).toBeVisible();

    await page.getByRole('button', { name: 'UPLOAD FILES' }).click();

    await page.waitForLoadState('domcontentloaded');

    await expect(uploadPromise).toBeHidden();

    await page.waitForLoadState('domcontentloaded');

    const saveBoundary = page.getByRole('button', { name: 'SAVE BOUNDARY' });

    await expect(saveBoundary).toBeEnabled({ timeout: 20000 });

    await saveBoundary.click();

    await expect(page.getByText('Upload Species Population Data')).toBeVisible({ timeout: 10000 });

    const finalURL = page.url();

    expect(finalURL).not.toBe(initialURL);
  });

  test('upload geojson zip files with shapefiles', async ({ page }) => {

    const initialURL = page.url();

    await page.getByRole('link', { name: 'UPLOAD DATA' }).click();

    await page.getByRole('button', { name: 'CREATE A NEW PROPERTY' }).click();

    await page.locator('#input_propertyname').fill('admin-property3');

    await page.getByRole('row', { name: 'Open/Closed System ​' }).getByLabel('​').click();

    await page.getByRole('option', { name: 'Closed' }).click();

    await page.getByRole('row', { name: 'Property Type ​' }).getByLabel('​').click();

    await page.getByRole('option', { name: 'Provincial' }).click();

    await page.getByRole('button', { name: 'SAVE PROPERTY INFORMATION' }).click();

    await page.getByRole('button', { name: 'Create Property Boundary' }).isVisible();

    const upload = page.getByRole('button', { name: 'UPLOAD' });

    await upload.click();

    const uploadPromise = page.getByRole('button', { name: 'Upload' });

    await expect(uploadPromise).toBeVisible();

    await page.getByText('Uploaded Files').isVisible();

    await expect(page.getByRole('heading', { name: 'Supported formats: zip, json, geojson, gpkg, kml (CRS 4326)' })).toBeVisible();

    const fileChooserPromise = page.waitForEvent('filechooser');

    await page.getByText('Browse').click();

    const fileChooser = await fileChooserPromise;

    await fileChooser.setFiles('tests/fixtures/parcel3.zip');

    await expect(page.getByText('parcel3.zip')).toBeVisible();

    await page.getByRole('button', { name: 'UPLOAD FILES' }).click();

    await page.waitForLoadState('domcontentloaded');

    await expect(uploadPromise).toBeHidden();

    await page.waitForLoadState('domcontentloaded');

    const saveBoundary = page.getByRole('button', { name: 'SAVE BOUNDARY' });

    await expect(saveBoundary).toBeEnabled({ timeout: 20000 });

    await saveBoundary.click();

    await expect(page.getByText('Upload Species Population Data')).toBeVisible({ timeout: 10000 });

    const finalURL = page.url();

    expect(finalURL).not.toBe(initialURL);
  });

  test('upload kml files', async ({ page }) => {

    const initialURL = page.url();

    await page.getByRole('link', { name: 'UPLOAD DATA' }).click();

    await page.getByRole('button', { name: 'CREATE A NEW PROPERTY' }).click();

    await page.locator('#input_propertyname').fill('admin-property4');

    await page.getByRole('row', { name: 'Open/Closed System ​' }).getByLabel('​').click();

    await page.getByRole('option', { name: 'Closed' }).click();

    await page.getByRole('row', { name: 'Property Type ​' }).getByLabel('​').click();

    await page.getByRole('option', { name: 'Provincial' }).click();

    await page.getByRole('button', { name: 'SAVE PROPERTY INFORMATION' }).click();

    await page.getByRole('button', { name: 'Create Property Boundary' }).isVisible();

    const upload = page.getByRole('button', { name: 'UPLOAD' });

    await upload.click();

    const uploadPromise = page.getByRole('button', { name: 'Upload' });

    await expect(uploadPromise).toBeVisible();

    await page.getByText('Uploaded Files').isVisible();

    await expect(page.getByRole('heading', { name: 'Supported formats: zip, json, geojson, gpkg, kml (CRS 4326)' })).toBeVisible();

    const fileChooserPromise = page.waitForEvent('filechooser');

    await page.getByText('Browse').click();

    const fileChooser = await fileChooserPromise;

    await fileChooser.setFiles('tests/fixtures/parcel4.kml');

    await expect(page.getByText('parcel4.kml')).toBeVisible();

    await page.getByRole('button', { name: 'UPLOAD FILES' }).click();

    await page.waitForLoadState('domcontentloaded');

    await expect(uploadPromise).toBeHidden();

    await page.waitForLoadState('domcontentloaded');

    const saveBoundary = page.getByRole('button', { name: 'SAVE BOUNDARY' });

    await expect(saveBoundary).toBeEnabled({ timeout: 20000 });

    await saveBoundary.click();

    await expect(page.getByText('Upload Species Population Data')).toBeVisible({ timeout: 10000 });

    const finalURL = page.url();

    expect(finalURL).not.toBe(initialURL);
  });

});
