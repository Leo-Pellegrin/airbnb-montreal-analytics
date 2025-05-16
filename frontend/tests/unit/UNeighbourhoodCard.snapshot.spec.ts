// tests/unit/UNeighbourhoodCard.snapshot.spec.ts
import { mount } from '@vue/test-utils'
import UNeighbourhoodCard from '@/components/UNeighbourhoodCard.vue'
import { describe, it, expect } from 'vitest'

it('correspond au snapshot', () => {
  const wrapper = mount(UNeighbourhoodCard, {
    props: {
      name: 'Le Marais',
      medianPrice: 120,
      occupancy: 0.87,
      avg_sentiment: 4.5
    }
  })
  expect(wrapper.html()).toMatchSnapshot()
})