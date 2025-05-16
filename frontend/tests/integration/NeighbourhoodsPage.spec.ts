// tests/integration/NeighbourhoodsPage.spec.ts
import { mount } from '@vue/test-utils'
import Neighbourhoods from '@/pages/neighbourhoods.vue'
import { describe, it, expect } from 'vitest'

describe('Page Neighbourhoods', () => {
  it('affiche la liste des quartiers mockés', async () => {
    const wrapper = mount(Neighbourhoods)
    // Attends le rendu
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Le Marais')
    expect(wrapper.text()).toContain('Montmartre')
  })
})