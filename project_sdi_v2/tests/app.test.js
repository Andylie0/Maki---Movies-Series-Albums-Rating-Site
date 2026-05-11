import { test, expect } from '@playwright/test';

test('should display welcome message', async ({ page }) => {
        await page.goto('http://localhost:5173')
        await expect(page.getByText('Welcome to Maki!')).toBeVisible()
    })

test('delete an item', async ({ page }) =>
    {
        await page.goto('http://localhost:5173/journal')
        const rows = await page.locator('.table-row')
        const initialCount = await rows.count()
        await rows.locator('.delete-button').first().click()
        await rows.locator('.delete-button').first().click()
        await expect(rows).toHaveCount(initialCount - 1)
    })

test('search filters movies', async ({ page }) => {
    await page.goto('http://localhost:5173/journal')
    await page.fill('.page-input', 'Matrix')
    const rows = await page.locator('.table-row')
    await expect(rows).toHaveCount(1)
})