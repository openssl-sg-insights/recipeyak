import { connect } from 'react-redux'

import Recipe from '../Recipe.jsx'

const mapStateToProps = (state, props) => {
  const id = props.match.params.id
  const recipe = state.recipes[id]
  console.log(recipe)
  return {
    ingredients: recipe.ingredients,
    steps: recipe.steps,
    name: recipe.name,
    author: recipe.author,
    source: recipe.source,
    time: recipe.time,
  }
}

const ConnectedIngredients = connect(
  mapStateToProps,
)(Recipe)

export default ConnectedIngredients
