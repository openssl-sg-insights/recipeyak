import React from 'react'
import { Link } from 'react-router-dom'
import PropTypes from 'prop-types'

class PasswordReset extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      email: '',
    }
  }

  handleInputChange = e => {
    this.setState({ [e.target.name]: e.target.value })
  }

  handleReset = (e) => {
    e.preventDefault()
    this.props.reset(this.state.email)
  }

  render () {
    return (
      <div className="container">
        <nav className="nav">
          <div className="nav-left">
            <div className="nav-item">
              <Link to="/" className="title">Caena</Link>
            </div>
          </div>
          <div className="nav-right">
            <Link to="/login" className="nav-item">Login</Link>
            <Link to="/signup" className="nav-item">Signup</Link>
          </div>
        </nav>

        <section className="section">
          <div className="container">
            <div className="columns">
              <div className="column is-one-third is-offset-one-third">
                <form onSubmit={ this.handleReset }>
                  <h1 className="title is-4">Password Reset</h1>
                  <div className="field">
                    <label className="label">Email</label>
                    <p className="control">
                      <input
                        onChange={ this.handleInputChange }
                        className="input"
                        type="email"
                        name="email"
                        placeholder="rick.sanchez@me.com"/>
                    </p>
                  </div>

                  {
                    !!this.props.error &&
                      <p className="help is-danger">Error with password reset</p>
                  }

                  <div className="field is-grouped">
                    <p className="control">
                      <button
                        className={ (this.props.loading ? 'is-loading ' : '') + 'button is-primary' }
                        type="submit">
                        Send Reset Email
                      </button>
                    </p>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </section>
      </div>
    )
  }
}

PasswordReset.PropTypes = {
  reset: PropTypes.func.isRequired,
  loading: PropTypes.bool.isRequired,
  error: PropTypes.bool.isRequired,
}

export default PasswordReset