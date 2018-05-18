import React from 'react'
import { Link } from 'react-router-dom'

export const Results = ({ recipes, query }) => {
  if (recipes.length === 0 && query === '') {
    return (
      <section className="d-flex grid-entire-row justify-center">
        <p className="fs-6 font-family-title mr-2">
          No recipes here.
        </p>

        <Link to='/recipes/add' className='my-button is-primary'>
          Add a Recipe
        </Link>
      </section>
    )
  } else if (recipes.length === 0 && query !== '') {
    return <p className="grid-entire-row justify-center fs-6 font-family-title break-word">
      No recipes found matching <strong>{ query }</strong>
    </p>
  }
  return recipes
}

export default Results