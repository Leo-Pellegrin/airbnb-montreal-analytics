// tests/unit/UNeighbourhoodCard.spec.ts
import { mount } from '@vue/test-utils'
import UNeighbourhoodCard from '@/components/UNeighbourhoodCard.vue'
import { describe, it, expect } from 'vitest'

describe('UNeighbourhoodCard', () => {
  it('affiche les props correctement', () => {
    const wrapper = mount(UNeighbourhoodCard, {
      props: {
        name: 'Le Marais',
        medianPrice: 120,
        occupancy: 0.87,
        avg_sentiment: 4.5,
        trend: 'up',
        description: 'Quartier historique',
        image: '/neigh-marais.jpg'
      }
    })
    expect(wrapper.text()).toContain('Le Marais')
    expect(wrapper.text()).toContain('120 $')
    expect(wrapper.text()).toContain('87 %')
    expect(wrapper.text()).toContain('4.50')
    expect(wrapper.text()).toContain('Quartier historique')
  })
})