// tests/a11y/UNeighbourhoodCard.a11y.spec.ts
import { render } from '@testing-library/vue'
import { axe } from 'vitest-axe'

import UNeighbourhoodCard from '@/components/UNeighbourhoodCard.vue'
import { it, expect } from 'vitest'


it('n\'a pas de violation a11y', async () => {
    const { container } = render(UNeighbourhoodCard, {
        props: {
            name: 'Le Marais',
            medianPrice: 120,
            occupancy: 0.87,
            avg_sentiment: 4.5
        }
    })
    const results = await axe(container)
    expect(results)
})