import React from 'react'
import ReactDOM from 'react-dom'
import {MemoryRouter} from 'react-router'

import RecipeList from './RecipeList.jsx'

describe('<RecipeList/>', () => {
  it('renders without crashing', () => {
    const recipe = {
        id: 123,
        title: 'Some recipe title',
        author: 'Recipe author',
        url: '/someurl',
        source: 'http://example.com/recipeTitle',
        tags: ['OneTag', 'TwoTag'],
        inCart: false,
        removeFromCart: () => console.log('Remove from cart'),
        addToCart: () => console.log('Add to cart'),
      }
    const div = document.createElement('div')
    ReactDOM.render(<MemoryRouter><RecipeList recipes={[recipe]} /></MemoryRouter>, div)
  })
})
