import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('upload geojson', async ({ page }) => {

  //test.setTimeout(360000)
  
  await page.goto(url);

  const initialURL = page.url();

  await page.getByRole('link', { name: 'UPLOAD DATA' }).click();

  await page.getByRole('button', { name: 'CREATE A NEW PROPERTY' }).click();
  
  await page.locator('#input_propertyname').fill('admin-property');

  await page.getByRole('row', { name: 'Open/Closed System ​' }).getByLabel('​').click();
  
  await page.getByRole('option', { name: 'Closed' }).click();

  await page.getByRole('row', { name: 'Property Type ​' }).getByLabel('​').click();

  await page.getByRole('option', { name: 'Provincial' }).click();

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

  await fileChooser.setFiles('tests/fixtures/plot1.gpkg');

  await expect(page.getByText('plot1.gpkg')).toBeVisible();

  await page.getByRole('button', { name: 'UPLOAD FILES' }).click();

  await page.waitForLoadState('domcontentloaded');

  //await page.getByRole('button', { name: 'PROCESSING FILES...' }).waitFor({state: 'detached'});

  await expect(uploadPromise).toBeHidden();
  
  await page.waitForLoadState('domcontentloaded');

  const closeModalButton = page.getByRole('button', { name: 'CLOSE' });

  await expect(closeModalButton).toBeVisible({timeout: 20000});

  await closeModalButton.click();

  const saveBoundary = page.getByRole('button', { name: 'SAVE BOUNDARY' });

  await expect(saveBoundary).toBeEnabled({timeout: 20000});

  await saveBoundary.click();

  await expect(page.getByText('Upload Species Population Data')).toBeVisible({timeout: 10000});
 
  const finalURL = page.url();

  expect(finalURL).not.toBe(initialURL);
});
