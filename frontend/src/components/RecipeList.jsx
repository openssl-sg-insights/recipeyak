import React from 'react'
import { Link } from 'react-router-dom'
import { Helmet } from 'react-helmet'

import Recipe from './RecipeItem.jsx'
import Loader from './Loader.jsx'

export const matchesQuery = ({
    name = '',
    author = ''
  }, query) => {
  const normalize = (x = '') => x.replace(/\W/g, '').toUpperCase()

  name = normalize(name)
  author = normalize(author)
  query = normalize(query)

  return name.includes(query) ||
    author.includes(query)
}

const Results = ({ recipes, query, onChange }) => {
  if (recipes.length === 0 && query === '') {
    return (
      <section className="d-flex grid-entire-row justify-center">
        <p className="fs-8 font-family-title mr-2">
          No recipes here.
        </p>

        <Link to='/recipes/add' className='my-button is-medium is-primary'>
          Add a Recipe
        </Link>
      </section>
    )
  } else if (recipes.length === 0 && query !== '') {
    return <p className="grid-entire-row justify-center fs-8 font-family-title">
      No recipes found matching <strong>{ query }</strong>
    </p>
  }
  return recipes
}

class RecipeList extends React.Component {
  state = {
    query: ''
  }

  static defaultProps = {
    cart: {},
    recipes: []
  }

  componentWillMount = () => {
    this.props.fetchData()
  }

  handleInputChange = e => {
    this.setState({ [e.target.name]: e.target.value })
  }

  render () {
    const {
      error,
      recipes,
      cart,
      removeFromCart,
      addToCart,
      loading
    } = this.props

    const {
      handleInputChange
    } = this

    const {
      query
    } = this.state

    if (error) return <p>Error fetching data</p>

    const results =
      recipes
      .filter(recipe => matchesQuery(recipe, query))
      .map(recipe =>
          <Recipe
            {...recipe}
            className='mb-0'
            inCart={ cart[recipe.id] > 0 ? cart[recipe.id] : 0 }
            key={ recipe.id }
            removeFromCart={ () => removeFromCart(recipe.id)}
            addToCart={ () => addToCart(recipe.id)}
          />
        )

    return (
      <div className="grid-container">
        <Helmet title='Recipes'/>
        <input
          autoFocus
          onChange={ handleInputChange }
          type='search'
          placeholder='search'
          className='my-input grid-entire-row'
          name='query'/>
        { loading
            ? <Loader/>
            : <Results recipes={ results } query={ query } />
        }
      </div>
    )
  }
}

export default RecipeList
