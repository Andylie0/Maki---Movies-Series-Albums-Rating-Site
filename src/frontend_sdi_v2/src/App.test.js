import { describe, it, expect } from 'vitest'
import { reviews } from './data'

describe('CRUD operations', () => {
    it('should delete a review', () => {
        const deleted = reviews.filter(r => r.id !== 1)
        expect(deleted.length).toBe(reviews.length - 1)
        expect(deleted.find(r => r.id === 1)).toBeUndefined()
    })

    it('should edit a review', () => {
        const updated = reviews.map(r =>
            r.id === 1 ? {...r, text: "new text", rating: 5} : r
        )
        expect(updated.find(r => r.id === 1).text).toBe("new text")
    })

    it('should add a review', () => {
        const newReview = { id: 99, movie_id: 1, text: "great!", rating: 4 }
        const updated = [...reviews, newReview]
        expect(updated.length).toBe(reviews.length + 1)
        expect(updated.find(r => r.id === 99)).toBeDefined()
    })
})

