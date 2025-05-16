// cypress/e2e/neighbourhoods.cy.js
describe('Navigation quartiers', () => {
  it('L’utilisateur peut naviguer vers un quartier', () => {
    cy.visit('/neighbourhoods')
    cy.contains('Le Marais').click()
    cy.url().should('include', '/neighbourhoods/Le%20Marais')
  })
})