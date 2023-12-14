import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('button', { name: 'Explore' }).click();

  await page.waitForURL('**/map/');

  await expect(page.getByPlaceholder('Search place')).toBeEmpty();

  await page.getByPlaceholder('Search place').click();

  await page.getByPlaceholder('Search place').fill('limpopo');
  
  await page.getByRole('option', { name: 'Limpopo, South Africa' }).click();

  await page.getByPlaceholder('Select').first().click();

  await page.getByPlaceholder('Select').first().fill('pa');

  await page.getByRole('option', { name: 'Panthera leo' }).click();

  await page.getByRole('tab', { name: 'REPORTS' }).click();

  await page.locator('nav').filter({ hasText: 'Report selected' }).getByLabel('Open').click();

  await page.locator('label').filter({ hasText: 'Select All' }).getByTestId('CheckBoxOutlineBlankIcon').click();
  
  await page.getByRole('button', { name: 'Close' }).click();

  await expect(page.locator('div').filter({ hasText: /^Activity$/ })).toBeVisible();

  await page.getByLabel('Open').nth(4).click();

  await page.locator('label').filter({ hasText: 'Select All' }).getByTestId('CheckBoxOutlineBlankIcon').click();

  await page.getByRole('button', { name: 'Close' }).click();

  await expect(page.locator('#dataContainer')).toContainText('SAWPS SUMMARY REPORT');

  await expect(page.getByRole('img', { name: 'Species image', exact: true })).toBeVisible();

  await expect(page.locator('#dataContainer').getByRole('img', { name: 'Organisation image' })).toBeVisible();

  await expect(page.locator('#dataContainer').getByRole('img', { name: 'Property image' })).toBeVisible();

  await expect(page.getByRole('img', { name: 'Clock image' })).toBeVisible();

  await page.getByRole('img', { name: 'Activity image' }).click();

  await expect(page.locator('#dataContainer')).toContainText('Species list: Panthera leo');

  await expect(page.getByText('Activity Report')).toBeVisible();

  await expect(page.locator('#dataContainer')).toContainText('Translocation (Intake)');

  await expect(page.locator('#dataContainer')).toContainText('Planned Hunt/Cull');

  await expect(page.locator('#dataContainer')).toContainText('Unplanned/Illegal Hunting');

  await expect(page.locator('#dataContainer')).toContainText('Other');

  await expect(page.getByText('Venetia Limpopo NR', { exact: true }).first()).toBeVisible();

  await expect(page.getByText('amy\'s shape').nth(1)).toBeVisible();

  await expect(page.getByText('Mapungubwe GR', { exact: true }).first()).toBeVisible();

  await page.locator('span').filter({ hasText: '1960' }).nth(1).click();

  await page.locator('span').filter({ hasText: '1960' }).nth(1).click();

  await page.getByText('19602023').click();

  await expect(page.getByText('Mapungubwe GR', { exact: true }).first()).toBeVisible();

  await page.getByRole('tab', { name: 'CHARTS' }).click();

  await page.waitForLoadState('domcontentloaded');

  await page.getByText('19601992').click();

  await page.locator('span').filter({ hasText: '1992' }).nth(1).click();

  await page.getByRole('spinbutton').nth(1).click();

  await page.getByRole('spinbutton').nth(1).fill('1994');

  await page.getByRole('spinbutton').nth(1).click();

  await page.getByRole('spinbutton').nth(1).fill('2023');

  await page.getByRole('spinbutton').nth(1).press('Enter');

  await expect(page.getByText('Number of properties per population category (count) of Lion for')).toBeVisible();

  await expect(page.locator('.bar-chart').first()).toBeVisible();

  await expect(page.getByText('Number of properties per categories of area (ha) for Lion for')).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .ChartContainerBox > .ChartContainer > .ChartBox > .BarChartContainer > .bar-chart')).toBeVisible();

  await expect(page.getByText('Number of properties per categories of area (ha) available to Lion for')).toBeVisible();

  await expect(page.locator('div:nth-child(3) > .ChartContainerBox > .ChartContainer > .ChartBox > .BarChartContainer > .bar-chart')).toBeVisible();

  await expect(page.getByText('Number of properties per population category (population density) of Lion for')).toBeVisible();

  await expect(page.locator('div:nth-child(4) > .ChartContainerBox > .ChartContainer > .ChartBox > .BarChartContainer > .bar-chart')).toBeVisible();

  await expect(page.getByText('Number of properties per population category (population density) of Lion for')).toBeVisible();

  await expect(page.getByText('Total count of species per')).toBeVisible();

  await expect(page.locator('div:nth-child(5) > .MuiGrid-root > .ChartContainerBox > .ChartContainer > .ChartBox > .BarChartContainer > .bar-chart')).toBeVisible();

  await expect(page.locator('.DoughnutChartContainer > canvas').first()).toBeVisible();

  await expect(page.getByText('Activity count as % of total')).toBeVisible();

  await expect(page.getByText('Total count per population')).toBeVisible();

  await expect(page.getByText('Mean and standard deviation')).toBeVisible();

  await expect(page.locator('.ChartBox > canvas')).toBeVisible();

  await page.getByLabel('Number of properties per categories of area (ha) available to Lion for').click();

  await page.getByRole('tab', { name: 'TRENDS' }).click();

  await page.getByRole('tab', { name: 'MAP' }).click();

  await page.getByRole('tab', { name: 'TRENDS' }).click();

  await page.getByLabel('Open').first().click();

  await page.getByPlaceholder('Select').first().fill('pa');

  await page.getByRole('option', { name: 'Panthera leo' }).click();

  await page.locator('#left-sidebar-container').getByLabel('FILTERS').locator('div').filter({ hasText: 'Clear AllSpeciesOrganisation21 Organisations selected' }).first().click();

  await expect(page.getByText('National Population Trend')).toBeVisible();

  await expect(page.locator('.PopulationTrendChart').first()).toBeVisible();

  await expect(page.getByText('Large Panthera Leo Populations')).toBeVisible();

  await expect(page.locator('.bar-chart').first()).toBeVisible();

  await expect(page.getByText('Medium Panthera Leo')).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .GroupedGrowthChartContainerBox > .ChartContainers > .ChartContainer > .ChartBox > .bar-chart').first()).toBeVisible();

  await expect(page.getByText('Total area vs area available')).toBeVisible();

  await expect(page.locator('div:nth-child(3) > .ChartContainerBox > .ChartContainer > .ChartBox > div > canvas').first()).toBeVisible();

  await expect(page.getByText('Small Panthera Leo Populations')).toBeVisible();

  await expect(page.locator('div:nth-child(3) > .GroupedGrowthChartContainerBox > .ChartContainers > .ChartContainer > .ChartBox > .bar-chart')).toBeVisible();

  await expect(page.getByText('Provincial')).toBeVisible();

  await expect(page.getByText('Free State').nth(1)).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .SectionContainer > div > div:nth-child(2) > div > div > div > div > .ChartContainerBox > .ChartContainer > .ChartBox > .PopulationTrendChartContainer > .PopulationTrendChart').first()).toBeVisible();

  await expect(page.getByText('Gauteng').nth(1)).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .ChartContainerBox > .ChartContainer > .ChartBox > .PopulationTrendChartContainer > .PopulationTrendChart').first()).toBeVisible();

  await expect(page.getByText('KwaZulu-Natal').first()).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^KwaZulu-Natal$/ }).nth(1)).toBeVisible();

  await expect(page.getByText('North West', { exact: true }).first()).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^North West$/ }).nth(1)).toBeVisible();

  await expect(page.getByText('Limpopo', { exact: true }).first()).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Limpopo$/ }).nth(1)).toBeVisible();

  await expect(page.getByText('Free State').nth(2)).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .SectionContainer > div > div:nth-child(2) > div > div:nth-child(2) > div > div > .GroupedGrowthChartContainerBox').first()).toBeVisible();

  await expect(page.getByText('Gauteng').nth(2)).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .SectionContainer > div > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(2) > .GroupedGrowthChartContainerBox')).toBeVisible();

  await expect(page.getByText('amy\'s shape', { exact: true })).toBeVisible();

  await expect(page.locator('div:nth-child(3) > .SectionContainer > div > div:nth-child(2) > div > div > div > div:nth-child(2) > .ChartContainerBox > .ChartContainer > .ChartBox > .PopulationTrendChartContainer > .PopulationTrendChart')).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Hluhluwe-Imfolozi Park$/ }).nth(3)).toBeVisible();

  await expect(page.locator('div:nth-child(3) > .SectionContainer > div > div:nth-child(2) > div > div > div > div:nth-child(5) > .ChartContainerBox > .ChartContainer > .ChartBox > .PopulationTrendChartContainer > .PopulationTrendChart')).toBeVisible();

  await expect(page.getByText('Luna\'s testing farm', { exact: true })).toBeVisible();

  await expect(page.locator('div:nth-child(6) > .ChartContainerBox > .ChartContainer > .ChartBox > .PopulationTrendChartContainer > .PopulationTrendChart').first()).toBeVisible();

  await expect(page.getByText('test', { exact: true })).toBeVisible();

  await expect(page.locator('div:nth-child(7) > .ChartContainerBox > .ChartContainer > .ChartBox > .PopulationTrendChartContainer > .PopulationTrendChart')).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Venetia Limpopo NR$/ }).nth(1)).toBeVisible();
  
  await expect(page.getByText('Venetia Limpopo NR', { exact: true })).toBeVisible();
});